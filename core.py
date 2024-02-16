from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class SeleniumCore:
    def __init__(self, chromedriver_path, chrome_user_data, profile):
        service = Service(executable_path=chromedriver_path)
        options = webdriver.ChromeOptions()
        options.add_argument(r'--user-data-dir='+chrome_user_data)
        options.add_argument(r'--profile-directory='+profile)
        options.add_experimental_option("detach",True)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def open(self,url):
        self.driver.get(url)

    def find(self, locator):
        loc = locator.split(",")
        type = loc[0]
        value = loc[1]
        try:
            if type == "class":
                locator = (By.CLASS_NAME, value)
            if type == "css":
                locator = (By.CSS_SELECTOR, value)
            if type == "id":
                locator = (By.ID, value)
            if type == "name":
                locator = (By.NAME, value)
            if type == "link":
                locator = (By.LINK_TEXT, value)
            if type == "partial":
                locator = (By.PARTIAL_LINK_TEXT, value)
            if type == "tag":
                locator = (By.TAG_NAME, value)
            if type == "xpath":
                locator = (By.XPATH, value)

            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            try:
                return self.wait.until(EC.visibility_of_element_located(locator))
            except TimeoutException:
                print('all expected condition failed')
                return None
        except NoSuchElementException:
            print("NoSuchElementException occurred")
            return None
        
    def text(self, locator, text):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)
    
    def click(self, locator):
        el = self.find(locator)
        el.click()

    def choose_category(self, locator, list_category):
        self.click(locator)
        categories = list_category.split(",")
        for category in categories:
            loc = (By.XPATH, f'//span[text()="{category}"]')
            try:
                self.click(loc)
            except TimeoutException:
                print(f"TimeoutException: Element {category} not clickable")

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()
    
    def switch_to_frame(self, locator):
        try:
            frame = self.wait.until(EC.frame_to_be_available_and_switch_to_it(locator))
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Failed to switch to frame: {str(e)}")