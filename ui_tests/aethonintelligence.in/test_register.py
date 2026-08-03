from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

REGISTER_PATH = '/register'


def _submit_button(driver):
    try:
        return driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    except Exception:
        return driver.find_element(By.CSS_SELECTOR, 'form button')


def test_register_page_loads(driver, base_url):
    import time
    driver.get(f'{base_url}{REGISTER_PATH}')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    time.sleep(1.5)
    email = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
    assert email.is_displayed()
    passwords = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
    assert len(passwords) >= 1


def test_register_empty_fields_validation(driver, base_url):
    driver.get(f'{base_url}{REGISTER_PATH}')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    submit = _submit_button(driver)
    submit.click()
    import time; time.sleep(1)
    assert 'register' in driver.current_url.lower()


def test_register_invalid_email_format(driver, base_url):
    import time
    driver.get(f'{base_url}{REGISTER_PATH}')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    time.sleep(1.5)
    email = driver.find_element(By.CSS_SELECTOR, "input[type='email']")
    email.send_keys('not-an-email')
    passwords = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
    for pw in passwords:
        pw.send_keys('SomePassw0rd!')
    submit = _submit_button(driver)
    submit.click()
    time.sleep(1)
    assert 'register' in driver.current_url.lower()
