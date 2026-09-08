"""Attach PQDI loot-table ids, names, and chances to raid_loot.json."""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from collections import defaultdict
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "_data" / "raid_loot.json"
CACHE_DIR = Path.home() / "AppData" / "Local" / "Temp" / "fg-pqdi-npc"
USER_AGENT = "FormerGloryLootEnricher/1.0 (+https://formerglory.lol)"

CARD_SPLIT = re.compile(r'<div class="card mb-4">')
HEADER_RE = re.compile(r"\(id:\s*(\d+)\)\s*([^<]+)", re.S)
PROB_RE = re.compile(
    r"With a probability of\s+([\d.]+)%.*?-\s*(\d+)\s+to\s+(\d+)\s+drops",
    re.S,
)
ITEM_RE = re.compile(
    r'href="/item/(\d+)"[^>]*>([^<]+)</a>\s*([\d.]+)%\s*\(([\d.]+)%\s*Global\)',
    re.S,
)
INDEPENDENT_MARK = "rolled for drop independently"


def pretty_pct(value: float) -> float | int:
    if abs(value - round(value)) < 0.05:
        return int(round(value))
    return round(value, 1)


def drop_summary(prob: float, min_drops: int, max_drops: int) -> str:
    if min_drops == max_drops:
        drop = "1 drop" if min_drops == 1 else f"{min_drops} drops"
    else:
        drop = f"{min_drops} to {max_drops} drops"
    return f"{pretty_pct(prob)}% · {drop}"


def clean_label(name: str) -> str:
    name = unescape(name).strip()
    name = re.sub(r"^\d+_?", "", name)
    return re.sub(r"_+", " ", name).strip(" _")


def parse_tables(html: str) -> list[dict]:
    tables = []
    for card in CARD_SPLIT.split(html)[1:]:
        header = HEADER_RE.search(card)
        prob = PROB_RE.search(card)
        if not header or not prob:
            continue
        items = []
        for match in ITEM_RE.finditer(card):
            items.append(
                {
                    "id": int(match.group(1)),
                    "name": unescape(match.group(2)).strip(),
                    "table_chance": float(match.group(3)),
                    "chance": float(match.group(4)),
                }
            )
        if not items:
            continue
        tables.append(
            {
                "id": header.group(1),
                "label": clean_label(header.group(2)),
                "summary": drop_summary(
                    float(prob.group(1)),
                    int(prob.group(2)),
                    int(prob.group(3)),
                ),
                "independent": INDEPENDENT_MARK in card,
                "items": items,
            }
        )
    return tables


def fetch_npc(npc_id: int) -> str:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / f"{npc_id}.html"
    if cache_path.exists() and cache_path.stat().st_size > 1000:
        return cache_path.read_text(encoding="utf-8", errors="replace")

    url = f"https://www.pqdi.cc/npc/{npc_id}"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                html = response.read().decode("utf-8", "replace")
            cache_path.write_text(html, encoding="utf-8")
            time.sleep(0.12)
            return html
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            last_error = error
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"failed to fetch {url}: {last_error}")


def item_payload(item: dict, table_chance: float | int | None = None) -> dict:
    payload = {
        "id": item["id"],
        "name": item["name"],
        "chance": item["chance"],
        "classes": item.get("classes", []),
    }
    if table_chance is not None:
        payload["table_chance"] = table_chance
    elif "table_chance" in item:
        payload["table_chance"] = item["table_chance"]
    for key in ("lore", "nodrop", "kind", "retired"):
        if key in item:
            payload[key] = item[key]
    return payload


def best_match(item: dict, occurrences: list[tuple[dict, dict]]) -> tuple[dict, dict] | None:
    if not occurrences:
        return None
    if len(occurrences) == 1:
        return occurrences[0]
    target = float(item.get("chance") or 0)
    return min(occurrences, key=lambda pair: abs(pair[1]["chance"] - target))


def enrich_boss(boss: dict, pqdi_tables: list[dict]) -> tuple[list[dict], list[str]]:
    by_item: dict[int, list[tuple[dict, dict]]] = defaultdict(list)
    for table in pqdi_tables:
        for pqdi_item in table["items"]:
            by_item[pqdi_item["id"]].append((table, pqdi_item))

    grouped: dict[str, dict] = {}
    leftovers: dict[str, dict] = {}
    unmatched_names: list[str] = []
    orig_counts: dict[str, int] = {}

    order = 0
    for orig_table in boss.get("tables", []):
        orig_key = str(orig_table.get("id"))
        orig_counts[orig_key] = len(orig_table.get("items", []))
        for item in orig_table.get("items", []):
            match = best_match(item, by_item.get(item["id"], []))
            if match is None:
                unmatched_names.append(f"{item['name']} ({item['id']})")
                bucket = leftovers.setdefault(
                    orig_key,
                    {
                        "order": order,
                        "id": orig_table.get("id"),
                        "label": orig_table.get("label"),
                        "summary": orig_table.get("summary"),
                        "independent": bool(orig_table.get("independent")),
                        "items": [],
                    },
                )
                bucket["items"].append(item_payload(item))
                order += 1
                continue

            table, pqdi_item = match
            bucket = grouped.setdefault(
                table["id"],
                {
                    "order": order,
                    "id": table["id"],
                    "label": table["label"],
                    "summary": table["summary"],
                    "independent": table["independent"],
                    "items": [],
                },
            )
            bucket["items"].append(item_payload(item, pretty_pct(pqdi_item["table_chance"])))
            order += 1

    for key, bucket in leftovers.items():
        chances = {item.get("chance") for item in bucket["items"]}
        if not str(bucket["id"]).isdigit() and chances == {100}:
            bucket["summary"] = "100%"
        elif len(bucket["items"]) != orig_counts.get(key, 0) and len(chances) == 1:
            chance = next(iter(chances))
            bucket["summary"] = f"{pretty_pct(float(chance))}%"

    tables = sorted(grouped.values(), key=lambda table: table["order"])
    tables.extend(sorted(leftovers.values(), key=lambda table: table["order"]))
    for table in tables:
        table.pop("order", None)
        if not table.get("independent"):
            table.pop("independent", None)
    return tables, unmatched_names


def iter_bosses(catalog: dict):
    for expansion in catalog.get("expansions", []):
        for zone in expansion.get("zones", []):
            for boss in zone.get("bosses", []):
                yield expansion, zone, boss


def main() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    bosses = list(iter_bosses(catalog))
    unique_ids = sorted({boss["npc_id"] for _, _, boss in bosses})
    parsed: dict[int, list[dict]] = {}
    failures: list[str] = []

    print(f"Fetching {len(unique_ids)} NPC pages ({len(bosses)} bosses)")
    for index, npc_id in enumerate(unique_ids, start=1):
        try:
            html = fetch_npc(npc_id)
            parsed[npc_id] = parse_tables(html)
            print(f"[{index}/{len(unique_ids)}] {npc_id} {len(parsed[npc_id])} tables")
        except Exception as error:  # noqa: BLE001 - keep going across NPCs
            failures.append(f"{npc_id}: {error}")
            print(f"[{index}/{len(unique_ids)}] {npc_id} FAIL {error}")

    updated = 0
    unmatched_bosses: list[str] = []
    numeric_tables = 0
    for _, _, boss in bosses:
        tables = parsed.get(boss["npc_id"])
        if not tables:
            continue
        new_tables, unmatched = enrich_boss(boss, tables)
        if not new_tables:
            continue
        boss["tables"] = new_tables
        updated += 1
        numeric_tables += sum(1 for table in new_tables if str(table["id"]).isdigit())
        if unmatched:
            unmatched_bosses.append(f"{boss['name']}: {', '.join(unmatched)}")

    CATALOG.write_text(json.dumps(catalog, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"Updated {updated}/{len(bosses)} bosses")
    print(f"Numeric tables: {numeric_tables}")
    if failures:
        print("Fetch failures:")
        for line in failures:
            print(f"  {line}")
    if unmatched_bosses:
        print(f"Unmatched catalog items on {len(unmatched_bosses)} bosses:")
        for line in unmatched_bosses:
            print(f"  {line}")


if __name__ == "__main__":
    main()
