import requests
from bs4 import BeautifulSoup
import csv

# List of companies and their URLs
companies = {
    "Voltas": 'https://www.screener.in/company/VOLTAS/consolidated/',
    "Havells": 'https://www.screener.in/company/HAVELLS/consolidated/',
    "Blue Star": 'https://www.screener.in/company/BLUESTAR/consolidated/',
    "Whirlpool": 'https://www.screener.in/company/WHIRLPOOL/consolidated/',
    "Crompton": 'https://www.screener.in/company/CROMPTON/consolidated/',
    "Symphony": 'https://www.screener.in/company/SYMPHONY/consolidated/',
    "Orient Electric": 'https://www.screener.in/company/ORIENTELEC/consolidated/'
}

# CSV file name
csv_file_name = 'company_balance_sheet_data.csv'

# Function to extract balance sheet data
def extract_balance_sheet(soup):
    balance_sheet = {}

    # Locate the section containing the balance sheet
    balance_sheet_div = soup.find('section', {'id': 'balance-sheet'})
    if balance_sheet_div:
        # Find the table within this section
        table = balance_sheet_div.find('table', class_='data-table')
        if table:
            # Get the header row for identifying months
            header = table.find('thead').find_all('th')
            month_index = None
            
            # Find the index of "Mar 2024"
            for i, month in enumerate(header):
                if month.text.strip() == 'Mar 2024':
                    month_index = i
                    break
            
            # If the month is found, extract the relevant data from tbody
            if month_index is not None:
                for row in table.find('tbody').find_all('tr'):
                    cells = row.find_all('td')
                    if len(cells) > month_index:
                        label = row.find('td', class_='text').text.strip()  # Get the label from the first <td>
                        value = cells[month_index].text.strip()  # Get the value for March 2024
                        # Only include relevant labels
                        relevant_labels = ['Reserves', 'Borrowings', 'Total Liabilities', 'Fixed Assets', 'Investments', 'Total Assets']
                        if label in relevant_labels:
                            balance_sheet[label] = value
    
    return balance_sheet

# Open the CSV file for writing
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    # Write the header row
    header = ['Stock Name', 'Year', 'Reserves', 'Borrowings', 'Total Liabilities', 'Fixed Assets', 'Investments', 'Total Assets']
    writer.writerow(header)

    # Iterate through the companies to scrape data
    for company_name, url in companies.items():
        # Send a request to the webpage
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Call the function to get balance sheet stats
            balance_sheet_data = extract_balance_sheet(soup)

            # Prepare data for CSV
            row = [company_name, '2024']  # Year is fixed as 2024
            row.extend(balance_sheet_data.get(label, '') for label in ['Reserves', 'Borrowings', 'Total Liabilities', 'Fixed Assets', 'Investments', 'Total Assets'])
            
            # Write the data row to the CSV file
            writer.writerow(row)
            print(f"Data for {company_name} written to CSV.")
        else:
            print(f"Failed to retrieve page for {company_name}, status code: {response.status_code}")

print(f"CSV file has been created successfully: {csv_file_name}")
