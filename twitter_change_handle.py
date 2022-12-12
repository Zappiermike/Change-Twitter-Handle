# selenium 4
from time import sleep
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


def main():
    # 30 calls max per 15 min
    username = input("Please enter your twitter username: ")
    passwd = input("Please enter your twitter password: ")
    new_username = input("Please enter your desired NEW twitter @handle: ")


    driver = login(username, passwd)

    # Get text input field
    input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="typedScreenName"]')))
    save_button = driver.find_element(By.CSS_SELECTOR, "div[data-testid='settingsDetailSave']")
    count = 0
    try:
        while True:
            input_field.clear()
            input_field.send_keys(f"{new_username}")
            save_button.click()
            count += 1
            now = datetime.datetime.now()
            print(f"{now} - Button has been clicked {count} times. Sleeping for 32 seconds...")
            sleep(32)
    except NoSuchElementException:
        print("DONE!")
    except StaleElementReferenceException:
        print("DONE!")
        

def login(username, passwd):
    # Initialize chrome webdriver to twitter's login page
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.set_window_position(0, 0)
    driver.set_window_size(1400, 800)
    driver.get("https://twitter.com/login")

    # Grab the username input text field and pass username
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="text"]')))
    element.send_keys(username)

    # Enter button
    button = driver.find_element("xpath", "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div/span")
    button.click()

    # Grab password input text field on next page
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))).send_keys(passwd)

    # Login Button
    login_button = driver.find_element("xpath", "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div")
    login_button.click()
    sleep(5)

    # Redirect to account settings page
    driver.get("https://twitter.com/settings/screen_name")
    driver.implicitly_wait(3)

    return driver

if __name__ == "__main__":
    main()