from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_PATH = '/login'
VALID_EMAIL = 'test@gmail.com'
VALID_PASSWORD = 'test@gmail.com'


def _submit_button(driver):
    try:
        return driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    except Exception:
        return driver.find_element(By.CSS_SELECTOR, 'form button')


def test_debug_login_dom(driver, base_url):
    import time
    driver.get(f'{base_url}{LOGIN_PATH}')
    time.sleep(5)
    url = driver.current_url
    source = driver.page_source
    assert False, f"URL={url}\nSOURCE={source[:3000]}"


def test_login_page_loads(driver, base_url):
    driver.get(f'{base_url}{LOGIN_PATH}')
    email = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    assert email.is_displayed()
    assert password.is_displayed()


def test_login_success(driver, base_url):
    driver.get(f'{base_url}{LOGIN_PATH}')
    email = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    email.send_keys(VALID_EMAIL)
    password.send_keys(VALID_PASSWORD)
    password.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(EC.url_contains('/dashboard'))
    assert '/dashboard' in driver.current_url


def test_login_wrong_password(driver, base_url):
    driver.get(f'{base_url}{LOGIN_PATH}')
    email = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    email.send_keys(VALID_EMAIL)
    password.send_keys('definitely-wrong-password')
    password.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(lambda d: True)
    import time; time.sleep(2)
    assert '/dashboard' not in driver.current_url


def test_login_empty_fields(driver, base_url):
    driver.get(f'{base_url}{LOGIN_PATH}')
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    submit = _submit_button(driver)
    submit.click()
    import time; time.sleep(1)
    assert '/dashboard' not in driver.current_url
