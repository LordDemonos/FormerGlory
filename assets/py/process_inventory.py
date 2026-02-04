import os
from datetime import datetime, timedelta
from collections import Counter
import sys
import time

def get_repo_root():
    """Get the repository root directory by going up two levels from the script location"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(script_dir))

def get_input_output_paths():
    """Get the correct input and output paths for GitHub automation"""
    repo_root = get_repo_root()
    input_dir = os.path.join(repo_root, 'assets', 'data')
    output_dir = repo_root
    
    print(f"📂 Repository root: {repo_root}")
    print(f"📂 Input directory: {input_dir}")
    print(f"📂 Output directory: {output_dir}")
    
    return input_dir, output_dir

def wait_for_both_spell_files(input_dir, max_wait_minutes=5, check_interval_seconds=30):
    """
    Wait for both spell inventory files to be available and recently updated.
    If only one file is updated, waits up to 5 minutes for the other to arrive.
    Returns True if both files are ready, False if timeout.
    """
    spell_files = {
        'Fgspells-Inventory.txt': 'FGS',
        'Fgspellsdump-Inventory.txt': 'SPD'
    }
    
    file_paths = {name: os.path.join(input_dir, name) for name in spell_files.keys()}
    max_wait_seconds = max_wait_minutes * 60
    start_time = time.time()
    initial_check = True
    
    print(f"\n⏳ Checking for both spell files (will wait up to {max_wait_minutes} minutes)...")
    
    while time.time() - start_time < max_wait_seconds:
        files_exist = {name: os.path.exists(path) for name, path in file_paths.items()}
        current_time = time.time()
        
        if all(files_exist.values()):
            # Both files exist, check modification times
            mod_times = {}
            for name, path in file_paths.items():
                mod_times[name] = os.path.getmtime(path)
            
            # Check if both files were modified within 5 minutes of each other
            time_diff = abs(mod_times['Fgspells-Inventory.txt'] - mod_times['Fgspellsdump-Inventory.txt'])
            
            if time_diff <= 300:  # 5 minutes in seconds
                print(f"✅ Both spell files found and updated within 5 minutes of each other!")
                return True
            else:
                # Files exist but weren't updated together
                older_file = 'Fgspells-Inventory.txt' if mod_times['Fgspells-Inventory.txt'] < mod_times['Fgspellsdump-Inventory.txt'] else 'Fgspellsdump-Inventory.txt'
                newer_file = 'Fgspellsdump-Inventory.txt' if older_file == 'Fgspells-Inventory.txt' else 'Fgspells-Inventory.txt'
                newer_mod_time = mod_times[newer_file]
                older_mod_time = mod_times[older_file]
                time_diff_minutes = time_diff / 60
                
                # Check if the newer file was updated recently (within last 5 minutes)
                # If so, wait for the older file to be updated
                time_since_newer = current_time - newer_mod_time
                if time_since_newer <= 300:  # Newer file updated within last 5 minutes
                    elapsed_minutes = (current_time - start_time) / 60
                    remaining_minutes = max_wait_minutes - elapsed_minutes
                    print(f"⏳ Files updated {time_diff_minutes:.1f} minutes apart. Newer file ({newer_file}) updated {time_since_newer/60:.1f} min ago. Waiting up to {remaining_minutes:.1f} more minutes for {older_file} to be updated...")
                else:
                    # Files are too far apart, proceed anyway
                    print(f"⚠️  Files updated {time_diff_minutes:.1f} minutes apart (newer file is older than 5 minutes). Proceeding...")
                    return True
        else:
            # One or both files missing
            existing_files = [name for name, exists in files_exist.items() if exists]
            missing_files = [name for name, exists in files_exist.items() if not exists]
            
            if existing_files:
                elapsed_minutes = (current_time - start_time) / 60
                remaining_minutes = max_wait_minutes - elapsed_minutes
                print(f"⏳ Found {', '.join(existing_files)}. Waiting up to {remaining_minutes:.1f} more minutes for: {', '.join(missing_files)}")
            else:
                print(f"⏳ Waiting for both files: {', '.join(missing_files)}")
        
        # Wait before checking again
        if not initial_check:
            time.sleep(check_interval_seconds)
        initial_check = False
    
    # Timeout reached
    print(f"⚠️  Timeout reached after {max_wait_minutes} minutes.")
    files_exist = {name: os.path.exists(path) for name, path in file_paths.items()}
    if all(files_exist.values()):
        # Check one more time if they're close enough
        mod_times = {}
        for name, path in file_paths.items():
            mod_times[name] = os.path.getmtime(path)
        time_diff = abs(mod_times['Fgspells-Inventory.txt'] - mod_times['Fgspellsdump-Inventory.txt'])
        if time_diff <= 300:
            print("✅ Both files found and updated within 5 minutes of each other!")
            return True
        else:
            print("⚠️  Both files exist but weren't updated together. Proceeding with available files...")
            return True
    else:
        missing_files = [name for name, exists in files_exist.items() if not exists]
        print(f"⚠️  Missing file(s): {', '.join(missing_files)}. Proceeding with available files...")
        return False

def process_text_data(text_data, is_spell_inventory, file_name, character_prefix='', return_raw=False):
    print(f"\n🔍 Processing {file_name}...")
    lines = text_data.strip().split('\n')
    item_counter = Counter()
    first_locations = {}  # (item_name, item_id) -> location string
    excluded_items = ['Empty', 'Backpack', 'Elemental Grimoire', 'Large Box', "Deluxe Toolbox", "Ivandyr's Hoop", 'A Worn Candle', 'Hand Made Backpack', 'Currency', 'Bread Cakes*', 'Skin of Milk', 'Large Sewing Kit']
    excluded_ids = ['0', '17005', '17880']
    
    def parse_location(loc):
        prefix = f'{character_prefix} ' if character_prefix else ''
        # General bags
        if loc.startswith('General'):
            if '-Slot' in loc:
                bag = loc[len('General'):loc.index('-Slot')]
                slot = loc.split('-Slot')[1]
                return f'{prefix}Inv{bag} s{slot}'
            else:
                bag = loc[len('General'):]
                return f'{prefix}Inv{bag}'
        # Bank bags
        if loc.startswith('Bank'):
            if '-Slot' in loc:
                bag = loc[len('Bank'):loc.index('-Slot')]
                slot = loc.split('-Slot')[1]
                return f'{prefix}Bnk{bag} s{slot}'
            else:
                bag = loc[len('Bank'):]
                return f'{prefix}Bnk{bag}'
        # SharedBank
        if loc.startswith('SharedBank'):
            if '-Slot' in loc:
                num = loc[len('SharedBank'):loc.index('-Slot')]
                return f'{prefix}SBnk{num}'
            else:
                num = loc[len('SharedBank'):]
                return f'{prefix}SBnk{num}'
        # Held
        if loc == 'Held':
            return f'{prefix}Held' if prefix else 'Held'
        return f'{prefix}{loc}' if prefix else loc  # fallback
    
    # Skip the first line
    items_processed = 0
    for line in lines[1:]:
        parts = line.split('\t')
        if len(parts) > 3:
            location = parts[0].strip()
            item_name = parts[1].strip()
            item_id = parts[2].strip()
            
            # Skip SharedBank slots unless we're processing the spells inventory
            if location.startswith('SharedBank') and not is_spell_inventory:
                continue
                
            # Check if the item should be excluded
            if item_name not in excluded_items and item_id not in excluded_ids:
                key = (item_name, item_id)
                if key not in first_locations:
                    first_locations[key] = parse_location(location)
                if is_spell_inventory:
                    # For spells, we just count occurrences
                    item_counter[key] += 1
                else:
                    # For bank items and gems, we sum the counts
                    count = int(parts[3].strip())
                    item_counter[key] += count
                items_processed += 1
    
    # Return raw data if requested (for spell combining)
    if return_raw:
        print(f"✅ Processed {items_processed} items from {file_name}")
        return item_counter, first_locations
    
    # Otherwise format and return output lines
    output_lines = []
    for (item_name, item_id), count in item_counter.items():
        loc = first_locations.get((item_name, item_id), '')
        if count > 1 or not is_spell_inventory:
            item_str = f'[{item_name}](https://www.pqdi.cc/item/{item_id}) x{count}'
        else:
            item_str = f'[{item_name}](https://www.pqdi.cc/item/{item_id})'
        output_lines.append(f'{loc} {item_str}'.strip())
    
    # Sort the output lines alphabetically by item name (ignoring location prefix)
    output_lines.sort(key=lambda x: x.split('[')[1].lower())
    print(f"✅ Processed {items_processed} items from {file_name}")
    return output_lines

def get_gem_legend():
    GEM_ID_MAP = {
        "Flawless Diamond": "25814",
        "Flawed Sea Sapphire": "25839",
        "Flawed Emerald": "25821",
        "Crushed Coral": "25831",
        "Crushed Black Marble": "25805",
        "Crushed Topaz": "25832",
        "Crushed Flame Emerald": "25838",
        "Pristine Emerald": "25807",
        "Nephrite": "25816",
        "Flawed Topaz": "25818",
        "Crushed Flame Opal": "25837",
        "Crushed Jaundice Gem": "25829",
        "Crushed Onyx Sapphire": "25841",
        "Chipped Onyx Sapphire": "25827",
        "Jaundice Gem": "25815",
        "Black Marble": "25805",
        "Crushed Lava Ruby": "25840",
        "Crushed Opal": "25836",  # Corrected ID
    }
    def gem_link(name):
        item_id = GEM_ID_MAP.get(name)
        if item_id:
            return f'<a href="https://www.pqdi.cc/item/{item_id}">{name}</a>'
        return name
    return f"""
<div class=\"gem-legend\" style=\"display: flex; justify-content: space-between; margin-top: 2rem;\">
    <div style=\"width: 32%;\">
        <h4>Bard/Beastlord/Monk/Paladin/Ranger/Shadow Knight/Rogue/Warrior</h4>
        <table class=\"gem-legend-table\">\n<tr><th>Slot</th><th>Gems x3</th></tr>\n<tr><td>Chest</td><td>{gem_link('Flawless Diamond')}</td></tr>\n<tr><td>Legs</td><td>{gem_link('Flawed Sea Sapphire')}</td></tr>\n<tr><td>Arms</td><td>{gem_link('Flawed Emerald')}</td></tr>\n<tr><td>Head</td><td>{gem_link('Crushed Coral')}</td></tr>\n<tr><td>Feet</td><td>{gem_link('Crushed Black Marble')}</td></tr>\n<tr><td>Hands</td><td>{gem_link('Crushed Topaz')}</td></tr>\n<tr><td>Wrist</td><td>{gem_link('Crushed Flame Emerald')}</td></tr>\n</table>
    </div>
    <div style=\"width: 32%;\">
        <h4>Enchanter/Magician/Necromancer/Wizard</h4>
        <table class=\"gem-legend-table\">\n<tr><th>Slot</th><th>Gems x3</th></tr>\n<tr><td>Chest</td><td>{gem_link('Pristine Emerald')}</td></tr>\n<tr><td>Legs</td><td>{gem_link('Nephrite')}</td></tr>\n<tr><td>Arms</td><td>{gem_link('Flawed Topaz')}</td></tr>\n<tr><td>Head</td><td>{gem_link('Crushed Flame Opal')}</td></tr>\n<tr><td>Feet</td><td>{gem_link('Crushed Jaundice Gem')}</td></tr>\n<tr><td>Hands</td><td>{gem_link('Crushed Topaz')}</td></tr>\n<tr><td>Wrist</td><td>{gem_link('Crushed Onyx Sapphire')}</td></tr>\n</table>
    </div>
    <div style=\"width: 32%;\">
        <h4>Cleric/Druid/Shaman</h4>
        <table class=\"gem-legend-table\">\n<tr><th>Slot</th><th>Gems x3</th></tr>\n<tr><td>Chest</td><td>{gem_link('Black Marble')}</td></tr>\n<tr><td>Legs</td><td>{gem_link('Chipped Onyx Sapphire')}</td></tr>\n<tr><td>Arms</td><td>{gem_link('Jaundice Gem')}</td></tr>\n<tr><td>Head</td><td>{gem_link('Crushed Onyx Sapphire')}</td></tr>\n<tr><td>Feet</td><td>{gem_link('Crushed Flame Emerald')}</td></tr>\n<tr><td>Hands</td><td>{gem_link('Crushed Lava Ruby')}</td></tr>\n<tr><td>Wrist</td><td>{gem_link('Crushed Opal')}</td></tr>\n</table>
    </div>
</div>
"""

def write_to_markdown_file(output_lines, output_file_path, front_matter, last_update):
    print(f"\n📝 Writing to {output_file_path}...")
    with open(output_file_path, 'w') as f:
        f.write(front_matter + '\n\n')  # Write front matter at the top of the file
        f.write(f'### Last Update: {last_update}\n\n')  # Add last update date as an H3 header
        for line in output_lines:
            f.write(line + '\n\n')  # Add an extra newline after each item for readability
        
        # Add gem legend if this is the gems file
        if 'gems.md' in output_file_path:
            f.write('\n### Gem Legend\n\n')
            f.write(get_gem_legend())
    print(f"✅ Successfully wrote {output_file_path}")

def combine_spell_data(counter1, locations1, counter2, locations2):
    """Combine spell data from two files, merging counters and keeping first locations"""
    combined_counter = Counter(counter1)
    combined_counter.update(counter2)
    
    # Combine locations, keeping the first instance found
    combined_locations = dict(locations1)
    for key, loc in locations2.items():
        if key not in combined_locations:
            combined_locations[key] = loc
    
    # Generate combined output lines
    output_lines = []
    for (item_name, item_id), count in combined_counter.items():
        loc = combined_locations.get((item_name, item_id), '')
        if count > 1:
            item_str = f'[{item_name}](https://www.pqdi.cc/item/{item_id}) x{count}'
        else:
            item_str = f'[{item_name}](https://www.pqdi.cc/item/{item_id})'
        output_lines.append(f'{loc} {item_str}'.strip())
    
    # Sort the output lines alphabetically by item name (ignoring location prefix)
    output_lines.sort(key=lambda x: x.split('[')[1].lower())
    return output_lines

def process_inventory_files():
    print("\n🚀 Starting inventory processing...")
    
    # Get the correct paths for GitHub automation
    input_dir, output_dir = get_input_output_paths()
    
    # Wait for both spell files to be available
    wait_for_both_spell_files(input_dir)
    
    # Process spell files separately and combine them
    spell_files = {
        'Fgspells-Inventory.txt': 'FGS',
        'Fgspellsdump-Inventory.txt': 'SPD'
    }
    
    spell_counters = []
    spell_locations = []
    spell_mod_times = []
    
    for file_name, prefix in spell_files.items():
        input_path = os.path.join(input_dir, file_name)
        
        if not os.path.exists(input_path):
            print(f"⚠️  Warning: Spell file not found: {input_path}")
            continue
        
        try:
            with open(input_path, 'r') as file:
                input_data = file.read()
            
            counter, locations = process_text_data(input_data, True, file_name, prefix, return_raw=True)
            spell_counters.append(counter)
            spell_locations.append(locations)
            
            # Get the date modified of the source file
            mod_time = os.path.getmtime(input_path)
            spell_mod_times.append(mod_time)
            
        except Exception as e:
            print(f"❌ Error processing {file_name}: {str(e)}")
            continue
    
    # Combine spell data if we have files
    if len(spell_counters) > 0:
        if len(spell_counters) == 2:
            combined_spell_data = combine_spell_data(
                spell_counters[0], spell_locations[0],
                spell_counters[1], spell_locations[1]
            )
        else:
            # Single file - format it directly
            counter = spell_counters[0]
            locations = spell_locations[0]
            output_lines = []
            for (item_name, item_id), count in counter.items():
                loc = locations.get((item_name, item_id), '')
                if count > 1:
                    item_str = f'[{item_name}](https://www.pqdi.cc/item/{item_id}) x{count}'
                else:
                    item_str = f'[{item_name}](https://www.pqdi.cc/item/{item_id})'
                output_lines.append(f'{loc} {item_str}'.strip())
            output_lines.sort(key=lambda x: x.split('[')[1].lower())
            combined_spell_data = output_lines
        
        # Use the most recent modification time
        if spell_mod_times:
            latest_mod_time = max(spell_mod_times)
            last_update = datetime.fromtimestamp(latest_mod_time).strftime('%Y-%m-%d')
        else:
            last_update = datetime.now().strftime('%Y-%m-%d')
        
        output_path = os.path.join(output_dir, 'spells.md')
        front_matter = """---
layout: page
title: Spell Bank
cover-img: /assets/img/spells.webp
subtitle: List of Spells in the guild bank
---
### Speak with Dihat if you wish to make a withdraw."""
        
        write_to_markdown_file(combined_spell_data, output_path, front_matter, last_update)
    
    # Define other expected input files
    expected_files = {
        'Fsbank-Inventory.txt': {
            'output': 'sky.md',
            'front_matter': """---
layout: page
title: Sky Bank
cover-img: /assets/img/sky.webp
subtitle: List of Plane of Sky items in the guild bank
---
### Speak with Dihat if you wish to make a withdraw."""
        },
        'Fggems-Inventory.txt': {
            'output': 'gems.md',
            'front_matter': """---
layout: page
title: Gem Bank
cover-img: /assets/img/gems.webp
subtitle: List of Gems in the guild bank
---
### Speak with Dihat if you wish to make a withdraw."""
        }
    }
    
    # Process other files
    for file_name, config in expected_files.items():
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, config['output'])
        
        if not os.path.exists(input_path):
            print(f"❌ Error: Input file not found: {input_path}")
            continue
            
        try:
            with open(input_path, 'r') as file:
                input_data = file.read()
            
            processed_data = process_text_data(input_data, False, file_name)
            
            # Get the date modified of the source file
            mod_time = os.path.getmtime(input_path)
            last_update = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d')
            
            write_to_markdown_file(processed_data, output_path, config['front_matter'], last_update)
            
        except Exception as e:
            print(f"❌ Error processing {file_name}: {str(e)}")
            continue
    
    print("\n✨ Inventory processing complete!")

if __name__ == "__main__":
    try:
        process_inventory_files()
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        sys.exit(1)
