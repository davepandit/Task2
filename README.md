What You Need
Python: Make sure you have Python installed. You can download it from python.org.
Pip: This usually comes with Python, but make sure you can use it to install packages.
Steps to Set Up the Project
Download the Project:

Get the project files from wherever it is stored (like GitHub or a zip file).
Open a Terminal:

If you're using Windows, you can use Command Prompt or PowerShell.
On macOS or Linux, just open the Terminal app.
Navigate to the Project Folder:

Use the cd command followed by the path to the project folder. For example:

```
cd path/to/your/project
```

Create a Virtual Environment:

This keeps your project’s packages separate from other projects. Run:
```
python -m venv venv
```

Activate the Virtual Environment:

Windows:

```
venv\Scripts\activate
```

macOS/Linux:
```
source venv/bin/activate
```

Install Required Packages:

You need requests and beautifulsoup4 to run the scraper. Install them with:
```
pip install requests beautifulsoup4
```

Running the Scraper
Run the Scraping Scripts:

There are different scripts for different tasks. You can run them like this:

```
python scrape_companies.py
```

After running, you’ll get a CSV file with financial data from the Pokémon companies.
Run the Inventory Scraper:

Use the inventory scraper to get balance sheet data:

```
python scrape_inventories.py
```

Deactivating the Virtual Environment
When you’re done, you can deactivate the virtual environment by simply typing:

```
deactivate
```
