import requests
from bs4 import BeautifulSoup
import csv

# Seed URLs for the companies
companies = {
    'Voltas': 'https://www.screener.in/company/VOLTAS/consolidated/',
    'Havells': 'https://www.screener.in/company/HAVELLS/consolidated/',
    # 'Blue Star': 'https://www.screener.in/company/BLUESTAR/consolidated/',  # Correct URL
    'Whirlpool': 'https://www.screener.in/company/WHIRLPOOL/consolidated/',
    'Crompton': 'https://www.screener.in/company/CROMPTON/consolidated/',
    'Symphony': 'https://www.screener.in/company/SYMPHONY/consolidated/',
    'Orient Electric': 'https://www.screener.in/company/ORIENTELEC/consolidated/',
}

# Function to extract company ratios
def extract_company_ratios(soup):
    ratios = {}
    
    # Locate the company ratios section
    ratios_div = soup.find('div', class_='company-ratios')
    if ratios_div:
        # Find the unordered list with the id of 'top-ratios'
        ratios_list = ratios_div.find('ul', id='top-ratios')
        if ratios_list:
            # Iterate over each list item to extract name and value
            for item in ratios_list.find_all('li'):
                name = item.find('span', class_='name').text.strip()
                value = item.find('span', class_='nowrap value').text.strip()
                # Store the values in the ratios dictionary
                ratios[name] = value
    
    return ratios

# Prepare CSV file with utf-8 encoding
with open('company_financial_metrics.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write header
    writer.writerow(['Stock Name', 'Market Cap (in Cr)', 'Current Price', 'Stock P/E', 'ROCE', 'ROE'])

    # Loop through each company
    for company_name, company_url in companies.items():
        # Send a request to the webpage
        response = requests.get(company_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract company ratios
            company_ratios_data = extract_company_ratios(soup)
            
            # Prepare the row data
            market_cap = company_ratios_data.get('Market Cap (in Cr)', 'N/A')
            current_price = company_ratios_data.get('Current Price', 'N/A')
            stock_pe = company_ratios_data.get('Stock P/E', 'N/A')
            roce = company_ratios_data.get('ROCE', 'N/A')
            roe = company_ratios_data.get('ROE', 'N/A')
            
            # Write the company data to the CSV
            writer.writerow([company_name, market_cap, current_price, stock_pe, roce, roe])
        else:
            print(f"Failed to retrieve page for {company_name}, status code: {response.status_code}")
