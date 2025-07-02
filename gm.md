---
layout: page
title: "GM Commands Reference"
cover-img: /assets/img/gm.webp
permalink: /gm/
subtitle: "Complete reference guide for GM commands in EverQuest"
---

# GM Commands Reference

This page contains a comprehensive list of GM commands available in EverQuest. Commands are organized by category for easier reference.

## Player Management

### Character & Account Commands
- `#ban [name][reason]` - Ban by character name
- `#delacct [accountname]` - Delete an account
- `#expansion [accountname][expansion]` - Sets the expansion value for the specified account
- `#kick [charname]` - Disconnect charname
- `#movechar [charname] [zonename]` - Move charname to zonename
- `#mule [account name] [0/1]` - Toggles the mule status of the specified account
- `#mute [charname] [1/0]` - Makes charname unable to talk on OOC
- `#revoke [charname] [1/0]` - Makes charname unable to talk on OOC
- `#suspend [name][days][reason]` - Suspend by character name and for specified number of days
- `#undeletechar` - Undelete a character that was previously deleted

### Character Appearance & Stats
- `#appearance [type] [value]` - Send an appearance packet for you or your target
- `#beard` - Change the beard of your target
- `#beardcolor` - Change the beard color of your target
- `#face` - Change the face of your target
- `#fixmob [race|gender|texture|helm|face|hair|haircolor|beard|beardcolor|heritage|tattoo|detail] [next|prev]` - Manipulate appearance of your target
- `#hair` - Change the hair style of your target
- `#haircolor` - Change the hair color of your target
- `#helm` - Change the helm of your target
- `#randomfeatures` - Temporarily randomizes the Facial Features of your target
- `#size [size]` - Change size of you or your target
- `#ngpermaclass <class> [deity] [city] [stats...] [force]` - Change your or your target's class (disconnects client)
- `#ngpermarace <race> [deity] [city] [stats...] [force]` - Change your or your target's race (zone to take effect)
- `#ngpermaraceclass <race> <class> [deity] [city] [stats...] [force]` - Change your or your target's race/class (disconnects client)
- `#ngpermastats <stats...>` - Change your or your target's starting stat point allocation (zone to take effect)

### Character Abilities & Spells
- `#altactivate [argument]` - activates alternate advancement abilities, use altactivate help for more information
- `#cast [spellid] [gm_override] [entityid]` - Cast a spell. GM override bypasses resist and stacking checks
- `#castspell [spellid] [gm_override] [entityid]` - Cast a spell. GM override bypasses resist and stacking checks
- `#fillbuffs` - Casts 15 buffs on the target for testing
- `#memspell [slotid] [spellid]` - Memorize spellid in the specified slot
- `#nukebuffs` - Strip all buffs on you or your target
- `#resetaa` - Resets a Player's AA in their profile and refunds spent AA's to unspent, disconnects player
- `#scribespell [spellid]` - Scribe specified spell in your target's spell book
- `#scribespells [max level] [min level]` - Scribe all spells for you or your player target that are usable by them
- `#unmemspell [spellid]` - Unmem specified spell from your target's spell bar
- `#unmemspells` - Clear out your or your player target's spell gems
- `#unscribespell [spellid]` - Unscribe specified spell from your target's spell book
- `#unscribespells` - Clear out your or your player target's spell book

### Items & Money
- `#equipitem [slotid(0-21)]` - Equip the item on your cursor into the specified slot
- `#gi [itemid] [charges]` - Summon an item onto your target's cursor. Charges are optional
- `#giveitem [itemid] [charges]` - Summon an item onto your target's cursor. Charges are optional
- `#givemoney [pp] [gp] [sp] [cp]` - Gives specified amount of money to the target player
- `#iteminfo` - Get information about the item on your cursor
- `#keyring` - Displays target's keyring items
- `#nukeitem [itemid]` - Remove itemid from your player target's inventory
- `#si [itemid] [charges]` - Summon an item onto your cursor. Charges are optional
- `#summonitem [itemid] [charges]` - Summon an item onto your cursor. Charges are optional
- `#takemoney [pp] [gp] [sp] [cp] [reason]` - Takes specified amount of money from the target player

## NPC & Mob Management

### Spawning & NPC Control
- `#advnpc [maketype|makegroup|addgroupentry|addgroupspawn][removegroupspawn|movespawn|editgroupbox|cleargroupbox]`
- `#advnpcspawn [maketype|makegroup|addgroupentry|addgroupspawn][removegroupspawn|movespawn|editgroupbox|cleargroupbox]`
- `#dbspawn [npctypeid] [factionid]` - Spawn an NPC from the db
- `#dbspawn [spawngroup] [respawn] [variance]` - Spawn an NPC from a predefined row in the spawn2 table
- `#depop` - Depop your NPC target
- `#depopzone` - Depop the zone
- `#makepet [level] [class] [race] [texture]` - Make a pet
- `#npccast [targetname/entityid] [spellid]` - Causes NPC target to cast spellid on targetname/entityid
- `#npcemote [message]` - Make your NPC target emote a message
- `#npcsay [message]` - Make your NPC target say a message
- `#npcshout [message]` - Make your NPC target shout a message
- `#npctypespawn [npctypeid] [factionid]` - Spawn an NPC from the db
- `#repop [Force]` - Repop the zone with optional force repop
- `#repopclose [distance in units]` - Repops only NPC's nearby for fast development purposes
- `#spawn [name] [race] [level] [material] [hp] [gender] [class] [priweapon] [secweapon] [merchantid]` - Spawn an NPC
- `#spawnfix` - Find targeted NPC in database based on its X/Y/heading and update the database
- `#testspawn [memloc] [value]` - spawns a NPC for you only, with the specified values set in the spawn struct

### NPC Editing & Properties
- `#ai [factionid/spellslist/con/guard/roambox/stop/start]` - Modify AI on NPC target
- `#attack [targetname]` - Make your NPC target attack targetname
- `#attackentity [entityid]` - Make your NPC target attack target entity
- `#npcedit [column] [value]` - Mega NPC editing command
- `#npcloot [show/money/add/remove] [itemid/all/money: pp gp sp cp]` - Manipulate the loot an NPC is carrying
- `#npcspawn [create/add/update/remove/delete]` - Manipulate spawn DB
- `#npctypecache [id] or all` - Clears the npc type cache for either the id or all npcs
- `#modifynpcstat [Stat] [Value]` - Modifies an NPC's stats temporarily
- `#setnpcexpansion [min_expansion] [max_expansion]` - Restrict an NPC's spawn2 by min, max expansion

### NPC Pathing & Movement
- `#grid [add/delete] [grid_num] [wandertype] [pausetype]` - Create/delete a wandering grid
- `#gridrecord [start|stop|addwp]` - Record a grid using start, stop and use AddWp to add a waypoint
- `#path` - view and edit pathing
- `#pf` - Display additional mob coordinate and wandering data
- `#wp [add/delete] [grid_num] [pause] [wp_num] [-h]` - Add/delete a waypoint to/from a wandering grid
- `#wpadd [pause] [-h]` - Add your current location as a waypoint to your NPC target's AI path

## Combat & Damage

### Combat Commands
- `#aggrozone [aggro] [0/1: Enforce ignore distance. If 0 or not set, all will come]` - Aggro every mob in the zone with X aggro
- `#damage [amount]` - Damage your target
- `#damagetotals` - Displays a list of what has damaged your NPC target
- `#gmdamage [amount] [skipaggro]` - Damage your target. Skips most combat checks, including invul
- `#kill` - Kill your target
- `#manaburn` - Use AA Wizard class skill manaburn on target
- `#push [pushback] [pushup]` - Pushes the target the specified amount
- `#stun [duration]` - Stuns you or your target for duration

### Combat Information
- `#d [type] [spell] [damage]` - Send an OP_Action packet with the specified values
- `#fleeinfo` - Gives info about whether a NPC will flee or not, using the command issuer as top hate
- `#manastat` - Report your or your target's cur/max mana
- `#mystats` - Show details about you or your pet
- `#showregen` - Shows information about your target's regen
- `#xpinfo` - Show XP info about your current target

## Zone & World Management

### Zone Control
- `#connectworld` - Make zone attempt to connect to worldserver
- `#connectworldserver` - Make zone attempt to connect to worldserver
- `#crashtest` - Crash the zoneserver
- `#shutdown` - Shut this zone process down
- `#synctod` - Send a time of day update to every client in zone
- `#worldshutdown` - Shut down world and all zones
- `#zone [Zone ID|Zone Short Name] [X] [Y] [Z]` - Teleport to specified Zone by ID or Short Name
- `#zonebootup (shortname) (ZoneServerID)` - Make a zone server boot a specific zone
- `#zoneguild [Zone ID|Zone Short Name] [GuildID] [X] [Y] [Z]` - Teleport to specified Zone by ID or Short Name
- `#zoneshutdown [shortname]` - Shut down a zone server
- `#zsave` - Saves zheader to the database

### Location & Movement
- `#bestz` - Ask map for a good Z coord for your x,y coords
- `#falltest [+Z]` - sends you to your current loc plus the Z specified
- `#goto [x] [y] [z]` - Teleport to the provided coordinates or to your target
- `#loc` - Print out your or your target's current location and heading
- `#rewind` - Rewind to the previous location
- `#summon [charname]` - Summons your player/npc/corpse target, or charname if specified
- `#underworld [z]` - Reports NPCs that are below the given Z or if not given, below the lowest spawn2/grid coord
- `#zuwcoords [z coord]` - Set underworld coord

### Graveyards & Death
- `#corpse` - Manipulate corpses, use with no arguments for help
- `#deletegraveyard [zone name]` - Deletes the graveyard for the specified zone
- `#setgraveyard [zone name]` - Creates a graveyard for the specified zone based on your target's LOC

## Guild Management
- `#guild` - Guild manipulation commands. Use argument help for more info
- `#guildapprove [guildapproveid]` - Approve a guild with specified ID (guild creator receives the id)
- `#guildcreate [guildname]` - Creates an approval setup for guild name specified
- `#guildlist [guildapproveid]` - Lists character names who have approved the guild specified by the approve id
- `#guilds` - Guild manipulation commands. Use argument help for more info

## Server Administration

### Database & Memory
- `#apply shared memory [shared_memory_name]` - Tells every zone and world to apply a specific shared memory segment by name
- `#hotfix [hotfix_name]` - Reloads shared memory into a hotfix, equiv to load_shared_memory followed by apply_shared_memory
- `#load shared memory [shared_memory_name]` - Reloads shared memory and uses the input as output
- `#mysql` - Mysql CLI, see 'help' for options
- `#mysqltest` - Akkadius MySQL Bench Test

### Logging & Debugging
- `#bug` - Bug report system. Encase your bug in quotes. Type: #bug <quote>I have a bug</quote>
- `#coredump` - Dumps a core log of any existing cores to view on web page
- `#logs` - Manage anything to do with logs
- `#logtest` - Performs log performance testing
- `#rl` - Reloads logs (alias of #reload logs)

### Reloading & Updates
- `#opcode` - Reloads all opcodes from server patch files
- `#reload` - Reloads different types of server data globally, use no argument for help menu
- `#reloadspmod` - Reload spell modifiers from database
- `#rq` - Reloads quests (alias of #reload quests)
- `#sendzonespawns` - Refresh spawn list for all clients in zone

## Communication & Chat

### Chat Commands
- `#chat [channel num] [message]` - Send a channel message to all zones
- `#chattest [color] [loops]` - Sends a test message with the specified color to yourself
- `#clearsaylink` - Clear the saylink table
- `#emote ['name'/'world'/'zone'] [type] [message]` - Send an emote message
- `#interrupt [message id] [color]` - Interrupt your casting. Arguments are optional

### Profanity & Rules
- `#profanity` - Manage censored language
- `#rules (subcommand)` - Manage server rules

## Utility Commands

### Information & Display
- `#help [search term]` - List available commands and their description, specify partial command as argument to search
- `#list [npc] [name|all]` - Search entities
- `#listnpcs [name/range]` - Search NPCs
- `#serversidename` - Prints target's server side name
- `#show` - Show command used to show various things
- `#showbonusstats [item|spell|all]` - Shows bonus stats for target from items or spells
- `#showfilters` - list client serverfilter settings
- `#showhelm on/off [all]` - Toggles displaying of player helms
- `#showlootlockouts` - Shows your currently active loot lockouts
- `#showpetspell [spellid/searchstring]` - search pet summoning spells
- `#showquake` - Shows current earthquake timer. Requires you to be a guild officer or leader
- `#showtraderitems` - Displays the list of items a trader has up for sale
- `#spellinfo [spellid]` - Get detailed info about a spell

### Testing & Development
- `#allowexport [off, worn, inventory, bank]` - Authorize export of this character to be included in nightly, open sourced database dumps
- `#betabuff [level]` - Buffs user's player to provided level, giving level * 100 platinum
- `#devtools` - Manages devtools
- `#interrogateinv` - use [help] argument for available options
- `#interrogatelegacy` - Interrogates legacy items of your current target
- `#lootsim [npc_type_id] [loottable_id] [iterations]` - Runs benchmark simulations using real loot logic
- `#numauths` - TODO: describe this command
- `#optest` - solar's private test command
- `#qtest` - QueryServ testing command
- `#randtest` - Perform a sampling of random number generation
- `#sendop [opcode]` - LE's Private test command, leave it alone
- `#testcommand` - Template for temporary commands as needed. Don't delete
- `#zopp` - Troubleshooting command - Sends a fake item packet to you. No server reference is created

### Special Functions
- `#boatinfo` - Gets information about the boats currently spawned in the zone
- `#cleartimers [timer]` - Clears one or all persistent timers on target
- `#close shop` - Closes a merchant shop
- `#disablerecipe [recipe_id]` - Disables a recipe using the recipe id
- `#doanim [animnum] [type]` - Send an EmoteAnim for you or your target
- `#enablerecipe [recipe_id]` - Enables a recipe using the recipe id
- `#find` - Search command used to find various things
- `#fish` - Fish for an item
- `#flagedit` - Edit zone flags on your target
- `#forage` - Forage an item
- `#giveplayerfaction [factionid] [factionvalue]` - Gives the target player faction with the given faction
- `#interrogatelegacy` - Interrogates legacy items of your current target
- `#ipban [IP address]` - Ban IP by character name
- `#ipexemption [accountname] [exemption]` - Set IP exemption amount for accountname by amount
- `#leaderboard [SFHC|SSFHC|SFHCOnly|HC]` - List hardcore leaderboard
- `#makemule` - Flags the account of the player who runs the command as a mule
- `#merchant close shop` - Closes a merchant shop
- `#merchant open shop` - Opens a merchants shop
- `#open shop` - Opens a merchants shop
- `#petition` - Handles everything petition related. Use with no args or with 'help' for how to use
- `#playsound [number]` - Plays a sound in the client. Valid range 0-3999
- `#quaketrigger [type_num (1 = Normal, 2 = PVP)]` - Triggers an earthquake manually
- `#raidloot LEADER|GROUPLEADER|SELECTED|ALL` - Sets your raid loot settings if you have permission to do so
- `#refreshgroup` - Refreshes Group
- `#removelegacyitem` - Remove a legacy item from your target [itemid], or specify a [charid] [itemid]
- `#resetboat` - Sets player's boat to 0 in their profile
- `#save` - Force your player or player corpse target to be saved to the database
- `#set` - Set command used to set various things
- `#setgreed [greed]` - Sets a merchant greed value
- `#skills` - List skill difficulty
- `#starve` - Sets hunger and thirst to 0
- `#togglepvp` - Toggles PVP for a client
- `#viewplayerfaction [factionid]` - Shows current personal and modified faction with the given ID
- `#wc [wear slot] [material]` - Sends an OP_WearChange for your target
- `#zonespawn` - Not implemented

---

*This reference contains all available GM commands. Use `#help [command]` for more detailed information about specific commands.*