from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pyautogui
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
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 15)

        self.locator_map = {
            "class"      : By.CLASS_NAME,
            "css"        : By.CSS_SELECTOR,
            "id"         : By.ID,
            "name"       : By.NAME,
            "link"       : By.LINK_TEXT,
            "partial"    : By.PARTIAL_LINK_TEXT,
            "tag"        : By.TAG_NAME,
            "xpath"      : By.XPATH
        }

    def open(self,url):
        self.driver.get(url)

    def waits(self):
        self.driver.implicitly_wait(15)

    def find(self, locator):
        loc = locator.split(",")
        types = loc[0]
        value = loc[1]
        try:
            locator_type = self.locator_map.get(types)
            if locator_type:
                locator = (locator_type, value)
                return self.wait.until(EC.presence_of_element_located(locator))

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
        if el:
            el.clear()
            el.send_keys(text)
        else:
            print('element tidak ditemukan atau tidak dapat diisi teks')
    
    def img(self,locator,img_path):
        el = self.find(locator)
        if el:
            el.send_keys(img_path)
        else:
            print('elemen tidak ditemukan')

    def img_click(self,locator,img_path):
        self.click(locator)
        time.sleep(1)
        pyautogui.write(img_path)
        pyautogui.press('enter')
    
    def click(self, locator):
        el = self.find(locator)
        if el:
            locator_type, locator_value = locator.split(",", 1)
            self.wait.until(EC.element_to_be_clickable((locator_type,locator_value))).click()
        else:
            print('Elemen tidak ditemukan atau tidak bisa di click')
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
        frame = self.find(locator)
        try:
            frame = self.wait.until(EC.frame_to_be_available_and_switch_to_it(frame))
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Failed to switch to frame: {str(e)}")


# driver      = r'env/chromedriver/chromedriver.exe'
# user_data   = r'C:/Users/ADM-IT/AppData/Local/Google/Chrome/User Data'
# profile     = 'profile1'
# browser = SeleniumCore(driver, user_data, profile)
