import requests
import fitz  # PyMuPDF
import pandas as pd
from openai import OpenAI

# Function to download the PDF from a URL
def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Your OpenAI API key
api_key = 'Insert API key'
client = OpenAI(api_key=api_key)

# Read the CSV file containing PDF URLs
pdf_dataset_path = r'C:\Users\rsun2\OneDrive\PDF_Test.csv'
pdf_data = pd.read_csv(pdf_dataset_path)

# Limit to first 5 PDFs for this example
pdf_data = pdf_data.head(5)

# List to store the results
results = []

# Process each PDF in the dataset
for index, row in pdf_data.iterrows():
    pdf_url = row['PDF Link']  # use the 'PDF Link' column
    
    # Download the PDF
    pdf_filename = f'downloaded_file_{index}.pdf'
    download_pdf(pdf_url, pdf_filename)
    
    # Extract text from the downloaded PDF
    pdf_text = extract_text_from_pdf(pdf_filename)
    
    # Prepare the prompt with the extracted text
    prompt = f"What date was it detected just give me the date if there is none that just write n/a:\n\n{pdf_text}"
    
    # Send the prompt to the ChatGPT API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-4"
    )
    
    # Extract the response
    response = chat_completion.choices[0].message.content.strip()
    
    # Append the result to the list
    results.append({
        "PDF Link": pdf_url,
        "Detected Date": response
    })

# Create a DataFrame from the results
results_df = pd.DataFrame(results)

# Path to the output CSV file
output_csv_path = r'C:\Users\rsun2\OneDrive\Reported.csv'

# Save the results to the new CSV file
results_df.to_csv(output_csv_path, index=False)

print("Process completed and results saved to Reported.csv.")
