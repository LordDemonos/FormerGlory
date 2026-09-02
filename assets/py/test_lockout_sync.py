"""Unit tests for lockout_sync.py (no network)."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import lockout_sync as ls  # noqa: E402

FIXTURES = HERE / "lockout_fixtures"

INDEX = """
<h4><a href="https://www.pqdi.cc/zone/32" target="_blank">Nagafen's Lair</a></h4>
<div class="card-container">
  <div class="card dragon">
    <ul>
      <li><a href="lord_nagafen">Lord Nagafen</a> · <a href="/raid-loot#lord-nagafen">Loot</a></li>
      <li>Level 55 Dragon Warrior</li>
    </ul>
  </div>
</div>
<h4><a href="https://www.pqdi.cc/zone/179" target="_blank">Akheva Ruins</a></h4>
<div class="card-container">
  <div class="card dragon">
    <ul>
      <li><a href="shei_vinitras">Shei Vinitras</a> · <a href="/raid-loot#shei-vinitras">Loot</a></li>
      <li>Level 65 Thought Horror Warrior</li>
    </ul>
  </div>
</div>
<h4><a href="https://www.pqdi.cc/zone/158" target="_blank">Vex Thal</a></h4>
<div class="card-container">
  <div class="card dragon">
    <ul>
      <li><a href="vex_thal">Vex Thal Overview</a></li>
      <li>With Maps</li>
    </ul>
  </div>
</div>
<h4><a href="https://www.pqdi.cc/zone/223" target="_blank">Plane of Time</a></h4>
<div class="card-container">
  <div class="card dragon">
    <ul>
      <li><a href="plane_of_time">Plane of Time</a></li>
      <li>Event Guide</li>
    </ul>
  </div>
  <div class="card dragon">
    <ul>
      <li><a href="neimon_of_air">Neimon of Air</a> · <a href="/raid-loot#neimon-of-air">Loot</a></li>
      <li>Level 68 Elemental Warrior</li>
    </ul>
  </div>
</div>
<div class="card-container">
  <div class="card dragon">
    <ul>
      <li><a href="pop_progression">Planes of Power Progression</a></li>
      <li>Flagging Guide</li>
    </ul>
  </div>
</div>
"""

NAGGY_PAGE = """---
title: Lord Nagafen
---
<div class="info-item"><strong>Zone:</strong> <a href="https://www.pqdi.cc/zone/32">Nagafen's Lair</a></div>
<div class="info-item"><strong>Faction:</strong> KOS&nbsp;&nbsp;&nbsp;<a href="https://www.pqdi.cc/npc/32040" target="_blank" title="View NPC on PQDI">🔗</a></div>
<div class="info-lockoutitem"><strong>Respawn Time:</strong> 3 days</div>
"""

SHEI_PAGE = """---
title: Shei Vinitras
---
<div class="info-item"><strong>Zone:</strong> <a href="https://www.pqdi.cc/zone/179">Akheva Ruins</a></div>
<div class="info-item"><strong>Faction:</strong> KOS&nbsp;&nbsp;&nbsp;<a href="https://www.pqdi.cc/npc/179017" target="_blank" title="View NPC on PQDI">🔗</a></div>
<div class="info-lockoutitem"><strong>Respawn Time:</strong> 6 days and 18 hours</div>
"""

NEIMON_PAGE = """---
title: Neimon of Air
---
<div class="info-item"><strong>Zone:</strong> <a href="https://www.pqdi.cc/zone/223">Plane of Time</a></div>
<div class="info-item"><strong>Faction:</strong> KOS&nbsp;&nbsp;&nbsp;<a href="https://www.pqdi.cc/npc/223044" target="_blank" title="View NPC on PQDI">🔗</a></div>
<div class="info-lockoutitem"><strong>Respawn Time:</strong> 3 days</div>
"""


def _write_pages(folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "lord_nagafen.md").write_text(NAGGY_PAGE, encoding="utf-8")
    (folder / "shei_vinitras.md").write_text(SHEI_PAGE, encoding="utf-8")
    (folder / "neimon_of_air.md").write_text(NEIMON_PAGE, encoding="utf-8")


class DurationTests(unittest.TestCase):
    def test_parse_common_strings(self) -> None:
        self.assertEqual(ls.parse_duration_seconds("6 days and 18 hours"), 162 * 3600)
        self.assertEqual(ls.parse_duration_seconds("66 hours"), 66 * 3600)
        self.assertEqual(ls.parse_duration_seconds("3 hours, 8 minutes, 20 seconds"), 3 * 3600 + 8 * 60 + 20)
        self.assertIsNone(ls.parse_duration_seconds("Event spawn"))
        self.assertIsNone(ls.parse_duration_seconds("Event spawn — trial lockout 30 minutes on success"))
        self.assertIsNone(ls.parse_duration_seconds("35 minutes after the Council"))

    def test_match_ignores_wording(self) -> None:
        self.assertTrue(ls.durations_match("6 days and 18 hours", "162 hours"))
        self.assertTrue(ls.durations_match("Event spawn", "Event spawn — extra"))
        self.assertFalse(ls.durations_match("3 days", "Event spawn"))


class WalkerTests(unittest.TestCase):
    def test_skips_guides_and_overviews(self) -> None:
        cards = ls.parse_index_cards(INDEX)
        skipped = {c.slug: c.skip_reason for c in cards if c.skip_reason}
        bosses = [c.slug for c in cards if not c.skip_reason]
        self.assertEqual(skipped["vex_thal"], "Overview")
        self.assertEqual(skipped["plane_of_time"], "Event Guide")
        self.assertEqual(skipped["pop_progression"], "Flagging Guide")
        self.assertEqual(bosses, ["lord_nagafen", "shei_vinitras", "neimon_of_air"])


class PqdiParseTests(unittest.TestCase):
    def test_instances_override_by_npc_id(self) -> None:
        html = (FIXTURES / "instances.html").read_text(encoding="utf-8")
        timers = ls.parse_instances_page(html)
        self.assertEqual(timers["32000"], "18 hours")
        self.assertEqual(timers["179017"], "2 days and 18 hours")

    def test_npc_quick_facts_and_ms_fallback(self) -> None:
        emperor = (FIXTURES / "npc_emperor.html").read_text(encoding="utf-8")
        gryme = (FIXTURES / "npc_gryme.html").read_text(encoding="utf-8")
        hit = ls.parse_npc_timer(emperor)
        self.assertIsNotNone(hit)
        assert hit is not None
        self.assertEqual(hit.source, "npc")
        self.assertEqual(ls.parse_duration_seconds(hit.text), 162 * 3600)
        self.assertIsNone(ls.parse_npc_timer(gryme))


class SyncTests(unittest.TestCase):
    def test_instances_wins_npc_page_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            strategy = Path(tmp)
            _write_pages(strategy)
            instances = (FIXTURES / "instances.html").read_text(encoding="utf-8")
            report = ls.sync_lockouts(
                index_text=INDEX,
                strategy_dir=strategy,
                instances_html=instances,
                apply=True,
            )
            naggy = (strategy / "lord_nagafen.md").read_text(encoding="utf-8")
            shei = (strategy / "shei_vinitras.md").read_text(encoding="utf-8")
            neimon = (strategy / "neimon_of_air.md").read_text(encoding="utf-8")
            # Nagafen 32040 is not on /instances — leave the page, do not use NPC spawn
            self.assertIn("3 days", naggy)
            self.assertIn("lord_nagafen", report.missing_timer)
            # instances hit for Shei 179017 beats FG 6d18h
            self.assertIn("2 days and 18 hours", shei)
            # event-only stays Event spawn when /instances has no override
            self.assertIn("Event spawn", neimon)
            self.assertNotIn("3 days", neimon)
            sources = {c.slug: c.source for c in report.changes}
            self.assertNotIn("lord_nagafen", sources)
            self.assertEqual(sources["shei_vinitras"], "instances")
            self.assertEqual(sources["neimon_of_air"], "event-allowlist")

    def test_apply_writes_lf_even_when_page_was_crlf(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            strategy = Path(tmp)
            _write_pages(strategy)
            (strategy / "shei_vinitras.md").write_bytes(
                SHEI_PAGE.replace("\n", "\r\n").encode("utf-8")
            )
            instances = (FIXTURES / "instances.html").read_text(encoding="utf-8")
            ls.sync_lockouts(
                index_text=INDEX,
                strategy_dir=strategy,
                instances_html=instances,
                apply=True,
            )
            written = (strategy / "shei_vinitras.md").read_bytes()
            self.assertNotIn(b"\r\n", written)
            self.assertIn(b"2 days and 18 hours", written)


if __name__ == "__main__":
    unittest.main()
