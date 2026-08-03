import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = os.environ.get('BASE_URL', 'https://aethonintelligence.in')
WEBDRIVER_URL = os.environ.get('WEBDRIVER_URL', '')
WEBDRIVER_SESSION_ID = os.environ.get('WEBDRIVER_SESSION_ID', '')


@pytest.fixture(scope='session')
def base_url():
    return BASE_URL.rstrip('/')


@pytest.fixture(scope='function')
def driver():
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--window-size=1920,1080')
    if WEBDRIVER_URL:
        if WEBDRIVER_SESSION_ID:
            chrome_options.set_capability('se:testSessionId', WEBDRIVER_SESSION_ID)
        drv = webdriver.Remote(command_executor=WEBDRIVER_URL, options=chrome_options)
    else:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        drv = webdriver.Chrome(options=chrome_options)
    yield drv
    drv.quit()
