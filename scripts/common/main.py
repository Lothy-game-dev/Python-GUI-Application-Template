import sys
from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_driver():
    # Create new option settings for Chrome WebDriver
    chrome_options = Options()
    # Comment the next line to run with UI, uncomment to run without UI
    chrome_options.add_argument("--headless")
    # Set Service for Chrome WebDriver
    chrome_service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=chrome_service, options=chrome_options)


DRIVER = None


def set_driver(new_driver):
    global DRIVER
    DRIVER = new_driver


def is_on_application():
    return getattr(sys, "frozen", False)


def find_and_click(x_path, delay_time=0):
    if x_path in ("", None):
        return None
    try:
        button = DRIVER.find_element(By.XPATH, x_path)
        DRIVER.execute_script("arguments[0].click();", button)
        if delay_time > 0:
            DRIVER.implicitly_wait(delay_time)
        return button
    except Exception as exc:
        raise Exception("Element not found") from exc


def find_and_click_by_class_name(class_name, delay_time=0):
    if class_name in ("", None):
        return None
    try:
        button = DRIVER.find_element(By.CLASS_NAME, class_name)
        DRIVER.execute_script("arguments[0].click();", button)
        if delay_time > 0:
            DRIVER.implicitly_wait(delay_time)
        return button
    except Exception as exc:
        raise Exception("Element not found") from exc
