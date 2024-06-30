from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from io import StringIO

# Set up the Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Open the webpage
    driver.get("https://results.eci.gov.in/PcResultGenJune2024/index.htm")

    # Wait for the page to load completely
    driver.implicitly_wait(10)

    # Locate the dropdown element by its ID
    dropdown = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_Result1_ddlState")

    # Create a Select object
    select = Select(dropdown)

    # Select the first option (index 1 because index 0 is the placeholder "Select State Wise")
    select.select_by_index(1)

    # Wait for the new page to load completely
    time.sleep(5)  # Adjust the sleep time if necessary

    # Locate the new dropdown element by its ID
    new_dropdown = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_Result1_ddlState")

    # Create a Select object for the new dropdown
    new_select = Select(new_dropdown)

    # Select the first option (index 1 because index 0 is the placeholder "Select Constituency")
    new_select.select_by_index(1)

    # Wait for the new page to load completely
    time.sleep(5)  # Adjust the sleep time if necessary

    # Locate the "Constituency Wise Table View" link by its href attribute
    table_view_link = driver.find_element(By.XPATH, "//a[@href='ConstituencywiseU011.htm']")

    # Click on the "Constituency Wise Table View" link
    table_view_link.click()

    # Wait for the new page to load completely
    time.sleep(5)  # Adjust the sleep time if necessary

    # Get the page source and read the table using pandas
    page_source = driver.page_source

    # Wrap the page source in a StringIO object
    page_source_io = StringIO(page_source)

    # Read the table using pandas
    tables = pd.read_html(page_source_io)

    # Assuming the table you want is the first one
    df = tables[0]

    # Save the dataframe to a CSV file
    df.to_csv('election_results.csv', index=False)

finally:
    # Close the browser
    driver.quit()
