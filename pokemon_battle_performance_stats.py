import requests
from bs4 import BeautifulSoup

def scrape_battle_performance_stats(base_url):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    battle_stats = {}
    
    # Find the table containing the battle performance stats
    stats_table = soup.find('table', {'class': 'data-table'})  # Adjust the class as necessary
    rows = stats_table.find_all('tr')

    # Extract headers from the first row
    stats_headers = [header.text.strip() for header in rows[0].find_all('th')]
    
    for i in range(2, len(rows)):  # Start from the second row
        row = rows[i]
        for j, stat_name in enumerate(stats_headers[1:]):  # Skip the first header
            value = row.find_all('td')[j].text.strip()
            # Check if stat_name exists, if not, initialize it
            if stat_name not in battle_stats:
                battle_stats[stat_name] = {}
            if value:  # Only assign if value is present
                battle_stats[stat_name][f'Mar 20{i}'] = value
    
    return battle_stats

# Example usage
if __name__ == "__main__":
    base_url = 'https://example.com/pokemon_stats'  # Replace with the actual URL
    voltas_battle_performance = scrape_battle_performance_stats(base_url)
    
    print(voltas_battle_performance)
