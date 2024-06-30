import os
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

def click_home_button(driver):
    wait = WebDriverWait(driver, 10)
    home_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Home')]")))
    home_button.click()

def verify_files():
    driver = setup_driver()
    try:
        dropdown = open_main_page(driver)
        select = Select(dropdown)
        total_states = len(select.options) - 1  # Exclude the placeholder option
        print(f"Total states found: {total_states}")  # Debug statement
        click_home_button(driver)
        all_files_exist = True

        for state_index in tqdm(range(1, total_states + 1), desc="States"):
            state_name = select_state(driver, state_index)
            constituency_options = get_constituency_options(driver)
            total_constituencies = len(constituency_options) - 1  # Exclude the placeholder option
            print(f"Total constituencies in {state_name}: {total_constituencies}")  # Debug statement

            state_folder_path = os.path.join(os.getcwd(), "Election_Results", state_name)
            if not os.path.exists(state_folder_path):
                print(f"Missing folder for State: {state_name}")
                all_files_exist = False
                continue

            state_files = []
            for constituency_index in tqdm(range(1, total_constituencies + 1), desc=f"Constituencies in {state_name}", leave=False):
                constituency_name = constituency_options[constituency_index].text
                file_path = os.path.join(state_folder_path, f"{constituency_name}.csv")
                if not os.path.exists(file_path):
                    print(f"Missing file for State: {state_name}, Constituency: {constituency_name} - {file_path}")
                    all_files_exist = False
                else:
                    state_files.append(file_path)

            if all_files_exist:
                print(f"All files are present for State: {state_name}. Files found:")
                for file in state_files:
                    print(file)
            
            click_home_button(driver)

        if all_files_exist:
            print("All files are present.")
        else:
            print("Some files are missing.")
    finally:
        driver.quit()

if __name__ == "__main__":
    verify_files()
