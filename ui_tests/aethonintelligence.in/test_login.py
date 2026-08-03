from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN_PATH = '/login'
LOGIN_COMPANY_PATH = '/login/company'
VALID_EMAIL = 'test@gmail.com'
VALID_PASSWORD = 'test@gmail.com'


def _submit_button(driver):
    try:
        return driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    except Exception:
        return driver.find_element(By.CSS_SELECTOR, 'form button')


def test_login_page_loads(driver, base_url):
    driver.get(f'{base_url}{LOGIN_PATH}')
    email = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    assert email.is_displayed()
    assert password.is_displayed()


def test_login_success(driver, base_url):
    driver.get(f'{base_url}{LOGIN_PATH}')
    email = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    email.send_keys(VALID_EMAIL)
    password.send_keys(VALID_PASSWORD)
    password.send_keys(Keys.RETURN)
    WebDriverWait(driver, 20).until(EC.url_contains('/dashboard'))
    assert '/dashboard' in driver.current_url


def test_login_wrong_password(driver, base_url):
    driver.get(f'{base_url}{LOGIN_PATH}')
    email = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    email.send_keys(VALID_EMAIL)
    password.send_keys('definitely-wrong-password')
    password.send_keys(Keys.RETURN)
    import time; time.sleep(3)
    assert '/dashboard' not in driver.current_url


def test_login_empty_fields(driver, base_url):
    driver.get(f'{base_url}{LOGIN_PATH}')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    submit = _submit_button(driver)
    submit.click()
    import time; time.sleep(1)
    assert '/dashboard' not in driver.current_url


def test_login_company_page_loads(driver, base_url):
    driver.get(f'{base_url}{LOGIN_COMPANY_PATH}')
    email = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    password = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    assert email.is_displayed()
    assert password.is_displayed()
    placeholder = (email.get_attribute('placeholder') or '').lower()
    assert 'yourcompany' in placeholder


def test_login_company_switch_link(driver, base_url):
    driver.get(f'{base_url}{LOGIN_COMPANY_PATH}')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    body_text = driver.find_element(By.TAG_NAME, 'body').text.lower()
    links = driver.find_elements(By.TAG_NAME, 'a')
    hrefs = [(a.get_attribute('href') or '').lower() for a in links]
    has_switch_text = 'individual' in body_text
    has_switch_link = any('/login' in h and 'company' not in h for h in hrefs)
    assert has_switch_text or has_switch_link
