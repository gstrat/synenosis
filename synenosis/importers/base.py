from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .exceptions import ConnectorError
from selenium.webdriver.common.by import By


class SeleniumConnector(object):
    # How many seconds to wait before a timeout occurs
    timeout = 15

    def __init__(self):
        # self.driver = webdriver.Firefox()
        self.driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true',
                                                        '--ssl-protocol=any'])
        self.driver.set_window_size(1120, 550)

    def login(self, username, password):
        raise NotImplementedError

    def wait_for_id(self, element_id, error_message, timeout=None):
        """ Wait for an id to load """
        if not timeout:
            timeout = self.timeout

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
        except:
            raise ConnectorError(error_message)
        else:
            return element

    def wait_for_link_text(self, link_text, error_message, timeout=None):
        """ Wait for a link text to load """
        if not timeout:
            timeout = self.timeout
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.LINK_TEXT, link_text))
            )
        except:
            raise ConnectorError(error_message)
        else:
            return element