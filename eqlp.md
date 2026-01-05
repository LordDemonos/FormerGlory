---
layout: page
title: EQLogParser Guide
cover-img: /assets/img/eqlp.png
subtitle: A guide to installing EQLogParser with Fabio's triggers
---

# EQLogParser Setup Guide

EQLogParser is a real-time combat log analyzer and damage parsing application built specifically for the EverQuest MMO. It monitors and processes in-game log files to provide detailed statistics as well as various utility functions including damage dealt and received, spell casting counts, audio triggers, and game overlays. This guide will walk you through downloading, installing, and configuring EQLogParser to enhance your EverQuest gameplay experience with automated alerts for raid mechanics, spell timers, and other critical game events.

## Download and Installation

## System Requirements

EQLogParser requires the following to function properly:

- **Windows 10/11** (64-bit only)
- **[.NET Desktop Runtime 8.0.11+](https://dotnet.microsoft.com/download/dotnet/8.0)** - Download and install this first if you don't have it
- **EverQuest in windowed mode** - Required for game overlays to function
- **Overlay Windows Taskbar disabled** - Turn this off in EverQuest settings for overlays to work correctly

## Direct Download Links

**Official Website:** [Download EQLogParser](https://eqlogparser.kizant.net/)

**GitHub Repository:** [EQLogParser on GitHub](https://github.com/kauffman12/EQLogParser)

**Installation Guide:** [EQLogParser Introductory Guide](https://github.com/kauffman12/EQLogParser/discussions/238)

## Installation Steps

1. **Install .NET Desktop Runtime 8.0.11+** - Download and install from the Microsoft link above if you don't already have it installed.

2. **Download EQLogParser** - Visit the official website and download the latest version (currently v2.3.41 or newer).

3. **Run the installer** - Execute the downloaded `.exe` file and follow the installation wizard prompts.

4. **Handle Windows security warnings** - Modern Windows versions may display security warnings about the installer.

    - Right-click the downloaded file and select "Properties"

    - Check "Unblock" if available and click "Apply"

    - Choose "Run anyway" when prompted by Windows Defender if needed

5. **Complete installation** - Follow the setup wizard to finish installation. EQLogParser will be available from your Start Menu or desktop shortcut.

If you encounter installation issues, try running the installer from an administrator command prompt or temporarily disable Windows Defender during installation.

## Adding Characters to EQLogParser

EQLogParser's multi-character monitoring capability requires setting up character profiles for each EverQuest character whose log file you want to monitor. Each character profile links to a specific log file and can have customized settings and monitoring preferences.

## Character Setup Process

1. **Enable EverQuest logging** by typing `/log on` in-game for each character you want to monitor

2. **Open EQLogParser** and navigate to the **Characters** section or tab

3. **Click Add** or the "+" button to create a new character profile

4. **Locate your log file** - EverQuest log files are typically found in your EverQuest installation directory under the `Logs` folder:

    - Example path: `D:\TAKPv22\Logs\` or `C:\Program Files\EverQuest\Logs\`

    - Log files are formatted as `eqlog_CharacterName_ServerName.txt`

    - Example: `eqlog_Xanax_pq.proj.txt`

5. **Select the appropriate log file** - Use the browse button or file picker to navigate to and select your character's log file

6. **Configure character settings** - Set your character name and any other preferences (voice settings, monitoring options, etc.)

7. **Save the character profile** to complete setup

Character profiles will display in your character list, and you can toggle monitoring on or off for each character. Active monitoring is typically indicated by a play/stop button or status indicator next to each character name.

## Understanding EQLogParser Triggers

Triggers in EQLogParser define specific text patterns to monitor in your log files and the corresponding notifications to display when those patterns are detected. Each trigger consists of search text that matches log file entries and one or more notification types including audio alerts, visual overlays, text-to-speech announcements, and timer displays.

Triggers are organized within trigger groups, allowing for easy management of class-specific triggers, raid-specific alerts, and general utility triggers. EQLogParser supports multiple notification types: audio playback, text overlays, text-to-speech synthesis, and timer displays with countdown functionality.

**For detailed information on regex patterns, trigger variables, and advanced trigger configuration, see the [EQLogParser Documentation](https://eqlogparser.kizant.net/documentation.html).**

## Fabio's Trigger Pack

**Primary Download:** [Download Fabio's GINA triggers](https://github.com/LordDemonos/FormerGlory/blob/master/gina_pack.gtp?raw=true)

**Note:** Fabio's trigger pack was originally created for GINA. EQLogParser can import GINA trigger packages (.gtp files), but you may need to review and adjust some triggers after import as the two systems have slight differences in trigger syntax and capabilities.

## Importing Custom Triggers

EQLogParser supports importing triggers from GINA package files (.gtp), making it easy to migrate your existing trigger collections. The import process allows you to merge imported triggers with your existing library while maintaining organization.

**Import Process:**

1. **Open EQLogParser** and navigate to **View > Triggers > Trigger Manager** from the menu bar

2. **Locate the "Triggers" folder** in the left sidebar of the Trigger Manager window - this is the root folder for all triggers

3. **Right-click on the "Triggers" folder** to open the context menu

4. **Select "Import to (Triggers)"** from the context menu (this option has a download icon next to it)

5. **Browse to your trigger file** (e.g., `gina_pack.gtp`) and select it

6. **Review the imported triggers** - EQLogParser will add the imported triggers to your library, organized within their existing group structure

**Video Tutorial:** [Importing Triggers](https://www.youtube.com/watch?v=OcaXCBLW2Gs)

For community-shared triggers, EQLogParser's trigger system is compatible with many GINA trigger packages, providing access to a wide collection of raid and utility triggers that can be directly imported and customized for your specific needs.

## Enabling and Managing Triggers

**Important Difference from GINA:** Unlike GINA where triggers could be enabled or disabled per character, EQLogParser uses a global trigger system. When you enable or disable triggers, they apply to all characters you have configured. This means all your characters will share the same trigger configuration.

EQLogParser uses a hierarchical system where triggers are organized into groups, and entire groups can be enabled or disabled globally. The trigger system monitors all active character log files simultaneously, so any enabled trigger will fire for any character whose log file matches the trigger pattern.

## Trigger Selection Strategy

**Enable selectively** rather than activating all available triggers to prevent notification overload. Focus on enabling:

- **Current expansion raid triggers** for active raid content

- **Class-specific triggers** that match the classes you play (these will fire for any character of that class)

- **General utility triggers** for common buffs and warnings

- **Guild-specific triggers** if using custom guild trigger packages

## Enabling Trigger Groups

1. **Open the Trigger Manager** by navigating to **View > Triggers > Trigger Manager**

    **Understanding the Interface:** EQLogParser uses a tabbed interface in the right pane. When you open **View > Triggers > Trigger Manager**, it opens a tab in the right pane. This tab contains:

    - **Left side:** A hierarchical tree view showing triggers and encounters
    - **Right side:** Properties and editing panel for the selected item
    - **Bottom section:** The "Manage Overlays" window where all overlays are displayed and managed

2. **View available trigger groups** in the left sidebar - triggers are organized in a hierarchical tree structure

3. **Enable relevant groups** using checkboxes:

    - Checked boxes indicate enabled groups

    - Unchecked boxes represent disabled groups

    - Some interfaces may show partial checkmarks for groups with mixed enabled/disabled sub-triggers

4. **Expand group folders** to enable specific sub-categories as needed

5. **Ensure "Triggers Enabled" checkbox** is checked at the top of the Trigger Manager (this is the master switch for all triggers)

**Note for GINA Users:** Since triggers are global in EQLogParser, you may want to be more selective about which triggers you enable compared to GINA. If you have multiple characters with different needs, consider creating separate trigger configurations or being strategic about which trigger groups you activate to avoid notification overload across all characters.

Avoid enabling excessive trigger groups simultaneously as this can cause performance issues during high-activity periods. Start with essential triggers and gradually add others based on your specific gameplay needs.

**Video Tutorial:** [Creating Triggers](https://www.youtube.com/watch?v=LU8RyJpxVTY)

## Setting Up Overlays

EQLogParser's overlay system provides visual notifications that appear on top of your EverQuest window, displaying trigger alerts, timers, and other information without requiring you to alt-tab out of the game. The overlay system supports both text displays and timer countdowns with customizable positioning, fonts, and colors.

**Important:** For overlays to work properly:

- EverQuest must be running in **windowed mode** (not fullscreen)
- The **"Overlay Windows Taskbar"** option must be **turned off** in EverQuest settings

## Creating Text Overlays

1. **Open the Trigger Manager** if you haven't already (navigate to **View > Triggers > Trigger Manager**)

2. **Scroll down to the "Manage Overlays" section** at the bottom of the Trigger Manager tab

3. **Locate the "Overlays" folder** in the overlay tree - you'll see default overlays like "A Default Text Overlay", "Buff Timers", "Debuff Timers", etc.

4. **Select "A Default Text Overlay"** or create a new text overlay by right-clicking on the "Overlays" folder

5. **Configure the overlay settings** in the right properties panel:

    - Set the overlay name and type (text display)

    - Configure font settings: Font Family, Font Size, Font Weight, Font Color

    - Set position coordinates: Position Left, Position Top, Position Width, Position Height

    - Configure alignment: Horizontal Alignment, Vertical Alignment

    - Set overlay appearance: Overlay Color (background), Text Drop Shadow, Streamer Mode

    - Configure fade settings: Fade Delay

6. **Click "Preview Overlay"** to see how it will appear on your screen

7. **Click "Save"** to save the overlay configuration

Text overlays can display trigger messages, character names, and other dynamic information. The positioning system allows precise placement over specific areas of your EverQuest interface, such as near your target window or chat area.

## Timer Overlay Configuration

Timer overlays provide countdown displays for spell durations, raid mechanics, and other time-sensitive events. These overlays integrate with triggers that specify timer durations.

1. **Open the Trigger Manager** if you haven't already (navigate to **View > Triggers > Trigger Manager**)

2. **Scroll down to the "Manage Overlays" section** at the bottom of the Trigger Manager tab

3. **Select an existing timer overlay** (like "Buff Timers", "Debuff Timers", "Emergency Timers", or "Short Duration Timers") or create a new timer overlay

4. **Configure timer settings** in the right properties panel:

    - Set the overlay name and type (timer/countdown)

    - Configure duration: Duration (hh:mm:ss)

    - Set timer behavior: If Triggered Again, Reset Duration

    - Configure timer end settings: End Sound/Text to, End Text to Display

    - Set timer warning settings: Warn With Time Remaining, Warning Sound/Text

    - Configure timer end early settings: Match Pattern, Sound/Text to Speak, Text to Display

5. **Customize appearance** including font size, color, and background settings (same as text overlays)

6. **Click "Save"** to save the overlay configuration

Configure timer overlays similarly to text overlays, with additional options for countdown display formats and expiration alerts. Position timer overlays in easily visible screen areas where they won't interfere with critical game interface elements.

**Video Tutorial:** [Setting Up Overlays](https://www.youtube.com/watch?v=lvCX4MR5SXQ)

## Assigning Overlays to Triggers

After setting up your overlays, you need to assign them to individual triggers so that the triggers will display their notifications using your configured overlays. This completes the setup cycle: import triggers → configure overlays → assign overlays to triggers.

**Assigning Overlays:**

1. **Open the Trigger Manager** if you haven't already (navigate to **View > Triggers > Trigger Manager**)

2. **Locate the trigger** you want to configure in the left sidebar tree view - expand folders as needed to find the specific trigger

3. **Click on the trigger** to select it - the trigger's properties will appear in the right properties panel

4. **Expand the "Overlays" section** in the right properties panel (if it's not already expanded)

5. **Assign a Text Overlay:**
    - Find the **"Assigned Text"** dropdown field
    - Click the dropdown and select the text overlay you want to use (e.g., "Default Text Overlay")
    - This overlay will display the trigger's "Text to Display" message when the trigger fires

6. **Assign a Timer Overlay:**
    - Find the **"Assigned Timer"** dropdown field
    - Click the dropdown and select the timer overlay you want to use (e.g., "Emergency Timers", "Buff Timers", "Debuff Timers")
    - This overlay will display countdown timers for triggers that have timers enabled
    - Note: The trigger must have "Enable Timer" set to "Countdown" in the Trigger section for the timer overlay to be used

7. **Click "Save"** to save your changes to the trigger

**Tips for Assigning Overlays:**

- **Text Overlays** are used for displaying alert messages when triggers fire. Most triggers will benefit from having a text overlay assigned.

- **Timer Overlays** are used for countdown displays. Only assign timer overlays to triggers that have timers enabled (check the "Enable Timer" setting in the Trigger section).

- You can assign both a text overlay and a timer overlay to the same trigger if you want both a message and a countdown.

- Common overlay assignments:
  - **Emergency Timers:** Use for critical raid mechanics, enrage timers, or urgent warnings
  - **Buff Timers:** Use for beneficial spell durations
  - **Debuff Timers:** Use for harmful effect durations
  - **Short Duration Timers:** Use for quick, short-duration effects
  - **Default Text Overlay:** Use for general text notifications

- After importing trigger packs, you may need to assign overlays to many triggers. You can work through them systematically by category (e.g., assign all raid triggers to Emergency Timers, all buff triggers to Buff Timers, etc.).

## Boss Fight Mechanics via In-Game Commands

Many trigger packages include boss information systems that respond to in-game commands, allowing players to quickly access fight mechanics without leaving the game. These systems typically use `/tell` commands directed at specific character names or channels to retrieve stored information about raid encounters.

## Using Boss Information Commands

The exact command structure varies by trigger package, but common implementations include:

- `/tell [BossName]` to get basic fight mechanics

- `/tell [Character] boss [EncounterName]` for detailed strategy information

- Channel-based commands for guild-specific fight information

These information systems prove invaluable during raids when players need quick reminders about specific mechanics, positioning requirements, or timing windows for particular encounters. The information typically appears as text overlays or audio announcements, providing immediate access without disrupting gameplay flow.

## Customizing and Editing Triggers

EQLogParser provides comprehensive trigger editing capabilities allowing you to modify existing triggers, adjust notification types, and fine-tune alert timing. The trigger editor interface offers detailed control over search patterns, notification methods, and trigger behavior.

## Accessing the Trigger Editor

1. **Navigate to your trigger library** in EQLogParser's interface

2. **Locate the trigger to modify** within its group structure

3. **Double-click the trigger** or right-click and select "Edit" to open the editor

4. **Make desired modifications** to search text, notifications, or settings:

    - Edit the trigger pattern/text to match

    - Adjust notification types (audio, overlay, text-to-speech)

    - Modify timer durations if applicable

    - Change trigger group assignment

5. **Save changes** to update the trigger

## Using Log Files for Trigger Development

EverQuest's log files provide the raw material for creating and refining triggers. Access your character's log file to identify exact text patterns for new triggers or troubleshoot existing ones that aren't firing correctly.

**Log File Analysis:**

1. **Locate your log file** in the EverQuest Logs directory (typically in your EverQuest installation folder)

2. **Open with a text editor** to view recent entries

3. **Identify trigger text patterns** by examining relevant game events

4. **Copy exact text** for use in trigger search fields

5. **Test triggers** using EQLogParser's trigger testing functionality if available

This approach ensures triggers match actual log output rather than assumed text patterns, improving reliability and reducing false positives. Regular log file review also helps identify new opportunities for helpful triggers based on your specific gameplay patterns and needs.

**For help with regex patterns and trigger variables when creating custom triggers, refer to the [EQLogParser Documentation](https://eqlogparser.kizant.net/documentation.html).**

## Backup and Log Management

EQLogParser provides useful tools for backing up your configuration and managing your EverQuest log files to keep them organized and manageable.

### Creating Configuration Backups

It's highly recommended to create regular backups of your EQLogParser configuration, especially after setting up triggers, overlays, and character profiles. This ensures you can restore your settings if something goes wrong or if you need to transfer your configuration to another computer.

**To create a backup:**

1. **Navigate to Tools > Create Backup File** from the menu bar

2. **Choose a location** to save your backup file

3. **Save the backup** - EQLogParser will create a backup file containing all your triggers, overlays, character settings, and other configuration data

**To restore from a backup:**

1. **Navigate to Tools > Restore From Backup** from the menu bar

2. **Select your backup file** and follow the prompts to restore your configuration

Regular backups are especially important before making major changes to your trigger setup or when updating EQLogParser versions.

### Log Management

EverQuest log files can grow very large over time, which can slow down EQLogParser and make log files difficult to manage. EQLogParser's Log Management feature allows you to automatically backup and archive your log files, keeping them at a manageable size.

**To configure Log Management:**

1. **Navigate to Tools > Log Management** from the menu bar

2. **Configure automatic log backups:**
   - Set when log files should be backed up (e.g., daily, weekly, or when they reach a certain size)
   - Choose where backup log files should be stored
   - Configure whether to compress old log files to save space

3. **Save your settings** - EQLogParser will automatically manage your log files according to your preferences

This feature helps keep your active log files small and performant while preserving historical log data in backups for later review or analysis.

## Additional Resources

- **Official Website:** [eqlogparser.kizant.net](https://eqlogparser.kizant.net/)
- **Official Documentation:** [EQLogParser Documentation](https://eqlogparser.kizant.net/documentation.html) - Comprehensive guide covering regex patterns, trigger variables, and advanced configuration
- **GitHub Repository:** [github.com/kauffman12/EQLogParser](https://github.com/kauffman12/EQLogParser)
- **Community Guide:** [EQLogParser Introductory Guide](https://github.com/kauffman12/EQLogParser/discussions/238)
- **Video Tutorials:**
  - [Creating Triggers](https://www.youtube.com/watch?v=LU8RyJpxVTY)
  - [Importing Triggers](https://www.youtube.com/watch?v=OcaXCBLW2Gs)
  - [Setting Up Overlays](https://www.youtube.com/watch?v=lvCX4MR5SXQ)

