import time
import os
from io import StringIO
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

def setup_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver

def open_main_page(driver):
    driver.get("https://results.eci.gov.in/PcResultGenJune2024/index.htm")
    wait = WebDriverWait(driver, 10)
    dropdown = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_Result1_ddlState")))
    return dropdown

def select_state(driver, state_index):
    wait = WebDriverWait(driver, 10)
    dropdown = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_Result1_ddlState")))
    select = Select(dropdown)
    state_name = select.options[state_index].text
    select.select_by_index(state_index)
    return state_name

def get_constituency_options(driver):
    wait = WebDriverWait(driver, 10)
    dropdown = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_Result1_ddlState")))
    select = Select(dropdown)
    return select.options

def select_constituency(driver, constituency_index):
    wait = WebDriverWait(driver, 10)
    dropdown = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ContentPlaceHolder1_Result1_ddlState")))
    select = Select(dropdown)
    constituency_name = select.options[constituency_index].text
    select.select_by_index(constituency_index)
    return constituency_name

def scrape_table(driver, state_name, constituency_name):
    wait = WebDriverWait(driver, 10)
    table_view_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'Constituencywise')]")))
    table_view_link.click()
    time.sleep(3)  # Adjust the sleep time if necessary
    page_source = driver.page_source
    page_source_io = StringIO(page_source)
    tables = pd.read_html(page_source_io)
    df = tables[0]
    parent_directory = os.path.join(os.getcwd(), "Election_Results")
    directory = os.path.join(parent_directory, state_name)
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, f"{constituency_name}.csv")
    df.to_csv(file_path, index=False)

def click_home_button(driver):
    wait = WebDriverWait(driver, 10)
    home_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Home')]")))
    home_button.click()

def main():
    driver = setup_driver()
    condition = False
    try:
        dropdown = open_main_page(driver)
        select = Select(dropdown)
        total_states = len(select.options) - 1  # Exclude the placeholder option
        for state_index in tqdm(range(1, total_states + 1), desc="States"):
            condition = True
            state_name = select_state(driver, state_index)
            constituency_options = get_constituency_options(driver)
            total_constituencies = len(constituency_options) - 1  # Exclude the placeholder option
            for constituency_index in tqdm(range(1, total_constituencies + 1), desc=f"Constituencies in {state_name}", leave=False):
                if condition == True:
                    pass
                else:
                    state_name = select_state(driver, state_index)
                constituency_name = select_constituency(driver, constituency_index)
                scrape_table(driver, state_name, constituency_name)
                click_home_button(driver)  # Click the home button after scraping
                open_main_page(driver)  # Reopen the main page to reset the state dropdown
                condition = False
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
