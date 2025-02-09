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
    
    creds_dict = json.loads(creds_content)
    print("Successfully parsed credentials JSON")
    print("Available keys:", list(creds_dict.keys()))
    
    creds = Credentials.from_service_account_info(
        creds_dict,
        scopes=SCOPES
    )
    print("Credentials loaded successfully")

except Exception as e:
    print(f"Error setting up credentials: {str(e)}")
    print("Exception type:", type(e).__name__)
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
RANGE_NAME = "'Form Responses 1'!A1:Z1000"

try:
    print(f"Attempting to access spreadsheet {SPREADSHEET_ID}")
    print(f"Using range: {RANGE_NAME}")
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    print(f"Successfully retrieved {len(values)} rows of data")

    if not values:
        print("No data found in spreadsheet")
        exit(1)

    print("\nFirst few rows of data:")
    for i, row in enumerate(values[:3]):
        print(f"Row {i}: {row}")
    print("\nColumn headers:")
    if values:
        print(values[0])

except Exception as e:
    print(f"Error accessing spreadsheet: {str(e)}")
    print("Please verify:")
    print("1. The spreadsheet ID is correct")
    print("2. The sheet name is exactly 'Form Responses 1'")
    print("3. The service account has access to the spreadsheet")
    exit(1)

# Predefined zone groupings
zone_groupings = {
    "Mon/Fri": ["Sebilis", "Skyfire"],
    "Wed": ["Plane of Sky", "City of Mist", "Chardok", "Timorous Deep", "Karnor's Castle", "Kithicor Forest", "Lake of Ill Omen"],
    "Sat": ["Plane of Hate", "Plane of Fear"]
}

print("\nZone groupings:")
for day, zones in zone_groupings.items():
    print(f"{day}: {zones}")

# Organize data by group and zone
grouped_data = {group: {zone: [] for zone in zones} for group, zones in zone_groupings.items()}

print("\nProcessing rows:")
for row in values[1:]:  # Skip header row
    print(f"\nProcessing row: {row}")
    if len(row) < 7:
        print(f"Skipping row - too short (length: {len(row)})")
        continue
    if row[6] == "Completed":
        print("Skipping row - marked as completed")
        continue

    zone = row[3]  # Zone column
    print(f"Zone from row: {zone}")
    for group, zones in zone_groupings.items():
        if zone in zones:
            print(f"Found zone {zone} in group {group}")
            grouped_data[group][zone].append(row)

print("\nGrouped data:")
for group, zones in grouped_data.items():
    print(f"\n{group}:")
    for zone, entries in zones.items():
        if entries:
            print(f"  {zone}: {len(entries)} entries")

# Generate markdown file
markdown_output = []
markdown_output.append('---')
markdown_output.append('layout: page')
markdown_output.append('title: Epic Mob Requests')
markdown_output.append('cover-img: /assets/img/targets.webp')
markdown_output.append('subtitle: List of raid target requests')
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
with open('targets.md', 'w') as f:
    f.write('\n'.join(markdown_output))

print("\nMarkdown file 'targets.md' has been generated successfully.")
