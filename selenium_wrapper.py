from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Firefox
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains


class SeleniumWrapper:
    SELECTORS = {"name": By.NAME, "class": By.CLASS_NAME, "id": By.ID, "tag": By.TAG_NAME}

    BROWSERS = {"firefox": Firefox, "chrome": Chrome}

    def __init__(self, browser):
        self.driver: WebDriver = self.BROWSERS[browser]()
        self.wait = WebDriverWait(self.driver, timeout=10)
        self.small_wait = WebDriverWait(self.driver, timeout=2)

    def access_url(self, url):
        self.driver.get(url)

    def get_element(self, selector_name, selector_value, parent=None, small_wait=False):
        if parent is not None:
            return parent.find_element(self.SELECTORS[selector_name], selector_value)
        if small_wait:
            return self.small_wait.until(
                expected.visibility_of_element_located((self.SELECTORS[selector_name], selector_value))
            )
        return self.wait.until(expected.visibility_of_element_located((self.SELECTORS[selector_name], selector_value)))

    def get_elements(self, selector_name, selector_value, parent=None, small_wait=False):
        if parent is not None:
            return parent.find_elements(self.SELECTORS[selector_name], selector_value)
        self.get_element(selector_name, selector_value, parent, small_wait)
        return self.driver.find_elements(self.SELECTORS[selector_name], selector_value)

    def send_keys(self, selector_name, selector_value, keys):
        self.get_element(selector_name, selector_value).send_keys(keys)

    def click(self, selector_name, selector_value):
        self.wait.until(expected.element_to_be_clickable((self.SELECTORS[selector_name], selector_value))).click()

    def right_click(self, selector_name, selector_value):
        element = self.get_element(selector_name, selector_value)
        action_chains = ActionChains(self.driver)
        action_chains.context_click(element).perform()

    def try_call(self, selector_name, selector_value, function, parent=None, small_wait=False):
        try:
            return function(selector_name, selector_value, parent, small_wait)
        except TimeoutException:
            return None
