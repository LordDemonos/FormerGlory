---
layout: page
title: PQ Companion Guide
cover-img: /assets/img/pq-companion.png
subtitle: A guide to installing PQ Companion with Former Glory trigger packs
---

# PQ Companion Setup Guide

PQ Companion is a desktop companion app for Project Quarm. It sits next to the client and covers raid overlays, a DPS meter, spell timers, NPC info, live maps, and a regex trigger engine with on-screen text, sound, and text-to-speech. This guide covers install, first-launch setup, and the Former Glory Planes of Power pack.

## Former Glory Trigger Packs

**Planes of Power:** [Download pop-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/pop-triggers.json?raw=true) — Updated September 2, 2026

This is a native PQ Companion pack (same Who / Casts / Procs / Emotes tree as the GINA and EQLogParser packs). Import it from Triggers → import wizard → select `pop-triggers.json`. Folders land as `PoP / {tier} / {zone} / {boss}`. Enable the bosses you are fighting.

Luclin GINA and EQLogParser packs stay on the [GINA Guide](/gina/) and the [EQLogParser Guide](/eqlp/).

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

- PQ Companion JSON packs (this is `pop-triggers.json`)
- GINA package files (`.gtp`) and GINA XML shares
- EQLogParser trigger files
- EQNag databases

**Import process:**

1. Open **Triggers**.

2. Start the import wizard and select `pop-triggers.json`.

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
- **Former Glory PQ Companion pack:** [pop-triggers.json](https://github.com/LordDemonos/FormerGlory/blob/master/pop-triggers.json?raw=true)
