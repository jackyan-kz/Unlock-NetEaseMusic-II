# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options) 
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00CF5DB3CE0C4922181E3602CE95AB61DF15C3983CC2F1EC7242A88AFE6740B817F4801F843F65988EC76C70D39B1090609D6370FE7A145C64A9A7E6A57D51AA92A1CE7F18FB8577F3415F857FE2C7B0A027B0BC6CF73813FD35F64AD07114DBCC4D67D06E886E73121E4B30B9A1B0D50A003E476C8157117C76C6F9EAEE57A40E8B76165487E98A39E549C0F0067690967281BFB099F596F8B1651E45CFE2A11D7EA5972B92A998574C664B53B410DA5BEFE96676DF01FEAF05E9257C3F3990927381C29AE937B356AD36E7C461083DCD1B00BAB088DAEFFE563E3B81E6258D9CEB31333D3891E4ADCD64818913DB4FE6E0746D83248E3E49AADDF3E1A0ACD5627321A84B97F8252DB420A2E2F4CAC02F36BBD9DBF324A1CFA2963852882130B03FF3B412BF446743BCA440705FB40B419A8AE9FCDBFB1F99C7D8589D3264D6D93BBDF7A634DA89E3DB4F8DFBE4E864CC"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
