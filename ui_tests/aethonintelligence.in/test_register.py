import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

REGISTER_PATH = '/register'


def _submit_button(driver):
    try:
        return driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    except Exception:
        return driver.find_element(By.CSS_SELECTOR, 'form button')


def _retry_stale(driver, action, attempts=4, delay=0.6):
    last_exc = None
    for _ in range(attempts):
        try:
            return action()
        except (StaleElementReferenceException, NoSuchElementException) as exc:
            last_exc = exc
            time.sleep(delay)
    raise last_exc


def test_register_page_loads(driver, base_url):
    driver.get(f'{base_url}{REGISTER_PATH}')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )

    def check():
        email = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        assert email.is_displayed()
        passwords = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
        assert len(passwords) >= 1
    _retry_stale(driver, check)


def test_register_empty_fields_validation(driver, base_url):
    driver.get(f'{base_url}{REGISTER_PATH}')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )

    def submit():
        _submit_button(driver).click()
    _retry_stale(driver, submit)
    time.sleep(1)
    assert 'register' in driver.current_url.lower()


def test_register_invalid_email_format(driver, base_url):
    driver.get(f'{base_url}{REGISTER_PATH}')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )

    def fill_and_submit():
        email = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
        email.send_keys('not-an-email')
        passwords = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
        for pw in passwords:
            pw.send_keys('SomePassw0rd!')
        _submit_button(driver).click()
    _retry_stale(driver, fill_and_submit)
    time.sleep(1)
    assert 'register' in driver.current_url.lower()
