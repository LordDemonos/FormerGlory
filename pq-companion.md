---
layout: page
title: PQ Companion Guide
cover-img: /assets/img/pq-companion.png
subtitle: A guide to installing PQ Companion with Former Glory trigger packs
---

# PQ Companion Setup Guide

PQ Companion is a desktop companion app for Project Quarm. It sits next to the client and covers raid overlays, a DPS meter, spell timers, NPC info, live maps, and a regex trigger engine with on-screen text, sound, and text-to-speech. This guide covers install, first-launch setup, and the Former Glory trigger packs.

## Former Glory Trigger Packs

Each file is its own pack. Import it from Triggers → import wizard, then enable the folders you are using. Countdown bars land on the custom timer overlay.

Planes of Power and Luclin files for GINA and EQLogParser stay on the [GINA Guide](/gina/) and the [EQLogParser Guide](/eqlp/).

### Planes of Power

**Planes of Power:** [Download pop-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/pop-triggers.json?raw=true) — Updated September 13, 2026

Folders land as `PoP / {tier} / {zone} / {boss}`. Enable the bosses you are fighting.

### Luclin

**Luclin:** [Download luclin-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/luclin-triggers.json?raw=true) — Updated October 2, 2026

111 triggers. Folders land as `Luclin / {zone} / {boss}`. Shei and Exiled DT bars speak when they end, including "Xanax One minute until Death Touch" and "XANAX DA THE TANK."

### Raiding

**General:** [Download raiding-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/raiding-triggers.json?raw=true) — Updated October 2, 2026

61 triggers. Chains, assists, debuff macros, and crew alerts.

**Classic:** [Download classic-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/classic-triggers.json?raw=true) — Updated October 2, 2026

38 triggers. Old World and planar mob cards.

**Kunark:** [Download kunark-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/kunark-triggers.json?raw=true) — Updated October 2, 2026

26 triggers. Kunark spells and mob cards.

**Velious:** [Download velious-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/velious-triggers.json?raw=true) — Updated October 2, 2026

96 triggers. Velious spells and mob cards.

### Classes

Import the classes you play.

- **Bard** (50): [class-bard-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/class-bard-triggers.json?raw=true)
- **Beastlord** (2): [class-beastlord-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/class-beastlord-triggers.json?raw=true)
- **Cleric** (45): [class-cleric-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/class-cleric-triggers.json?raw=true)
- **Druid** (38): [class-druid-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/class-druid-triggers.json?raw=true)
- **Enchanter** (51): [class-enchanter-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/class-enchanter-triggers.json?raw=true)
- **Magician** (15): [class-magician-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/class-magician-triggers.json?raw=true)
- **Monk** (16): [class-monk-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/class-monk-triggers.json?raw=true)
- **Necromancer** (44): [class-necromancer-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/class-necromancer-triggers.json?raw=true)
- **Paladin** (25): [class-paladin-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/class-paladin-triggers.json?raw=true)
- **Ranger** (34): [class-ranger-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/class-ranger-triggers.json?raw=true)
- **Rogue** (23): [class-rogue-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/class-rogue-triggers.json?raw=true)
- **Shadow Knight** (25): [class-shadow-knight-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/class-shadow-knight-triggers.json?raw=true)
- **Shaman** (61): [class-shaman-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/class-shaman-triggers.json?raw=true)
- **Warrior** (16): [class-warrior-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/class-warrior-triggers.json?raw=true)
- **Wizard** (12): [class-wizard-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/class-wizard-triggers.json?raw=true)

Updated October 2, 2026.

### Utility

- **Buffs** (134): [buffs-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/buffs-triggers.json?raw=true)
- **Debuffs** (57): [debuffs-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/debuffs-triggers.json?raw=true)
- **Common** (81): [common-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/common-triggers.json?raw=true) — combat alerts, caster and melee warnings
- **Guild** (8): [guild-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/guild-triggers.json?raw=true) — guild tells `!KBP`, `!KBUMP`, `!KCH`, `!KRCH`, `!KDRAG`, `!KLOGS`, `!KMT`, `!KTANK`
- **Tracking** (5): [tracking-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/tracking-triggers.json?raw=true)
- **Timers** (8): [timers-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/timers-triggers.json?raw=true) — `/who fear1`, `malo`, `slow`, `vulakae`, `drain`, `DA`, or `TLUP` to start the bar

Updated October 2, 2026.

## Download and Installation

## System Requirements

- **Windows 10/11**
- **EverQuest log file enabled** — type `/log on` in-game
- **[Zeal](https://github.com/iamclint/Zeal)** (recommended) — Spell Checklist, Inventory Tracker, Key Tracker, and live pipe-source triggers

PQ Companion ships everything it needs. No Go, Node.js, or Docker required to run the app.

## Direct Download Links

**Latest installer:** [PQ Companion Releases](https://github.com/jasonsoprovich/pq-companion/releases/latest) — download `PQ-Companion-Setup-x.x.x.exe`

**Website:** [pq-companion.com](https://pq-companion.com)

**GitHub:** [jasonsoprovich/pq-companion](https://github.com/jasonsoprovich/pq-companion)

## Installation Steps

1. **Download the installer** from the Releases page (`PQ-Companion-Setup-x.x.x.exe`).

2. **Run the installer** and follow the setup wizard.

3. **Handle Windows security warnings** if they appear.

    - Right-click the downloaded file and select "Properties"

    - Check "Unblock" if available and click "Apply"

    - Choose "Run anyway" when prompted by Windows Defender if needed

4. **Launch PQ Companion.** The app updates itself in the background and prompts you to restart when a new version is ready.

## First-Launch Setup

1. Open **Settings** at the bottom of the sidebar.

2. Set **EverQuest Path** to your Project Quarm folder (the folder that contains `eqgame.exe`).

3. Set **Character Name** exactly as it appears in-game.

4. In-game, type `/log on`.

5. Confirm **Parse Combat Log** is enabled in Settings.

The app finds your log file and Zeal exports from that path. A first-launch wizard also tries to auto-detect Zeal.

## Zeal (Recommended)

Install [Zeal](https://github.com/iamclint/Zeal) so PQ Companion can read live client state over a local Windows pipe: target, target HP, pet, group HP, casting, spellbook, inventory, and AAs. Without Zeal the app still runs. Spell Checklist, Inventory Tracker, Key Tracker, and pipe-source triggers will not have data.

## Importing Trigger Packs

Open **Triggers** in the sidebar. The import wizard detects and previews:

- PQ Companion JSON packs (the Former Glory `.json` files above)
- GINA package files (`.gtp`) and GINA XML shares
- EQLogParser trigger files
- EQNag databases

**Import process:**

1. Open **Triggers**.

2. Start the import wizard and select the pack you want (`pop-triggers.json`, `luclin-triggers.json`, a class pack, and so on). Import one pack at a time.

3. Review the preview, then commit the pack into a category.

4. Enable the category (or individual triggers) you want live.

Enable selectively. Start with current raid content and the class you are playing.

The app also ships built-in community packs, including class crowd-control break alerts. Enable those from Triggers without importing anything.

To share a pack later, export a category as JSON from Triggers.

## Setting Up Overlays

Overlays (NPC Info, DPS Meter, Spell Timers, trigger alerts) float above the game as transparent, click-through windows.

1. Confirm **Parse Combat Log** is on and `/log on` is active.

2. Open **Overlays** in the sidebar (or the specific overlay tab).

3. Click the pop-out button (⤢) to float that panel over the game.

4. Drag panels to position. Use Settings overlay lock controls if you need a display-only HUD.

The Overlay Dashboard can hold DPS, spell timers, NPC info, and trigger alerts in one layout.

## Backup and Restore

Under **Settings → Backups**, use **App Backup & Restore** to export settings, triggers, and trigger packs as a single `.pqcb` bundle. Import that file on another machine to restore the same setup.

## Additional Resources

- **Website:** [pq-companion.com](https://pq-companion.com)
- **GitHub:** [github.com/jasonsoprovich/pq-companion](https://github.com/jasonsoprovich/pq-companion)
- **Releases:** [Latest download](https://github.com/jasonsoprovich/pq-companion/releases/latest)
- **Discord:** [PQ Companion Discord](https://discord.gg/Srj4FXcRaz)
- **Zeal:** [github.com/iamclint/Zeal](https://github.com/iamclint/Zeal)
- **Former Glory GINA Guide:** [GINA Guide](/gina/) — `pop.gtp` (Planes of Power) and Fabio's Luclin `.gtp`
- **Former Glory EQLogParser Guide:** [EQLogParser Guide](/eqlp/) — `pop.tgf.gz` (Planes of Power)
- **Former Glory PQ Companion packs:** listed at the top of this page, starting with [pop-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/pop-triggers.json?raw=true)
