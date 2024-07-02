# Election-Result-Scrapper 🗳️📊

This Folder contains a Python script that automates the scraping of election results from the Election Commission of India's website. Using Selenium, it navigates through the site, selects states and constituencies, and saves the results in Election Result folder.

## Features ✨
- **Automated Web Scraping**: Uses Selenium to automate browser interactions.
- **Dynamic Dropdown Handling**: Selects states and constituencies dynamically.
- **Data Extraction**: Extracts election results tables and saves them as CSV files.
- **Progress Tracking**: Uses `tqdm` for a progress bar to track the scraping process.

## Requirements 📋
- Python 3.7+
- `selenium`
- `pandas`
- `tqdm`
- `webdriver_manager`

## Installation 🔧
1. Clone this repository:
    ```bash
    git clone https://github.com/mohit2pal/2024-Lok_Sabha-Data-Analysis.git
    cd 2024-Lok_Sabha-Data-Analysis/Scraping
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage 🚀
1. **Setup the WebDriver**: Ensure you have Chrome installed. The script uses `webdriver_manager` to handle the ChromeDriver setup.
2. **Run the Script**:
    ```bash
    python eci_result_scrapper.py
    ```
