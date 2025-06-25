---
published: 'true'
date: '2025-06-24 22:33 -0400'
author: Xanax
title: Xanny Helper
description: >-
  A purpose built solution for managing raid schedules, offnight events,
  inventory, and suggestions for our gaming community.
keywords: >-
  discord, inventory, raid, offnight, static group, suggestions, events,
  calendar, website, automation
---
# Former Glory Discord Event Bot

A self-hosted Discord bot for managing raid schedules, offnight events, and community logistics.

---

## **Key Features**

- **Discord Integration**
  - Reads and parses raid schedules and offnight events directly from Discord threads and messages.
  - Supports recurring events via thread titles (e.g., “Sundays 10:30 AM EST”).

- **Google Calendar Sync**
  - Automatically creates, updates, and deletes Google Calendar events to match the Discord raid schedules and static group events.
  - Keeps the calendar in sync with what’s posted in Discord—no manual entry needed.
  
- **Inventory File Management**
   - Monitors Discord channels for inventory file uploads (e.g., `Fggems-Inventory.txt`).
   - Updates local and GitHub copies, ensuring the latest data is always available.

- **Suggestions System**
  - Reads suggestions from a Google Sheet and posts new ones to a designated Discord channel.
  - Prevents reposting and supports moderation.

- **GitHub Integration**
  - Backs up and version-controls our raid and inventory files by syncing them to my GitHub repo.
  - Ensures our event data is never lost and can be audited or restored.

- **Automated Cleanup**
  - Only processes active Discord threads—archived/inactive threads are ignored.
  - Cleans up old events from the calendar and event files when threads go inactive.

- **Production-Ready Logging**
  - Concise, color-coded logs for all major operations, errors, and sync summaries.
  - No sensitive data is ever logged.

---

I've been working on this for many weeks now. My apologies for any weirdness with the calendar. I wanted to further automate some tasks and provide better visibility not only for raids but for all the offnight and static groups we create. That way every event gets advertised and any changes are updated quickly and accurately.

I never properly introduced the bot in a patch note, and today marks what I'd consider the first release of the code.

---

*Want to see the ((awful)) code or run it yourself? [Check it out on GitHub!](https://github.com/LordDemonos/xanny-helper)*
