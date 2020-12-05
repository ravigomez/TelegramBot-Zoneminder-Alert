import sys
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class ZoneMinderScraper():
    def __init__(self):
        super().__init__()

    def __click(self, driver, element_XPATH):
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, element_XPATH))
        )
        ActionChains(driver).move_to_element(
            element).click(element).perform()

    def __setTextbox(self, driver, element_XPATH, valor):
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, element_XPATH))
        )
        element.clear()
        element.send_keys(valor)
        element.send_keys(Keys.TAB)

    def __setCombobox(self, driver, element_XPATH, valor):
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, f'{element_XPATH}/option[text()="{valor}"]'))
        )
        element.click()

    def scrap(self, driver, videoID):

        driver.get(
            f'{os.environ.get("ZONEMINDER_URL")}/zm/index.php?view=video&eid={videoID}&popup=1')

        time.sleep(1)
        self.__setCombobox(driver, '//*[@id="rate"]', '4x')
        time.sleep(1)
        self.__click(driver, '//*[@id="contentForm"]/button')
        time.sleep(1)
        self.__click(driver, '//*[@id="videoTable"]/tbody/tr/td[5]/a[2]')
        time.sleep(1)
        self.__click(driver, '//*[@id="videoTable"]/tbody/tr/td[5]/a[3]')
        time.sleep(1)

    def processVideos(self, IDs):

        gettrace = getattr(sys, 'gettrace', None)
        options = Options()
        if gettrace() is None:
            options.add_argument("--headless")

        driver = webdriver.Remote(
            command_executor=os.environ.get('SELENIUM_DRIVER'),
            desired_capabilities=DesiredCapabilities.CHROME)

        # driver = webdriver.Chrome(
        #    'src/chromedriver/chromedriver', options=options)

        driver.get(
            f'{os.environ.get("ZONEMINDER_URL")}/zm/index.php')

        self.__setTextbox(
            driver, '//*[@id="inputUsername"]', os.environ.get('ZONEMINDER_USER'))
        self.__setTextbox(
            driver, '//*[@id="inputPassword"]', os.environ.get('ZONEMINDER_PASSWORD'))
        self.__click(driver, '//*[@id="loginform"]/button')

        for i in IDs:
            self.scrap(driver, i)

        driver.quit()
