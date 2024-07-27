import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# URL of the website
url = "https://oag.ca.gov/privacy/databreach/list"

# Fetch the content of the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table containing the data breaches
    table = soup.find('table')

    # Extract the headers
    headers = [header.text for header in table.find_all('th')]

    # Extract the rows
    rows = []
    for row in table.find_all('tr')[1:]:  # Skipping the header row
        cells = [cell.text.strip() for cell in row.find_all('td')]
        
        # Assuming the reported date is in the first cell (adjust index if needed)
        if cells:
            reported_date_str = cells[2]  # Adjust the index based on the correct column
            try:
                reported_date = datetime.strptime(reported_date_str, '%m/%d/%Y')
                if datetime(2019, 1, 1) <= reported_date <= datetime(2023, 12, 31):
                    rows.append(cells)
            except ValueError:
                continue  # Skip rows with invalid dates

    # Path to the CSV file
    csv_file_path = "C:\\Users\\rsun2\\OneDrive\\ChatData.csv"

    # Write data to the CSV file
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers
        writer.writerows(rows)  # Write rows
    
    print(f"Data successfully written to {csv_file_path}")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
