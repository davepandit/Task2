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

    # Call the function to get company ratios
    company_ratios_data = extract_company_ratios(soup)

    # Print the extracted company ratios
    for key, value in company_ratios_data.items():
        print(f"{key}: {value}")

else:
    print(f"Failed to retrieve page, status code: {response.status_code}")
