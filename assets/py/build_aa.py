"""Convert aa_source.md into _data/alternate_advancement.json."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).resolve().parent / "aa_source.md"
OUT = ROOT / "_data" / "alternate_advancement.json"

CLASS_ORDER = [
    "WAR",
    "CLR",
    "PAL",
    "RNG",
    "SHD",
    "DRU",
    "MNK",
    "BRD",
    "ROG",
    "SHM",
    "NEC",
    "WIZ",
    "MAG",
    "ENC",
    "BST",
]
CLASS_SET = set(CLASS_ORDER)

GROUPS = {
    "ALL": CLASS_ORDER,
    "MANA CLASSES": [
        "CLR",
        "PAL",
        "RNG",
        "SHD",
        "DRU",
        "BRD",
        "SHM",
        "NEC",
        "WIZ",
        "MAG",
        "ENC",
        "BST",
    ],
    "HYBRIDS + MELEES": ["WAR", "PAL", "RNG", "SHD", "MNK", "BRD", "ROG", "BST"],
    "CASTERS + PRIESTS": ["CLR", "DRU", "SHM", "NEC", "WIZ", "MAG", "ENC"],
    "MELEE CLASSES": ["WAR", "MNK", "ROG"],
    "HYBRIDS": ["PAL", "RNG", "SHD", "BRD", "BST"],
    "PRIESTS": ["CLR", "DRU", "SHM"],
}

BROKEN = {
    "Celestial Regeneration",
    "Channeling Focus",
    "Extended Notes",
    "Frenzied Burnout",
    "Jam Fest",
    "Hobble of Spirits",
    "Poison Mastery",
    "Spell Casting Deftness",
    "Quick Buff",
    "Fleet of Foot",
}

BROKEN_WHY = {
    "Celestial Regeneration": "Single target, not group. The timer shows 15 minutes but the real reuse is 72 minutes.",
    "Channeling Focus": "Does nothing for Bards. Bards do not channel.",
    "Extended Notes": "Only beneficial group songs. AE resists, Lceas, PBAoE dots, and snares are unchanged.",
    "Frenzied Burnout": "Does not stack with Ancient: Burnout Blaze. The AA's 15% haste overwrites the 80% pet haste.",
    "Jam Fest": "Only the Bard gets the higher singing level. The group does not.",
    "Hobble of Spirits": "Snare caps at 40% and often fails to stop high-level runners. Also blocks some pet procs such as Spirit of Snow.",
    "Poison Mastery": "You can still fail poison application. The other rank bonuses still work.",
    "Spell Casting Deftness": "Redundant with Quick Buff and foci. Spell haste is capped at 50% server-side.",
    "Quick Buff": "Redundant with Spell Casting Deftness and foci. Spell haste is capped at 50% server-side.",
    "Fleet of Foot": "Was refunded. Everyone has FoF 3 for free and bards cannot buy it.",
}

SECTIONS = {
    "General AA's": ("luclin", "Luclin", "general-aas", "General"),
    "Archetype AA's": ("luclin", "Luclin", "archetype-aas", "Archetype"),
    "Class AA's": ("luclin", "Luclin", "class-aas", "Class"),
    "PoP Advance AA's": ("pop", "Planes of Power", "pop-advance-aas", "PoP Advance"),
    "PoP Ability AA's": ("pop", "Planes of Power", "pop-ability-aas", "PoP Ability"),
}

SKIP_CELLS = {
    "Name",
    "Classes",
    "---",
    "Alt Activate #",
    "Ability Name (Classes)",
}


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def split_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [cell.strip() for cell in line.split("|")]


def parse_name_cell(cell: str) -> tuple[str, str, bool, str]:
    broken = bool(re.search(r"\[\[[^\]]+\]\]\(/baa/?\)", cell, re.I))
    cell = re.sub(r"\[\[[^\]]+\]\]\(/baa/?\)", "", cell).strip()
    match = re.match(r"\[([^\]]+)\]\(([^)]+)\)(.*)$", cell)
    if match:
        name = match.group(1).strip()
        url = match.group(2).strip()
        note = match.group(3).strip().strip("*").strip()
        return name, url, broken, note
    return cell.strip(), "", broken, ""


def parse_classes(cell: str) -> list[str]:
    raw = re.sub(r"\s+", " ", cell).strip()
    if not raw:
        return ["ALL"]

    upper = raw.upper()
    if upper in GROUPS:
        classes = list(GROUPS[upper])
    else:
        classes = []
        remaining = upper
        for group_name in sorted(GROUPS, key=len, reverse=True):
            if group_name == "ALL":
                continue
            if remaining == group_name or remaining.startswith(group_name + " "):
                classes.extend(GROUPS[group_name])
                remaining = remaining[len(group_name) :].strip()
                break
        if remaining:
            for token in remaining.split():
                token = token.strip(",")
                if token == "BER":
                    continue
                if token in CLASS_SET and token not in classes:
                    classes.append(token)
                elif token == "ALL":
                    return ["ALL"]
        if not classes and upper == "ALL":
            return ["ALL"]

    ordered = [name for name in CLASS_ORDER if name in classes]
    if ordered == CLASS_ORDER:
        return ["ALL"]
    return ordered


def parse_abilities(lines: list[str]) -> dict[str, list[dict]]:
    expansions: dict[str, dict] = {}
    current = None

    for line in lines:
        heading = re.match(r"^#\s+(.+?)\s*$", line)
        if heading:
            title = heading.group(1).strip()
            current = SECTIONS.get(title)
            continue
        if not current or not line.startswith("|"):
            continue

        cells = split_row(line)
        if len(cells) < 5:
            continue
        if "Collapse" in cells[0] or cells[0] in SKIP_CELLS or set(cells[0]) <= {"-"}:
            continue

        name, url, marked_broken, note = parse_name_cell(cells[0])
        if not name:
            continue

        expansion_id, expansion_name, group_id, group_name = current
        classes = parse_classes(cells[1])
        broken = marked_broken or name in BROKEN
        ability = {
            "id": f"{group_id}-{slug(name)}",
            "name": name,
            "url": url,
            "note": note,
            "broken": broken,
            "broken_why": BROKEN_WHY.get(name, "") if broken else "",
            "classes": classes,
            "ranks": cells[2],
            "cost": cells[3],
            "description": cells[4],
            "activate": cells[5] if len(cells) > 5 else "",
            "search": " ".join(
                [
                    name,
                    note,
                    BROKEN_WHY.get(name, "") if broken else "",
                    " ".join(classes),
                    cells[1],
                    cells[2],
                    cells[3],
                    cells[4],
                    cells[5] if len(cells) > 5 else "",
                ]
            ).lower(),
        }

        bucket = expansions.setdefault(
            expansion_id,
            {"id": expansion_id, "name": expansion_name, "groups": {}},
        )
        group = bucket["groups"].setdefault(group_id, {"id": group_id, "name": group_name, "abilities": []})
        group["abilities"].append(ability)

    return expansions


def parse_activates(lines: list[str]) -> list[dict]:
    activates = []
    in_table = False
    for line in lines:
        if line.startswith("# ") and "Alt Activate" in line:
            in_table = True
            continue
        if not in_table or not line.startswith("|"):
            continue
        cells = split_row(line)
        if len(cells) < 2 or cells[0] in SKIP_CELLS or set(cells[0]) <= {"-"}:
            continue
        label = cells[1]
        name = re.sub(r"\s*\([^)]*\)\s*$", "", label).strip()
        classes_label = ""
        match = re.search(r"\(([^)]*)\)\s*$", label)
        if match:
            classes_label = match.group(1).strip()
        activates.append(
            {
                "code": cells[0],
                "name": name,
                "classes_label": classes_label,
                "search": f"{cells[0]} {label}".lower(),
            }
        )
    return activates


def main() -> None:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    expansions = parse_abilities(lines)
    catalog = {
        "classes": CLASS_ORDER,
        "expansions": [
            {
                "id": expansion["id"],
                "name": expansion["name"],
                "groups": list(expansion["groups"].values()),
            }
            for expansion in expansions.values()
        ],
        "activates": parse_activates(lines),
    }
    OUT.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    counts = {
        expansion["name"]: sum(len(group["abilities"]) for group in expansion["groups"])
        for expansion in catalog["expansions"]
    }
    print(json.dumps({"abilities": counts, "activates": len(catalog["activates"])}, indent=2))


if __name__ == "__main__":
    main()
