import os
import json
from collections import defaultdict
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Load credentials from the environment variable
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
creds_content = os.environ.get('GOOGLE_CREDENTIALS')

if not creds_content:
    print("Error: GOOGLE_CREDENTIALS environment variable is not set")
    exit(1)

creds_dict = json.loads(creds_content)
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

# Build the service
service = build('sheets', 'v4', credentials=creds)

# Specify the spreadsheet ID and range for the data
SPREADSHEET_ID = '10Y4D2n7LFb0WwZpZwNRxK1eKy0J8xjA6LZknpPuszc0'
RANGE_NAME = "'Form Responses 1'!A2:G100"  # Start from A2 to skip headers

# Define the zone mapping for off-night targets
off_night_zones = [
    # Kunark zones
    "Plane of Hate",
    "Plane of Fear",
    "Plane of Sky",
    "Kithicor Forest",
    "Lake of Ill Omen",
    "Skyfire",
    "City of Mist",
    "Chardok",
    "Timorous Deep",
    "Karnor's Castle",
    "Sebilis",
    "Burning Woods"
]

# Define the raid night zones
raid_night_zones = [
    # Velious zones
    "Great Divide"  # For Dain Ring War
]

# Create a combined mapping for validation
zone_day_mapping = {zone: "off_night" for zone in off_night_zones}

def process_sheet(sheet):
    epic_needs = {
        'raid_nights': [],
        'off_night': []
    }
    
    # Skip header row
    for row in sheet.iter_rows(min_row=2, values_only=True):
        # Debugging: Print the row to see its contents
        print("Processing row:", row)
        
        # Check if there's a value in the Completed column (column G, index 6)
        if row[6]:  # If Completed column has any value, skip this row
            print("Skipping row due to Completed column:", row)
            continue
            
        name = row[0]
        char_class = row[1]
        zone = row[2]
        item = row[3]
        days = row[4]
        
        if not all([name, char_class, zone, item, days]):  # Skip if any required field is empty
            continue
            
        entry = {
            'name': name,
            'class': char_class,
            'zone': zone,
            'item': item,
            'days': days
        }
        
        # Add to appropriate list based on zone
        if zone in raid_night_zones:
            epic_needs['raid_nights'].append(entry)
        elif zone in off_night_zones:
            epic_needs['off_night'].append(entry)
    
    return epic_needs

try:
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    print(f"DEBUG: Total rows fetched: {len(values)}")
    print(f"DEBUG: Raw values: {values}")  # This will show us exactly what data we're getting

    if not values:
        print("No data found in the specified range.")
    else:
        # Organize cards by category
        cards_by_category = {
            'raid_nights': [],
            'off_night': []
        }
        
        # Get current date for comparison
        current_date = datetime.now()
        
        for row in values:
            print(f"DEBUG: Processing row: {row}")
            
            # Skip if row doesn't have enough elements
            if len(row) < 5:
                print(f"DEBUG: Row skipped - insufficient fields: {row}")
                continue

            # Skip completed rows (only if column G exists and has a value)
            if len(row) > 6 and row[6]:
                print(f"DEBUG: Row skipped - marked as completed: {row}")
                continue
            
            # Only process if we have all required fields
            if all(field.strip() for field in row[0:5]):
                # Parse the timestamp from the first column
                try:
                    entry_date = datetime.strptime(row[0], '%m/%d/%Y %H:%M:%S')
                    days_old = (current_date - entry_date).days
                    
                    # Skip if entry is older than 30 days and not in Great Divide
                    if days_old > 30 and row[3] != "Great Divide":
                        print(f"DEBUG: Row skipped - older than 30 days: {row}")
                        continue
                except ValueError as e:
                    print(f"DEBUG: Error parsing date for row: {row}, Error: {e}")
                    continue
                
                zone = row[3]
                if zone in raid_night_zones:
                    cards_by_category['raid_nights'].append(row)
                elif zone in off_night_zones:
                    cards_by_category['off_night'].append(row)
                else:
                    print(f"DEBUG: Zone not found in either category: {zone}")

        print(f"DEBUG: Final cards_by_category contents: {dict(cards_by_category)}")

        with open('targets.md', 'w') as file:
            # Write the front matter
            file.write("---\n")
            file.write("layout: page\n")
            file.write("title: Target Requests\n")
            file.write("subtitle: Submit your requests for raid night\n")
            file.write("cover-img: /assets/img/targets.webp\n")
            file.write("---\n\n")
            
            # Add the table of contents heading
            file.write('<div class="toc-heading">Table of Contents</div>\n')
            # Write the submission link and table of contents in one flex container
            file.write('<div style="display: flex; justify-content: space-between; align-items: center; font-size: 1.25em; margin-bottom: 20px;">\n')
            file.write('  <div style="display: flex; gap: 20px; flex: 1;">\n')
            file.write('    <a href="#raid-nights">Raid Nights</a>\n')
            file.write('    <a href="#off-night-targets">Off Night Targets</a>\n')
            file.write('  </div>\n')
            file.write('  <div style="margin-left: 20px;">\n')
            file.write('    <a href="https://docs.google.com/forms/d/e/1FAIpQLSfrdGZCRdUpdJ14DtRNTurlymNWYFvUbFBp0GvLOXvZb9JApA/viewform">Request Form</a>\n')
            file.write('  </div>\n')
            file.write('</div>\n\n')

            # Write Raid Nights section
            file.write('<h2 id="raid-nights">Raid Nights</h2>\n')
            file.write('<p class="raid-description">Our main raid nights are focused on the Dain Ring War in Great Divide.</p>\n')
            file.write('<div class="card-container">\n')
            for row in cards_by_category['raid_nights']:
                class_name = row[2].lower().replace(" ", "-")
                file.write(f'  <div class="card {class_name}">\n')
                file.write('    <ul>\n')
                for item in row[1:6]:
                    file.write(f'      <li>{item}</li>\n')
                file.write('    </ul>\n')
                file.write('  </div>\n')
            file.write('</div>\n\n')

            # Write Off Night Targets section
            file.write('<h2 id="off-night-targets">Off Night Targets</h2>\n')
            file.write('<p class="raid-description">These targets can be tackled on off nights with smaller groups.</p>\n')
            file.write('<div class="card-container">\n')
            for row in cards_by_category['off_night']:
                class_name = row[2].lower().replace(" ", "-")
                file.write(f'  <div class="card {class_name}">\n')
                file.write('    <ul>\n')
                for item in row[1:6]:
                    file.write(f'      <li>{item}</li>\n')
                file.write('    </ul>\n')
                file.write('  </div>\n')
            file.write('</div>\n\n')

        print("Data successfully written to targets.md with front matter")

except Exception as e:
    print(f"Error accessing spreadsheet: {str(e)}")
    exit(1)
