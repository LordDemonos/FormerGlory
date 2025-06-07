# Former Glory Guild Website

This site is built on top of the [Beautiful Jekyll](https://beautifuljekyll.com/) theme, but has been heavily customized for the needs of the Former Glory guild on the Project Quarm EverQuest server.

## Major Customizations from Base Beautiful Jekyll

### Navigation & Layout
- **Custom navigation bar** with multi-level dropdowns for Strategy and Services, mobile-friendly hamburger menu, and improved mobile dropdown behavior.
- **Custom layouts and includes** for raid schedules, spell banks, gem banks, and more.
- **Dark and light mode toggle** with persistent user preference.
- **Responsive design** improvements for mobile usability.

### Custom CSS
- `assets/css/custom-styles.css`: Extensive custom styles for cards, tooltips, raid info, spell/gem banks, navigation, and more.
- **Gem legend, spell tooltips, and raid cards** are all styled for clarity and mobile-friendliness.

## JavaScript Enhancements

### Tooltip and Icon Scripts
- `assets/js/tooltip.js`:  
  Adds EverQuest-style item tooltips and icons to all item links (from pqdi.cc), with fallback icons and robust error handling.
- `assets/js/spell-tooltip.js`:  
  Adds rich, dynamic tooltips for spell links using Tippy.js and the pqdi.cc API.

### Raid and Event Utilities
- `assets/js/raid-schedule-generator.js`:  
  Node.js script to parse, organize, and generate markdown for raid schedules, grouping by week/month and providing copy-to-clipboard blocks for Discord announcements.

### UI/UX Scripts
- `assets/js/copy-text.js`:  
  Adds "Copy to Clipboard" buttons to raid/event blocks and other content, with visual feedback and fallback for older browsers.
- `assets/js/back-to-top.js`:  
  Adds a floating button to quickly scroll to top/bottom of the page, with dynamic icon.
- `assets/js/image-resize.js`:  
  Allows images with the `.resize-img` class to be toggled between thumbnail and full-size on click.
- `assets/js/view-toggle.js`:  
  Lets users toggle between "strategy" and "spoilers" views, remembering their preference and scroll position.
- `assets/js/light-dark-toggle.js`:  
  Implements a persistent dark/light mode toggle for the entire site.

## Python Automation

- `assets/py/update_epic_needs.py`:  
  Connects to a Google Sheet to fetch epic request data, processes and categorizes it, and generates/updates the `targets.md` file for the site. This automates the display of raid and off-night target requests, keeping the site in sync with guild submissions.

## Data & Content Automation

- **Google Sheets integration** for epic needs and raid targets, with automated markdown generation.
- **Dynamic raid/event schedule generation** with copy-paste blocks for Discord.

## Intended Purpose & Use

- **Guild Management:**  
  Centralizes raid schedules, target requests, spell/gem banks, and requirements for all members.
- **Community Tools:**  
  Provides easy access to guides, Discord, DKP, and other resources.
- **Quality of Life:**  
  Tooltips, copy buttons, and responsive design make the site easy to use for all members, on any device.
- **Automation:**  
  Reduces officer workload by automating data pulls and page updates from Google Sheets and other sources.

## How to Use/Extend

- **To update raid schedules:**  
  Use the `raid-schedule-generator.js` script to generate new markdown.
- **To update epic needs/targets:**  
  Run the Python script in `assets/py/` to pull the latest data from Google Sheets.
- **To add new tooltips or icons:**  
  Link to pqdi.cc item or spell pages; the JS will handle the rest.
- **To customize styles:**  
  Edit `assets/css/custom-styles.css`.

---

**This README is a living document.**  
If you add new scripts, automations, or major features, please update this file to help future maintainers and guild members!

Welcome to the **Former Glory** guild website! This site serves as the central hub for our community on the **Project Quarm** EverQuest server. Here, you will find all the information you need about our guild, including our charter, events, and resources to help you navigate your journey in Norrath.

## About Former Glory

**Former Glory** is a relaxed, non-hardcore guild dedicated to fostering friendships and adventures among players. We believe in creating a welcoming environment where everyone can enjoy the game at their own pace. Our guild was founded by a group of friends who met in Blackburrow, and we aim to maintain that spirit of camaraderie as we explore the vast world of EverQuest together.

## Our Mission

Our mission is to provide a supportive and enjoyable gaming experience for all members. We focus on:

- **Respect**: Treating all guild members and fellow players with kindness and understanding.
- **Inclusivity**: Welcoming players of all skill levels and backgrounds.
- **Community**: Building lasting friendships through shared experiences in-game.

## Guild Features

- **Non-Mandatory Raiding**: We offer scheduled raids without the pressure of mandatory attendance. Life comes first!
- **Epic Weapon Support**: We assist active members in their quests for epic weapons during the Kunark expansion.
- **Scheduled Events**: Regular raids are held on Monday, Wednesday, and Friday at 9 PM EST, along with occasional unscheduled events.

## Getting Involved

If you're interested in joining **Former Glory**, we encourage you to reach out to our members in-game or through our website. We are always looking for new friends to join our adventures!

Thank you for visiting the **Former Glory** guild website! We look forward to seeing you in Norrath!

