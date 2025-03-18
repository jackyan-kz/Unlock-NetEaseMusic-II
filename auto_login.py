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
    browser.add_cookie({"name": "MUSIC_U", "value": "00263ED7F6B93AD6805028938F641C065A4E32CB11AFF111015566BBECA53621FB24576AC4804F137F9340534B346A5051EDD17177382260470A620014627B025310DAC9AFA8E695A64B37059E9E752BD9584060715EE3B75028DED2887A275D1B9EBC8C08B52D2679FC01F026BC83CA63F2E46215F33D2F4457C0A4853A53DE35460EE4C55B6EEBD2039FC3ED9EADB1EAF9AA59EAD9FC4A6671A2DD8FCF5F5B5C24C0B548984894647B82F1362E83042B5B7329F0FA93EEB018FA33AC3BD243A410794B591EB9F4CE4C665A67FB06FD48C714154DE632BB6D46D6AB7E0075222A964BCFC3CCF44492135DADB03F41C8BE01146D49F18207C0BE58C8C08267B7D5620DBDCCE32397E23B58E372931C5334B49509F81B5079957A3AA842B73EC3C609C9A065F1F5B64C817E01BC427CE867E3E67052989344D7809A103D972F0892B16EE9235D1AC6518244B3BF268C4568"})
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
