import os
import json
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

try:
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print("No data found in the specified range.")
    else:
        with open('targets.md', 'w') as file:
            # Write the front matter
            file.write("---\n")
            file.write("layout: page\n")
            file.write("title: Target Requests\n")
            file.write("cover-img: /assets/img/targets.webp\n")
            file.write("subtitle: List of Target Requests\n")
            file.write("---\n\n")

            # Start the card container
            file.write('<div class="card-container">\n')

            for row in values:
                # Use the second item in the row as a class name
                class_name = row[2].lower().replace(" ", "-")
                file.write(f'  <div class="card {class_name}">\n')
                file.write('    <ul>\n')
                # Skip the first column (timestamp) and write each remaining item as a list item
                for item in row[1:]:
                    file.write(f'      <li>{item}</li>\n')
                file.write('    </ul>\n')
                file.write('  </div>\n')  # End the card

            # End the card container
            file.write('</div>\n')

        print("Data successfully written to targets.md with front matter")

except Exception as e:
    print(f"Error accessing spreadsheet: {str(e)}")
    exit(1)
