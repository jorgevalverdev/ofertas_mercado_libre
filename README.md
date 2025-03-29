# Mercado Libre Web Scraper

This project is a web scraper designed to extract offers from the Mercado Libre website and save the data into an Excel file for further analysis.

## Project Structure

### Directory Structure

```
ofertas_mercado_libre/
│
├── README.md
├── requirements.txt
│
├── data/
│   └── processed/
│       └── mercado_libre_ofertas.xlsx
│
├── drivers/
│   └── chromedriver.exe
│
├── env/
│   └── venv_final/
│       └── ... (virtual environment files)
│
└── src/
    ├── __init__.py
    └── web_scrapping/
        ├── __init__.py
        ├── scrapper.py
        └── breakdown.py
```

### Key Files and Directories

- **`src/web_scrapping/scrapper.py`**: The main script that performs the web scraping.
- **`src/web_scrapping/breakdown.py`**: Contains the `Oferta` class used to process individual offers.
- **`data/processed/mercado_libre_ofertas.xlsx`**: The output file where the scraped data is saved.
- **`drivers/chromedriver.exe`**: The ChromeDriver executable required for Selenium.
- **`requirements.txt`**: Lists the Python dependencies for the project.

## Prerequisites

1. **Python**: Ensure Python 3.12 or higher is installed.
2. **Google Chrome**: Install the latest version of Google Chrome.
3. **ChromeDriver**: Download the ChromeDriver version compatible with your Chrome browser and place it in the `drivers/` directory.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Set up a virtual environment:

   ```bash
   python -m venv env/venv_final
   source env/venv_final/Scripts/activate  # On Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the scraper:

   ```bash
   python src/web_scrapping/scrapper.py
   ```

2. The script will:

   - Open the Mercado Libre offers page.
   - Scrape offers from all available pages.
   - Save the data to `data/processed/mercado_libre_ofertas.xlsx`.

3. The output file will be located in the `data/processed/` directory.

## Error Handling

- **TimeoutException**: If the page takes too long to load, the script will print an error message and exit gracefully.
- **General Exceptions**: Any other errors will be logged to the console.

## Notes

- Ensure the `chromedriver.exe` path in `scrapper.py` matches the location of your ChromeDriver.
- The script uses Selenium and BeautifulSoup for web scraping.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
