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
    "Timorous Deep": "Wednesday",
    "Karnor's Castle": "Wednesday",
    "Sebilis": "Monday/Friday",
}

try:
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print("No data found in the specified range.")
    else:
        # Organize cards by day
        cards_by_day = defaultdict(list)
        for row in values:
            zone = row[3]  # Assuming the zone is in the fourth column
            day = zone_day_mapping.get(zone)
            if day:
                cards_by_day[day].append(row)

        def write_markdown(epic_needs):
            with open("docs/epic_needs.md", "w") as f:
                # Write the title
                f.write("# Epic Quest Needs\n\n")
                
                # Write the description and TOC section
                f.write('<div class="toc-description">Table of Contents - Jump to a Raid Night</div>\n\n')
                
                # Write the raid day links in their own div
                f.write('<div class="raid-day-links">\n')
                f.write("- [Monday/Friday](#mondayfriday)\n")
                f.write("- [Wednesday](#wednesday)\n")
                f.write("- [Saturday](#saturday)\n")
                f.write("</div>\n\n")
                
                # Write the request form link in its own div
                f.write('<div class="request-form-link">\n')
                f.write("[Request Form](https://forms.gle/your-form-link-here)\n")
                f.write("</div>\n\n")
                
                # Write the Monday/Friday section
                f.write("## Monday/Friday\n")
                f.write("Typical raid targets include Veeshan's Peak in Skyfire, and Trakanon in Old Sebilis.\n\n")
                # ... rest of Monday/Friday content

                # Write the Wednesday section
                f.write("## Wednesday\n")
                f.write("Typical raid targets include Plane of Sky and various Epic raid mobs that are less convenient on other nights.\n\n")
                # ... rest of Wednesday content

                # Write the Saturday section
                f.write("## Saturday\n")
                f.write("Typical raid targets include Plane of Hate, Plane of Fear, Venril Sathir.\n\n")
                # ... rest of Saturday content

                # Continue with the rest of your existing markdown generation...

        write_markdown(cards_by_day)

except Exception as e:
    print(f"Error accessing spreadsheet: {str(e)}")
    exit(1)
