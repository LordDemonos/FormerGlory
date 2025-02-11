import os
import json
from collections import defaultdict
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
RANGE_NAME = "'Form Responses 1'!A2:G10"  # Start from A2 to skip headers

# Define the zone-day mapping
zone_day_mapping = {
    "Plane of Hate": "Saturday",
    "Plane of Fear": "Saturday",
    "Plane of Sky": "Wednesday",
    "Kithicor Forest": "Wednesday",
    "Lake of Ill Omen": "Wednesday",
    "Skyfire": "Monday/Friday",
    "City of Mist": "Wednesday",
    "Chardok": "Wednesday",
    "Timorous Deep": "Saturday",
    "Karnor's Castle": "Wednesday",
    "Sebilis": "Monday/Friday",
}

def process_sheet(sheet):
    epic_needs = {
        'monday_friday': [],
        'wednesday': [],
        'saturday': []
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
            
        days_list = [day.strip() for day in days.split(',')]
        
        entry = {
            'name': name,
            'class': char_class,
            'zone': zone,
            'item': item,
            'days': days_list
        }
        
        # Add to appropriate day lists
        if any(day in ['Mon', 'Fri'] for day in days_list):
            epic_needs['monday_friday'].append(entry)
        if 'Wed' in days_list:
            epic_needs['wednesday'].append(entry)
        if 'Sat' in days_list:
            epic_needs['saturday'].append(entry)
    
    return epic_needs

try:
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    print(f"Total rows fetched from spreadsheet: {len(values)}")  # Debug line

    if not values:
        print("No data found in the specified range.")
    else:
        # Organize cards by day
        cards_by_day = defaultdict(list)
        for row in values:
            print(f"Processing row: {row}")  # Debug line
            
            # Skip if row doesn't have enough elements
            if len(row) < 5:
                print(f"Skipping row due to insufficient fields: {row}")
                continue

            # Skip completed rows
            if len(row) > 6 and row[6]:
                print(f"Skipping completed row: {row}")
                continue
            
            # Only process if we have all required fields
            if all(row[0:5]):  # Check if first 5 fields have values
                zone = row[2]  # Zone is in the third column
                day = zone_day_mapping.get(zone)
                if day:
                    cards_by_day[day].append(row)
                    print(f"Added row to {day}: {row}")  # Debug line
                else:
                    print(f"No day mapping found for zone: {zone}")  # Debug line
            else:
                print(f"Skipping row due to missing required fields: {row}")  # Debug line

        print(f"Final cards_by_day contents: {dict(cards_by_day)}")  # Debug line

        with open('targets.md', 'w') as file:
            # Write the front matter
            file.write("---\n")
            file.write("layout: page\n")
            file.write("title: Target Requests\n")
            file.write("subtitle: Submit your requests for raid night\n")
            file.write("cover-img: /assets/img/targets.webp\n")
            file.write("---\n\n")
            # Add the table of contents heading
            file.write('<div class="toc-heading">Table of Contents - Jump to a Raid Night</div>\n')
            # Write the submission link and table of contents in one flex container
            file.write('<div style="display: flex; justify-content: space-between; align-items: center; font-size: 1.25em; margin-bottom: 20px;">\n')
            file.write('  <div style="display: flex; gap: 20px; flex: 1;">\n')
            for day in ["Monday/Friday", "Wednesday", "Saturday"]:
                anchor = day.lower().replace("/", "-")
                file.write(f'    <a href="#{anchor}">{day}</a>\n')
            file.write('  </div>\n')
            file.write('  <div style="margin-left: 20px;">\n')
            file.write('    <a href="https://docs.google.com/forms/d/e/1FAIpQLSfrdGZCRdUpdJ14DtRNTurlymNWYFvUbFBp0GvLOXvZb9JApA/viewform">Request Form</a>\n')
            file.write('  </div>\n')
            file.write('</div>\n\n')

            # Write cards under each day
            for day in ["Monday/Friday", "Wednesday", "Saturday"]:
                anchor = day.lower().replace("/", "-")
                file.write(f'<h2 id="{anchor}">{day}</h2>\n')
                file.write(f'<p class="raid-description">{day} raid targets include {", ".join([zone for zone, d in zone_day_mapping.items() if d == day])}</p>\n')
                file.write('<div class="card-container">\n')
                for row in cards_by_day.get(day, []):
                    class_name = row[1].lower().replace(" ", "-")
                    file.write(f'  <div class="card {class_name}">\n')
                    file.write('    <ul>\n')
                    for item in row[0:5]:
                        file.write(f'      <li>{item}</li>\n')
                    file.write('    </ul>\n')
                    file.write('  </div>\n')
                file.write('</div>\n\n')

        print("Data successfully written to targets.md with front matter")

except Exception as e:
    print(f"Error accessing spreadsheet: {str(e)}")
    exit(1)
