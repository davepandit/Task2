import requests
from bs4 import BeautifulSoup

# Seed URL for Voltas company
url = 'https://www.screener.in/company/VOLTAS/consolidated/'

# Send a request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

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

    # Call the function to get balance sheet stats
    balance_sheet_data = extract_balance_sheet(soup)

    # Print the extracted balance sheet data
    for key, value in balance_sheet_data.items():
        print(f"{key}: {value}")

else:
    print(f"Failed to retrieve page, status code: {response.status_code}")
