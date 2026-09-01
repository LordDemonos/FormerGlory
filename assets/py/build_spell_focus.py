"""Convert focus.md into _data/spell_focus.json and enrich items from PQDI."""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FOCUS_MD = Path(__file__).resolve().parent / "focus_source.md"
OUT = ROOT / "_data" / "spell_focus.json"
CACHE = Path(r"E:\JavaScript\formerglory\.cache\pqdi-items")
UA = "FormerGlory-focus-guide/1.0 (+https://formerglory.lol/focus)"

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

FAMILY_META = {
    "All Spell Duration Focus Effects": {
        "id": "all-duration",
        "name": "All Duration",
        "applies": "all",
    },
    "Buff Spell Duration Focus Effects": {
        "id": "buff-duration",
        "name": "Buff Duration",
        "applies": "beneficial",
    },
    "Detrimental Spell Duration Focus Effects": {
        "id": "dot-duration",
        "name": "DoT Duration",
        "applies": "detrimental",
    },
    "Healing Spell Enhancement Focus Effects": {
        "id": "healing",
        "name": "Healing",
        "applies": "beneficial",
    },
    "Spell Aggro Reduction Focus Effects": {
        "id": "aggro",
        "name": "Aggro",
        "applies": "all",
    },
    "Spell Damage Focus Effects": {
        "id": "damage",
        "name": "Damage",
        "applies": "detrimental",
    },
    "Spell Haste Focus Effects": {
        "id": "haste",
        "name": "Haste",
        "applies": "all",
    },
    "Spell Mana Efficiency Focus Effects": {
        "id": "mana",
        "name": "Mana",
        "applies": "all",
    },
    "Spell Range Extension Focus Effects": {
        "id": "range",
        "name": "Range",
        "applies": "all",
    },
    "Spell Reagent Conservation Focus Effects": {
        "id": "reagent",
        "name": "Reagent",
        "applies": "all",
    },
}

SLOT_MAP = {
    "HEAD": "HEAD",
    "FACE": "FACE",
    "EAR": "EAR",
    "EARS": "EAR",
    "NECK": "NECK",
    "SHOULDERS": "SHOULDERS",
    "ARMS": "ARMS",
    "BACK": "BACK",
    "WRIST": "WRIST",
    "WRISTS": "WRIST",
    "HANDS": "HANDS",
    "CHEST": "CHEST",
    "LEGS": "LEGS",
    "FEET": "FEET",
    "WAIST": "WAIST",
    "FINGER": "FINGER",
    "FINGERS": "FINGER",
    "PRIMARY": "PRIMARY",
    "SECONDARY": "SECONDARY",
    "RANGE": "RANGE",
    "AMMO": "AMMO",
    "CHARM": "CHARM",
}

SLOT_ORDER = [
    "HEAD",
    "FACE",
    "EAR",
    "NECK",
    "SHOULDERS",
    "ARMS",
    "BACK",
    "WRIST",
    "HANDS",
    "CHEST",
    "LEGS",
    "FEET",
    "WAIST",
    "FINGER",
    "PRIMARY",
    "SECONDARY",
    "RANGE",
    "AMMO",
    "CHARM",
]

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
SPELL_ID_RE = re.compile(r"pqdi\.cc/spell/(\d+)", re.I)
ITEM_ID_RE = re.compile(r"pqdi\.cc/item/(\d+)", re.I)
MAX_LV_RE = re.compile(r"Max Lv\s*(\d+)", re.I)
SLUG_RE = re.compile(r"[^a-z0-9]+")
CLASSES_RE = re.compile(r"Classes:\s*([A-Z][A-Z0-9 /]*)", re.I)
SLOT_RE = re.compile(r"Slot:\s*([A-Za-z /]+)")
ELEMENT_RE = re.compile(
    r"(?:Resist:\s*|(?:^|[,(]\s*))(Fire|Cold|Magic|Disease|Poison)(?:\s+allowed)?",
    re.I,
)


def slugify(text: str) -> str:
    value = SLUG_RE.sub("-", text.lower()).strip("-")
    return value or "focus"


def strip_md(text: str) -> str:
    text = LINK_RE.sub(r"\1", text)
    text = re.sub(r"[*`_]+", "", text)
    return re.sub(r"\s+", " ", text).strip(" |")


def parse_links(cell: str) -> list[dict]:
    links = [{"name": name.strip(), "url": url.strip()} for name, url in LINK_RE.findall(cell)]
    leftover = strip_md(cell)
    if leftover and not links:
        links.append({"name": leftover, "url": ""})
    return links


def split_cells(line: str) -> list[str]:
    raw = line.strip()
    if raw.startswith("|"):
        raw = raw[1:]
    if raw.endswith("|"):
        raw = raw[:-1]
    return [cell.strip() for cell in raw.split("|")]


def parse_applies(family_applies: str, description: str) -> str:
    text = description.lower()
    if "beneficial only" in text or "buff spell" in text:
        return "beneficial"
    if "detrimental only" in text:
        return "detrimental"
    return family_applies


def parse_element(description: str) -> str:
    match = ELEMENT_RE.search(description)
    if not match:
        return ""
    return match.group(1).capitalize()


def parse_classes(blob: str) -> list[str]:
    match = CLASSES_RE.search(blob)
    if not match:
        return ["ALL"]
    token = re.sub(r"\s+", " ", match.group(1)).strip().upper()
    if token == "ALL":
        return ["ALL"]
    classes = [part for part in token.split(" ") if part in CLASS_SET]
    return classes or ["ALL"]


def parse_slots(blob: str) -> list[str]:
    match = SLOT_RE.search(blob)
    if not match:
        return []
    found: list[str] = []
    for part in re.split(r"[ /]+", match.group(1).upper()):
        mapped = SLOT_MAP.get(part)
        if mapped and mapped not in found:
            found.append(mapped)
    return found


def unique_slug(base: str, used: set[str]) -> str:
    slug = base
    n = 2
    while slug in used:
        slug = f"{base}-{n}"
        n += 1
    used.add(slug)
    return slug


def parse_markdown(text: str) -> list[dict]:
    families: list[dict] = []
    family = None
    effect = None
    rank = None
    desc_lines: list[str] = []
    used_ids: set[str] = set()
    in_table = False

    def flush_desc() -> None:
        nonlocal desc_lines, effect
        if effect is not None and not effect.get("description"):
            cleaned = strip_md(" ".join(desc_lines))
            cleaned = re.sub(r"^effect type[\s\xa0]*:\s*", "", cleaned, flags=re.I)
            effect["description"] = cleaned
        desc_lines = []

    def start_rank(name: str, spell_id: int | None) -> None:
        nonlocal rank, effect
        if effect is None:
            return
        flush_desc()
        if spell_id:
            rank_id = unique_slug(f"{effect['id']}-{spell_id}", used_ids)
        else:
            rank_id = unique_slug(f"{effect['id']}-rank", used_ids)
        rank = {
            "id": rank_id,
            "name": name,
            "spell_id": spell_id,
            "max_level": int(MAX_LV_RE.search(name).group(1)) if MAX_LV_RE.search(name) else 65,
            "items": [],
        }
        effect["ranks"].append(rank)

    lines = text.splitlines()
    started = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# ") and stripped[2:] in FAMILY_META:
            started = True
            flush_desc()
            meta = FAMILY_META[stripped[2:]]
            family = {
                "id": meta["id"],
                "name": meta["name"],
                "applies": meta["applies"],
                "effects": [],
            }
            families.append(family)
            effect = None
            rank = None
            in_table = False
            continue
        if not started or family is None:
            continue
        if stripped.startswith("## "):
            flush_desc()
            name = strip_md(stripped[3:])
            effect = {
                "id": unique_slug(slugify(name), used_ids),
                "name": name,
                "description": "",
                "ranks": [],
            }
            family["effects"].append(effect)
            rank = None
            in_table = False
            continue
        if stripped.startswith("|"):
            cells = split_cells(stripped)
            if not cells or set("".join(cells)) <= {"-", " "}:
                in_table = True
                continue
            first = cells[0]
            if first.lower() == "name":
                in_table = True
                continue
            spell_match = SPELL_ID_RE.search(first)
            if spell_match:
                start_rank(strip_md(first), int(spell_match.group(1)))
                in_table = True
                continue
            if effect is None:
                continue
            if rank is None:
                start_rank(effect["name"], None)
            item_match = ITEM_ID_RE.search(first)
            item_links = parse_links(first)
            zone_cell = cells[1] if len(cells) > 1 else ""
            source_cell = cells[2] if len(cells) > 2 else ""
            name = item_links[0]["name"] if item_links else strip_md(first)
            if not name:
                continue
            rank["items"].append(
                {
                    "id": int(item_match.group(1)) if item_match else 0,
                    "name": name,
                    "url": item_links[0]["url"] if item_links else "",
                    "zone": strip_md(zone_cell),
                    "sources": [link["name"] for link in parse_links(source_cell)] or ([strip_md(source_cell)] if strip_md(source_cell) else []),
                    "classes": ["ALL"],
                    "slots": [],
                }
            )
            in_table = True
            continue
        if stripped.startswith("---") or stripped.startswith("#"):
            continue
        if stripped and not in_table:
            desc_lines.append(stripped)

    flush_desc()
    for fam in families:
        for effect in fam["effects"]:
            applies = parse_applies(fam["applies"], effect["description"])
            element = parse_element(effect["description"])
            effect["applies"] = applies
            effect["element"] = element
            for rank in effect["ranks"]:
                rank["applies"] = parse_applies(applies, rank["name"])
                rank["element"] = element
    return families


def fetch_item_html(item_id: int) -> str:
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{item_id}.html"
    if path.exists() and path.stat().st_size > 200:
        return path.read_text(encoding="utf-8", errors="replace")
    url = f"https://www.pqdi.cc/item/{item_id}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    path.write_text(body, encoding="utf-8")
    return body


def html_to_text(html: str) -> str:
    html = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    html = re.sub(r"<style[\s\S]*?</style>", " ", html, flags=re.I)
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    html = re.sub(r"</(p|div|tr|h1|h2|li)>", "\n", html, flags=re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"[ \t]+", " ", html)


def enrich_items(families: list[dict]) -> None:
    ids: list[int] = []
    seen: set[int] = set()
    for fam in families:
        for effect in fam["effects"]:
            for rank in effect["ranks"]:
                for item in rank["items"]:
                    item_id = item.get("id") or 0
                    if item_id and item_id not in seen:
                        seen.add(item_id)
                        ids.append(item_id)

    details: dict[int, dict] = {}
    with ThreadPoolExecutor(max_workers=6) as pool:
        futs = {pool.submit(fetch_item_html, item_id): item_id for item_id in ids}
        for fut in as_completed(futs):
            item_id = futs[fut]
            try:
                text = html_to_text(fut.result())
                details[item_id] = {
                    "classes": parse_classes(text),
                    "slots": parse_slots(text),
                }
                print(item_id, "OK", " ".join(details[item_id]["classes"]), "/".join(details[item_id]["slots"]))
            except Exception as err:
                print(item_id, "ERR", err)
                time.sleep(0.4)

    for fam in families:
        for effect in fam["effects"]:
            for rank in effect["ranks"]:
                for item in rank["items"]:
                    info = details.get(item.get("id") or 0)
                    if not info:
                        continue
                    item["classes"] = info["classes"]
                    item["slots"] = info["slots"]


ZONE_ALIASES = (
    (re.compile(r"^the plane of tranquility$", re.I), "Plane of Tranquility"),
    (re.compile(r"^plane of tranquility$", re.I), "Plane of Tranquility"),
    (re.compile(r"^the plane of knowledge$", re.I), "Plane of Knowledge"),
    (re.compile(r"^plane of knowledge$", re.I), "Plane of Knowledge"),
    (re.compile(r"^the plane of time:? phase 2$", re.I), "Plane of Time Phase 2"),
    (re.compile(r"^plane of time phase 2$", re.I), "Plane of Time Phase 2"),
    (re.compile(r"^drunder, fortress of zek(?: \(plane of tactics\))?$", re.I), "Drunder, the Fortress of Zek"),
    (re.compile(r"^drunder, the fortress of zek$", re.I), "Drunder, the Fortress of Zek"),
)


def canonicalize_zone(zone: str) -> str:
    text = (zone or "").strip()
    if not text:
        return ""
    for pattern, canonical in ZONE_ALIASES:
        if pattern.match(text):
            return canonical
    return text


def normalize_zones(families: list[dict]) -> None:
    for fam in families:
        for effect in fam["effects"]:
            for rank in effect["ranks"]:
                for item in rank["items"]:
                    item["zone"] = canonicalize_zone(item.get("zone") or "")


def attach_search(families: list[dict]) -> None:
    for fam in families:
        for effect in fam["effects"]:
            for rank in effect["ranks"]:
                for item in rank["items"]:
                    item["applies"] = rank.get("applies") or effect.get("applies") or fam["applies"]
                    item["element"] = rank.get("element") or effect.get("element") or ""
                    item["max_level"] = rank.get("max_level") or 65
                    parts = [
                        fam["name"],
                        effect["name"],
                        effect.get("description") or "",
                        rank["name"],
                        item["name"],
                        item.get("zone") or "",
                        " ".join(item.get("sources") or []),
                        " ".join(item.get("slots") or []),
                        " ".join(item.get("classes") or []),
                        item.get("applies") or "",
                        item.get("element") or "",
                    ]
                    item["search"] = " ".join(parts).lower()


EXPANSIONS = [
    {"id": "classic", "name": "Classic"},
    {"id": "kunark", "name": "Kunark"},
    {"id": "velious", "name": "Velious"},
    {"id": "luclin", "name": "Luclin"},
    {"id": "pop", "name": "Planes of Power"},
]
EXPANSION_ORDER = [item["id"] for item in EXPANSIONS]
EXPANSION_KEYWORDS = {
    "pop": [
        "plane of time",
        "plane of tranquility",
        "plane of knowledge",
        "plane of innovation",
        "tower of solusek",
        "doomfire",
        "eryslai",
        "kingdom of wind",
        "plane of fire",
        "plane of storms",
        "plane of water",
        "vegarlson",
        "earthen badlands",
        "bastion of thunder",
        "torden",
        "ragrax",
        "drunder",
        "fortress of zek",
        "potactics",
        "plane of air",
        "halls of honor",
        "plane of disease",
        "plane of justice",
        "plane of nightmare",
        "plane of valor",
        "torment",
        "plane of pain",
        "crypt of decay",
        "lxanvom",
        "coirnav",
        "terris thule",
        "temple of marr",
        "plane of earth",
        "pottery",
        "blacksmithing",
        "tailoring",
        "jewelry making",
        "spell research",
        "spell: summon",
        "bor warhammer",
    ],
    "luclin": [
        "vex thal",
        "ssraeshza",
        "fungus grove",
        "echo caverns",
        "katta",
        "grieg",
        "sanctus seru",
        "bazaar",
        "akheva",
        "umbral",
        "the deep",
        "dawnshroud",
        "scarlet desert",
        "shadeweaver",
        "hollowshade",
        "paludal",
        "tenebral",
        "maiden",
        "acrylia",
        "grimling",
        "netherbian",
        "twilight",
    ],
    "velious": [
        "temple of veeshan",
        "kael",
        "skyshrine",
        "velketor",
        "dragon necropolis",
        "icewell",
        "sleeper",
        "kerafyrm",
        "great divide",
        "western wastes",
        "cobaltscar",
        "wakening",
        "iceclad",
        "frozen shadow",
        "siren",
        "thurgadin",
        "western waste",
    ],
    "kunark": [
        "chardok",
        "howling stones",
        "sebilis",
        "frontier mountains",
        "timorous",
        "veeshan's peak",
        "dreadlands",
        "emerald jungle",
        "skyfire",
        "burning wood",
        "karnor",
        "droga",
        "trakanon",
        "field of bone",
        "kaesora",
        "kurn",
        "overthere",
        "firiona",
        "nurga",
        "warsliks",
        "city of mist",
        "lake of ill omen",
        "swamp of no hope",
        "dreadlands",
    ],
}


def expansion_for_zone(zone: str) -> str:
    text = (zone or "").lower()
    matched = "classic"
    for exp_id in EXPANSION_ORDER:
        keywords = EXPANSION_KEYWORDS.get(exp_id) or []
        if any(keyword in text for keyword in keywords):
            matched = exp_id
    return matched


def group_by_expansion(families: list[dict]) -> list[dict]:
    expansions = []
    for meta in EXPANSIONS:
        exp_families = []
        for family in families:
            effects = []
            for effect in family["effects"]:
                ranks = []
                for rank in effect["ranks"]:
                    items = [
                        item
                        for item in rank["items"]
                        if expansion_for_zone(item.get("zone") or "") == meta["id"]
                    ]
                    if items:
                        ranks.append({**rank, "id": f"{meta['id']}-{rank['id']}", "items": items})
                if ranks:
                    effects.append({**effect, "id": f"{meta['id']}-{effect['id']}", "ranks": ranks})
            if effects:
                exp_families.append(
                    {
                        **family,
                        "id": f"{meta['id']}-{family['id']}",
                        "key": family["id"],
                        "effects": effects,
                    }
                )
        expansions.append({**meta, "families": exp_families})
    return expansions


def collect_slots(families: list[dict]) -> list[str]:
    found: set[str] = set()
    for fam in families:
        for effect in fam["effects"]:
            for rank in effect["ranks"]:
                for item in rank["items"]:
                    found.update(item.get("slots") or [])
    return [slot for slot in SLOT_ORDER if slot in found]


def main() -> None:
    if "--from-json" in sys.argv:
        payload = json.loads(OUT.read_text(encoding="utf-8"))
        normalize_zones(payload["families"])
        attach_search(payload["families"])
        payload["family_filters"] = [{"id": fam["id"], "name": fam["name"]} for fam in payload["families"]]
        payload["expansions"] = group_by_expansion(payload["families"])
        OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote expansions for {len(payload['expansions'])} expansions")
        return

    families = parse_markdown(FOCUS_MD.read_text(encoding="utf-8"))
    enrich_items(families)
    normalize_zones(families)
    attach_search(families)
    payload = {
        "classes": CLASS_ORDER,
        "slots": collect_slots(families),
        "levels": [20, 44, 60, 65],
        "families": families,
        "family_filters": [{"id": fam["id"], "name": fam["name"]} for fam in families],
        "expansions": group_by_expansion(families),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    items = sum(
        len(rank["items"])
        for fam in families
        for effect in fam["effects"]
        for rank in effect["ranks"]
    )
    print(f"wrote {OUT} families={len(families)} items={items}")


if __name__ == "__main__":
    main()
