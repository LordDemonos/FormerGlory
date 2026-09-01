"""PQDI → Former Glory Respawn Time sync.

Walks strategy.md boss cards, skips event-guide / overview / flagging cards,
reads PQDI /instances then the NPC page, and rewrites the lockout box when
the guide disagrees. Event-only names stay "Event spawn" unless /instances
has an override. Do not invent hours.
"""
from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = REPO_ROOT / "strategy.md"
STRATEGY_DIR = REPO_ROOT / "strategy"
UA = "FormerGlory-lockout-sync/1.0 (raid lockouts; +https://github.com/LordDemonos/FormerGlory)"
INSTANCES_URL = "https://www.pqdi.cc/instances"
NPC_URL = "https://www.pqdi.cc/npc/{npc_id}"

EVENT_ONLY_SLUGS = frozenset(
    {
        "xanamech_nezmirthafen",
        "a_construct_of_nightmares",
        "avhi_escron",
        "bishop_toluwon",
        "raex_pwodill",
        "vindor_mawnil",
        "high_priest_ultor_szanvon",
        "neimon_of_air",
        "terlok_of_earth",
        "kazrok_of_fire",
        "anar_of_water",
        "rythor_of_the_undead",
        "windshapen_warlord_of_air",
        "earthen_overseer",
        "gutripping_war_beast",
        "war_shapen_emissary",
        "ralthos_enrok",
        "avatar_of_the_elements",
        "supernatural_guardian",
    }
)

# Keep existing Event spawn wording unless /instances later has a real timer.
PRESERVE_EVENT_SPAWN_SLUGS = EVENT_ONLY_SLUGS | frozenset(
    {
        "gallows_master_teion",
        "punisher_veshtaq",
        "lashman_azakal",
        "prime_executioner_vathoch",
        "punisher_of_flame",
        "yurae_zhaleem",
        "falto_lord_of_thunder",
        "ston_ruak_ancient_of_the_trees",
    }
)

SKIP_SECOND_LI = frozenset({"Event Guide", "Flagging Guide"})
RESPAWN_RE = re.compile(
    r'(<div class="info-lockoutitem"><strong>Respawn Time:</strong>\s*)([^<]+)(</div>)',
    re.I,
)
NPC_LINK_RE = re.compile(
    r'href="https://www\.pqdi\.cc/npc/(\d+)"[^>]*title="View NPC on PQDI"',
    re.I,
)
NPC_LINK_ANY_RE = re.compile(r'href="https://www\.pqdi\.cc/npc/(\d+)"', re.I)
ZONE_RE = re.compile(
    r'<strong>Zone:</strong>\s*<a href="[^"]+"[^>]*>([^<]+)</a>',
    re.I,
)
TITLE_RE = re.compile(r"^title:\s*(.+)$", re.M)
H4_ZONE_RE = re.compile(
    r'<h4><a href="https://www\.pqdi\.cc/zone/\d+"[^>]*>([^<]+)</a></h4>',
    re.I,
)
INSTANCES_ITEM_RE = re.compile(
    r"<li class=\"list-group-item\">\s*"
    r"<a href=['\"]/npc/(\d+)['\"][^>]*>\s*([^<]+?)\s*</a>"
    r".*?Respawn Time:\s*([^<]+?)\s*</small>",
    re.I | re.S,
)
QUICK_TIMER_RE = re.compile(
    r"Instance Spawn Timer:\s*(?:<br\s*/?>)?\s*([^<]+)",
    re.I,
)
OVERRIDE_MS_RE = re.compile(
    r"instance_spawn_timer_override:\s*</strong>\s*"
    r"<span class=\"text-wrap\">\s*(\d+)\s*</span>",
    re.I,
)
DURATION_PART_RE = re.compile(
    r"(\d+)\s*(weeks?|days?|hours?|minutes?|seconds?)",
    re.I,
)

UNIT_SECONDS = {
    "week": 7 * 86400,
    "weeks": 7 * 86400,
    "day": 86400,
    "days": 86400,
    "hour": 3600,
    "hours": 3600,
    "minute": 60,
    "minutes": 60,
    "second": 1,
    "seconds": 1,
}


@dataclass
class BossCard:
    slug: str
    link_text: str
    zone: str
    note: str | None
    skip_reason: str | None = None


@dataclass
class BossPage:
    slug: str
    title: str
    name: str
    note: str | None
    zone: str | None
    npc_id: str | None
    respawn_text: str | None
    path: Path | None = None
    raw: str = ""


@dataclass
class TimerHit:
    text: str
    source: str  # instances | npc | event-allowlist


@dataclass
class Change:
    slug: str
    old: str
    new: str
    source: str


@dataclass
class SyncReport:
    scanned: int = 0
    skipped_cards: list[str] = field(default_factory=list)
    changes: list[Change] = field(default_factory=list)
    event_only_forced: list[str] = field(default_factory=list)
    event_only_preserved: list[str] = field(default_factory=list)
    missing_lockout: list[str] = field(default_factory=list)
    missing_npc: list[str] = field(default_factory=list)
    missing_timer: list[str] = field(default_factory=list)
    unchanged: int = 0

    def to_markdown(self) -> str:
        lines = [
            "## Lockout sync",
            "",
            f"Scanned **{self.scanned}** boss cards. Unchanged: **{self.unchanged}**.",
            "",
        ]
        if self.changes:
            lines.append("### Updates")
            for change in self.changes:
                lines.append(
                    f"- `{change.slug}`: {change.old} → {change.new} ({change.source})"
                )
            lines.append("")
        else:
            lines.append("No lockout box rewrites.")
            lines.append("")
        def _blk(title: str, rows: list[str]) -> None:
            if not rows:
                return
            lines.append(f"### {title}")
            for row in rows:
                lines.append(f"- `{row}`")
            lines.append("")

        _blk("Event-only forced to Event spawn", self.event_only_forced)
        _blk("Event-only preserved (no /instances override)", self.event_only_preserved)
        _blk("Missing lockout box", self.missing_lockout)
        _blk("Missing NPC link", self.missing_npc)
        _blk("No PQDI timer", self.missing_timer)
        if self.skipped_cards:
            lines.append(f"Skipped index cards: **{len(self.skipped_cards)}**.")
            lines.append("")
        return "\n".join(lines)


def normalize_name(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("`", "'").strip().lower())


def is_event_spawn_token(text: str | None) -> bool:
    if not text:
        return False
    stripped = text.strip().lower()
    return stripped == "spawned" or stripped.startswith("event spawn")


def parse_duration_seconds(text: str | None) -> int | None:
    if not text or is_event_spawn_token(text):
        return None
    parts = DURATION_PART_RE.findall(text)
    if not parts:
        return None
    remainder = DURATION_PART_RE.sub("", text)
    remainder = re.sub(r"\band\b|[,\s]+", "", remainder, flags=re.I)
    if remainder:
        return None
    total = 0
    for amount, unit in parts:
        total += int(amount) * UNIT_SECONDS[unit.lower()]
    return total if total > 0 else None


def format_duration(total_seconds: int) -> str:
    weeks, rem = divmod(total_seconds, 7 * 86400)
    days, rem = divmod(rem, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    parts: list[str] = []
    if weeks:
        parts.append(f"{weeks} week{'s' if weeks != 1 else ''}")
    if days:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    if not parts:
        return "0 seconds"
    if len(parts) == 1:
        return parts[0]
    if len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    return f"{', '.join(parts[:-1])} and {parts[-1]}"


def ms_override_to_seconds(raw_ms: int) -> int | None:
    if raw_ms <= 0:
        return None
    return raw_ms // 1000


def durations_match(left: str | None, right: str | None) -> bool:
    if is_event_spawn_token(left) and is_event_spawn_token(right):
        return True
    left_s = parse_duration_seconds(left)
    right_s = parse_duration_seconds(right)
    if left_s is None or right_s is None:
        if left and right:
            return left.strip().lower() == right.strip().lower()
        return False
    return left_s == right_s


def split_name_and_note(title: str) -> tuple[str, str | None]:
    trimmed = title.strip()
    match = re.search(r"^(.*?)\s*\(([^)]+)\)\s*$", trimmed)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return trimmed, None


def parse_index_cards(index_text: str) -> list[BossCard]:
    cards: list[BossCard] = []
    zone = "Unknown"
    current: list[str] | None = None
    for line in index_text.splitlines():
        zone_match = H4_ZONE_RE.search(line)
        if zone_match:
            zone = zone_match.group(1).strip()
        if '<div class="card dragon">' in line:
            current = [line]
            continue
        if current is not None:
            current.append(line)
            if "</div>" in line:
                cards.append(_card_from_html("\n".join(current), zone))
                current = None
    return cards


def _card_from_html(html: str, zone: str) -> BossCard:
    lis = re.findall(r"<li>(.*?)</li>", html, re.S)
    first = lis[0] if lis else ""
    second = re.sub(r"<[^>]+>", "", lis[1]).strip() if len(lis) > 1 else ""
    slug = None
    link_text = None
    for href, label in re.findall(r'<a href="([^"]+)">([^<]+)</a>', first):
        if href.startswith(("http://", "https://", "/", "#")):
            continue
        slug = href
        link_text = label.strip()
        break
    if not slug or not link_text:
        return BossCard("", "", zone, None, skip_reason="no-slug")
    skip = None
    if second in SKIP_SECOND_LI:
        skip = second
    elif link_text.endswith("Overview"):
        skip = "Overview"
    _, note = split_name_and_note(link_text)
    return BossCard(slug=slug, link_text=link_text, zone=zone, note=note, skip_reason=skip)


def parse_boss_page(slug: str, text: str, path: Path | None = None) -> BossPage:
    title_match = TITLE_RE.search(text)
    title = title_match.group(1).strip() if title_match else slug
    name, note = split_name_and_note(title)
    npc_match = NPC_LINK_RE.search(text) or NPC_LINK_ANY_RE.search(text)
    zone_match = ZONE_RE.search(text)
    respawn_match = RESPAWN_RE.search(text)
    return BossPage(
        slug=slug,
        title=title,
        name=name,
        note=note,
        zone=zone_match.group(1).strip() if zone_match else None,
        npc_id=npc_match.group(1) if npc_match else None,
        respawn_text=respawn_match.group(2).strip() if respawn_match else None,
        path=path,
        raw=text,
    )


def replace_respawn_time(page_text: str, new_text: str) -> str | None:
    if not RESPAWN_RE.search(page_text):
        return None
    return RESPAWN_RE.sub(rf"\g<1>{new_text}\g<3>", page_text, count=1)


def parse_instances_page(html: str) -> dict[str, str]:
    """Map npc_id -> Respawn Time string from /instances."""
    timers: dict[str, str] = {}
    for npc_id, _name, timer in INSTANCES_ITEM_RE.findall(html):
        text = re.sub(r"\s+", " ", timer).strip()
        if npc_id not in timers:
            timers[npc_id] = text
    return timers


def parse_npc_timer(html: str) -> TimerHit | None:
    quick = QUICK_TIMER_RE.search(html)
    if quick:
        text = re.sub(r"\s+", " ", quick.group(1)).strip()
        if text:
            return TimerHit(text=text, source="npc")
    override = OVERRIDE_MS_RE.search(html)
    if override:
        seconds = ms_override_to_seconds(int(override.group(1)))
        if seconds:
            return TimerHit(text=format_duration(seconds), source="npc")
    return None


def fetch_url(url: str, cache_path: Path | None, delay_s: float) -> str:
    if cache_path and cache_path.exists() and cache_path.stat().st_size > 200:
        return cache_path.read_text(encoding="utf-8", errors="replace")
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8", errors="replace")
            if cache_path:
                cache_path.parent.mkdir(parents=True, exist_ok=True)
                cache_path.write_text(body, encoding="utf-8")
            if delay_s:
                time.sleep(delay_s)
            return body
        except urllib.error.HTTPError as err:
            last_error = err
            if err.code in (429, 500, 502, 503, 504) and attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue
            raise
        except urllib.error.URLError as err:
            last_error = err
            if attempt < 2:
                time.sleep(2 * (attempt + 1))
                continue
            raise
    raise RuntimeError(f"Failed to fetch {url}: {last_error}")


def load_boss_page(slug: str, strategy_dir: Path) -> BossPage | None:
    path = strategy_dir / f"{slug}.md"
    if not path.exists():
        return None
    return parse_boss_page(slug, path.read_text(encoding="utf-8"), path)


def desired_timer(
    card: BossCard,
    page: BossPage,
    instances: dict[str, str],
    npc_timer: TimerHit | None,
) -> TimerHit | None:
    instances_text = instances.get(page.npc_id) if page.npc_id else None
    if instances_text:
        return TimerHit(text=instances_text, source="instances")

    if card.slug in EVENT_ONLY_SLUGS:
        return TimerHit(text="Event spawn", source="event-allowlist")

    if card.slug in PRESERVE_EVENT_SPAWN_SLUGS:
        if is_event_spawn_token(page.respawn_text):
            return TimerHit(text=page.respawn_text or "Event spawn", source="event-allowlist")
        return TimerHit(text="Event spawn", source="event-allowlist")

    return npc_timer


def sync_lockouts(
    *,
    index_text: str,
    strategy_dir: Path,
    instances_html: str | None,
    fetch_npc,
    apply: bool,
) -> SyncReport:
    report = SyncReport()
    instances = parse_instances_page(instances_html) if instances_html else {}
    cards = parse_index_cards(index_text)
    for card in cards:
        if card.skip_reason:
            report.skipped_cards.append(f"{card.slug or card.link_text}:{card.skip_reason}")
            continue
        report.scanned += 1
        page = load_boss_page(card.slug, strategy_dir)
        if page is None:
            report.missing_lockout.append(f"{card.slug}: missing page")
            continue
        if page.respawn_text is None:
            report.missing_lockout.append(card.slug)
            continue
        if not page.npc_id and card.slug not in EVENT_ONLY_SLUGS:
            report.missing_npc.append(card.slug)

        npc_timer = None
        if page.npc_id and fetch_npc is not None:
            npc_html = fetch_npc(page.npc_id)
            if npc_html:
                npc_timer = parse_npc_timer(npc_html)

        desired = desired_timer(card, page, instances, npc_timer)
        if desired is None:
            report.missing_timer.append(card.slug)
            continue

        if durations_match(page.respawn_text, desired.text):
            if desired.source == "event-allowlist":
                report.event_only_preserved.append(card.slug)
            report.unchanged += 1
            continue

        if desired.source == "event-allowlist":
            report.event_only_forced.append(card.slug)

        updated = replace_respawn_time(page.raw, desired.text)
        if updated is None:
            report.missing_lockout.append(card.slug)
            continue
        if apply and page.path is not None:
            page.path.write_text(updated, encoding="utf-8")
        report.changes.append(
            Change(
                slug=card.slug,
                old=page.respawn_text,
                new=desired.text,
                source=desired.source,
            )
        )
    return report


def make_fetcher(cache_dir: Path, delay_s: float, offline: bool):
    def fetch_npc(npc_id: str) -> str | None:
        cache_path = cache_dir / "npc" / f"{npc_id}.html"
        if offline:
            if cache_path.exists():
                return cache_path.read_text(encoding="utf-8", errors="replace")
            return None
        return fetch_url(NPC_URL.format(npc_id=npc_id), cache_path, delay_s)

    return fetch_npc


def load_instances(cache_dir: Path, delay_s: float, offline: bool) -> str | None:
    cache_path = cache_dir / "instances.html"
    if offline:
        if cache_path.exists():
            return cache_path.read_text(encoding="utf-8", errors="replace")
        return None
    return fetch_url(INSTANCES_URL, cache_path, delay_s)


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    parser.add_argument("--apply", action="store_true", help="Write lockout box updates")
    parser.add_argument("--dry-run", action="store_true", help="Scan without writing")
    parser.add_argument("--scan-only", action="store_true", help="Walk strategy.md, no PQDI")
    parser.add_argument("--offline", action="store_true", help="Use cache only; no network")
    parser.add_argument("--cache-dir", type=Path, default=None)
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument("--delay", type=float, default=0.25)
    return parser.parse_args(list(argv) if argv is not None else None)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    root: Path = args.root
    index_path = root / "strategy.md"
    strategy_dir = root / "strategy"
    cache_dir = args.cache_dir or (root / ".lockout-cache")
    apply = bool(args.apply) and not args.dry_run and not args.scan_only

    index_text = index_path.read_text(encoding="utf-8")
    if args.scan_only:
        cards = parse_index_cards(index_text)
        bosses = [c for c in cards if not c.skip_reason]
        skipped = [c for c in cards if c.skip_reason]
        print(f"Boss cards: {len(bosses)}")
        print(f"Skipped: {len(skipped)}")
        for card in skipped:
            print(f"  skip {card.slug or card.link_text} ({card.skip_reason})")
        return 0

    instances_html = load_instances(cache_dir, args.delay, args.offline)
    fetch_npc = make_fetcher(cache_dir, args.delay, args.offline)
    report = sync_lockouts(
        index_text=index_text,
        strategy_dir=strategy_dir,
        instances_html=instances_html,
        fetch_npc=fetch_npc,
        apply=apply,
    )
    markdown = report.to_markdown()
    print(markdown)
    if args.report:
        args.report.write_text(markdown, encoding="utf-8")
    if apply:
        print(f"Wrote {len(report.changes)} lockout box update(s).")
    else:
        print("Dry run: no files written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
