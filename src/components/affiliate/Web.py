import pytest
import os
import pprint
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from src.resource.constants import *


class Web(object):

    def __init__(self, Krakken, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, color=DEFAULT_COLOR, browser=DEFAULT_BROWSER):

        self.krakken = Krakken 
        self.logger = self.krakken.logger
        self.x = width
        self.y = height
        self.color = color
        self.browser = browser
        self.username = DEFAULT_UI_USERNAME
        self.password = DEFAULT_UI_PASSWORD

        self.logger.info("Initializing a " + self.browser + " instance")

        if self.browser == 'Chrome':
            self.driver = webdriver.Chrome()
        else:
            # TODO: implement for FF/Safari/IE
            pass 
        try:
            self.driver.set_window_size(self.x, self.y)
            self.logger.info("@Window size now: " + pprint.pformat(self.driver.get_window_size()))
            self.driver.set_page_load_timeout(30)
        except:
            self.logger.warn("Failed to resize, maybe testing locally.")
            pytest.fail("Exception happens during initializing web driver...")

