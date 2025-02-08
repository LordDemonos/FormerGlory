import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime

# Add debug logging
print("Script started")
print("Current working directory:", os.getcwd())

# Load credentials from the environment variable
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
try:
    print("Attempting to load credentials...")
    creds_content = os.environ.get('GOOGLE_CREDENTIALS')
    if not creds_content:
        print("Error: GOOGLE_CREDENTIALS environment variable is not set")
        exit(1)
    
    # Try to parse the credentials
    try:
        creds_dict = eval(creds_content)
        print("Credential keys available:", list(creds_dict.keys()))
    except Exception as e:
        print(f"Error parsing credentials: {str(e)}")
        exit(1)

    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=SCOPES
    )
    print("Credentials loaded successfully")

except Exception as e:
    print(f"Error setting up credentials: {str(e)}")
    exit(1)

# Build the service
try:
    print("Building service...")
    service = build('sheets', 'v4', credentials=creds)
    print("Service built successfully")
except Exception as e:
    print(f"Error building service: {str(e)}")
    exit(1)

# Specify the spreadsheet ID and range
SPREADSHEET_ID = '10Y4D2n7LFb0WwZpZwNRxK1eKy0J8xjA6LZknpPuszc0'
RANGE_NAME = 'Sheet1!A1:Z'  # Adjust as needed

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])

# Predefined zone groupings
zone_groupings = {
    "Mon/Fri": ["Sebilis", "Skyfire"],
    "Wed": ["Plane of Sky", "City of Mist", "Chardok", "Timorous Deep", "Karnor's Castle", "Kithicor Forest", "Lake of Ill Omen"],
    "Sat": ["Plane of Hate", "Plane of Fear"]
}

# Organize data by group and zone
grouped_data = {group: {zone: [] for zone in zones} for group, zones in zone_groupings.items()}

for row in values[1:]:  # Skip header row
    if len(row) < 7 or row[6] == "Completed":  # Skip if row is incomplete or task is completed
        continue

    zone = row[3]  # Zone column
    for group, zones in zone_groupings.items():
        if zone in zones:
            grouped_data[group][zone].append(row)

# Generate markdown file
markdown_output = []
markdown_output.append('---')
markdown_output.append('layout: page')
markdown_output.append('title: Epic Mob Requests')
markdown_output.append('permalink: /epic-needs/')
markdown_output.append('last_updated: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
markdown_output.append('---\n')

# Table of contents
markdown_output.append('## Table of Contents\n')
for group in zone_groupings.keys():
    markdown_output.append(f'- [{group}](#{group.lower().replace("/", "-")})')
markdown_output.append('\n')

# Grouped sections
for group, zones in grouped_data.items():
    markdown_output.append(f'## {group}\n')
    for zone, entries in zones.items():
        if entries:  # Only display zones with entries
            markdown_output.append(f'### {zone}\n')
            markdown_output.append('<div class="request-container">')
            for entry in entries:
                markdown_output.append('  <div class="request-card">')
                markdown_output.append(f'    <p><strong>Character Name:</strong> {entry[1]}</p>')
                markdown_output.append(f'    <p><strong>Class:</strong> {entry[2]}</p>')
                markdown_output.append(f'    <p><strong>Target:</strong> {entry[4]}</p>')
                markdown_output.append(f'    <p><strong>Availability:</strong> {entry[5]}</p>')
                markdown_output.append('  </div>')
            markdown_output.append('</div>\n')

# Write to file
with open('epic_needs.md', 'w') as f:
    f.write('\n'.join(markdown_output))

print("Markdown file 'epic_needs.md' has been generated successfully.")
