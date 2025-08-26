import os
from datetime import datetime
from collections import Counter
import sys

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

def process_text_data(text_data, is_spell_inventory, file_name):
    print(f"\n🔍 Processing {file_name}...")
    lines = text_data.strip().split('\n')
    item_counter = Counter()
    first_locations = {}  # (item_name, item_id) -> location string
    excluded_items = ['Empty', 'Backpack', 'Elemental Grimoire', 'Large Toolbox', "Deluxe Toolbox", "Ivandyr's Hoop", 'A Worn Candle', 'Hand Made Backpack', 'Currency', 'Bread Cakes*', 'Skin of Milk', 'Large Sewing Kit']
    excluded_ids = ['0', '17005', '17880']
    
    def parse_location(loc):
        # General bags
        if loc.startswith('General'):
            if '-Slot' in loc:
                bag = loc[len('General'):loc.index('-Slot')]
                slot = loc.split('-Slot')[1]
                return f'Inv{bag} s{slot}'
            else:
                bag = loc[len('General'):]
                return f'Inv{bag}'
        # Bank bags
        if loc.startswith('Bank'):
            if '-Slot' in loc:
                bag = loc[len('Bank'):loc.index('-Slot')]
                slot = loc.split('-Slot')[1]
                return f'Bnk{bag} s{slot}'
            else:
                bag = loc[len('Bank'):]
                return f'Bnk{bag}'
        # SharedBank
        if loc.startswith('SharedBank'):
            if '-Slot' in loc:
                num = loc[len('SharedBank'):loc.index('-Slot')]
                return f'SBnk{num}'
            else:
                num = loc[len('SharedBank'):]
                return f'SBnk{num}'
        # Held
        if loc == 'Held':
            return 'Held'
        return loc  # fallback
    
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

def process_inventory_files():
    print("\n🚀 Starting inventory processing...")
    
    # Get the correct paths for GitHub automation
    input_dir, output_dir = get_input_output_paths()
    
    # Define the expected input files
    expected_files = {
        'Fgspells-Inventory.txt': {
            'output': 'spells.md',
            'front_matter': """---
layout: page
title: Spell Bank
cover-img: /assets/img/spells.webp
subtitle: List of Spells in the guild bank
---
### Speak with Dihat if you wish to make a withdraw."""
        },
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
    
    # Process each file
    for file_name, config in expected_files.items():
        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, config['output'])
        
        if not os.path.exists(input_path):
            print(f"❌ Error: Input file not found: {input_path}")
            continue
            
        try:
            with open(input_path, 'r') as file:
                input_data = file.read()
            
            is_spell_inventory = 'Fgspells-Inventory.txt' in file_name
            processed_data = process_text_data(input_data, is_spell_inventory, file_name)
            
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
