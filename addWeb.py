import requests
from bs4 import BeautifulSoup
import csv

# Function to extract reported date from a row
def extract_reported_date(row):
    try:
        reported_date = row.find_all('td')[2].text.strip()  # Assuming reported date is in the third column (index 2)
        return reported_date
    except:
        return None

# URL of the website
url = "https://oag.ca.gov/privacy/databreach/list?field_sb24_org_name_value=&field_sb24_breach_date_value%5Bmin%5D=&field_sb24_breach_date_value%5Bmax%5D=&order=created&sort=desc"

# Fetch the content of the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table containing the data breaches
    table = soup.find('table')

    # Initialize list to store filtered detail page links
    detail_page_links = []

    # Extract the rows
    for row in table.find_all('tr')[1:]:  # Skipping the header row
        # Extract reported date
        reported_date = extract_reported_date(row)

        # Check if reported date is within 2019-2023
        if reported_date:
            year = int(reported_date.split('/')[-1])  # Extracting year from date format MM/DD/YYYY
            if year in range(2019, 2024):
                # Get the link to the detail page
                detail_link_tag = row.find_all('td')[0].find('a')
                if detail_link_tag and 'href' in detail_link_tag.attrs:
                    detail_url = f"{detail_link_tag['href']}"
                    detail_page_links.append([detail_url])

    # Path to the CSV file
    csv_file_path = "C:/Users/rsun2/OneDrive/Test.csv"

    # Write data to the CSV file
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Detail Page URL"])  # Write header
        writer.writerows(detail_page_links)  # Write rows
    
    print(f"Data successfully written to {csv_file_path}")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
