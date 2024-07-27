import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup

# Function to extract first PDF link from detail page
def extract_first_pdf_link(detail_url):
    try:
        # Send a GET request to the URL
        response = requests.get(detail_url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all <a> tags (links) in the page
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and href.endswith('.pdf'):
                    return href  # Return the first PDF link found
            
        else:
            print(f"Failed to retrieve {detail_url}. Status code: {response.status_code}")
    
    except requests.RequestException as e:
        print(f"Error extracting PDF link from {detail_url}: {e}")
    
    return None

# Path to the input CSV file with website URLs
input_csv_file = "C:/Users/rsun2/OneDrive/Test.csv"

# Path to the output CSV file for PDF links
output_csv_file = "C:/Users/rsun2/OneDrive/PDF_Test.csv"

# Read URLs from input CSV
try:
    df = pd.read_csv(input_csv_file)
    detail_page_urls = df['Detail Page URL'].tolist()[:12]  # Limit to first 10 URLs
except Exception as e:
    print(f"Error reading input CSV file: {e}")
    detail_page_urls = []


pdf_links = []

# Process each detail page URL
for url in detail_page_urls:
    pdf_link = extract_first_pdf_link(url)
    if pdf_link:
        pdf_links.append([pdf_link])
    else:
        pdf_links.append([""])

# Write PDF links to output CSV
try:
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["PDF Link"])
        writer.writerows(pdf_links)
    print(f"PDF links successfully written to {output_csv_file}")
except Exception as e:
    print(f"Error writing PDF links to output CSV file: {e}")
