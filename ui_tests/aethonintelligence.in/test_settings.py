from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

API_KEYS_PATH = '/dashboard/settings?tab=api-keys'
BAD_MARKERS = ['404', 'page not found', 'something went wrong', 'application error', 'internal server error']


def test_api_keys_page_loads(logged_in_driver, base_url):
    driver = logged_in_driver
    driver.get(f'{base_url}{API_KEYS_PATH}')
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    assert '/login' not in driver.current_url
    body_text = driver.find_element(By.TAG_NAME, 'body').text
    assert len(body_text.strip()) > 20, 'Page body appears empty'
    lower = body_text.lower()
    for marker in BAD_MARKERS:
        assert marker not in lower, f'Page shows error content: {marker!r}'


def test_api_keys_generate_button_present(logged_in_driver, base_url):
    driver = logged_in_driver
    driver.get(f'{base_url}{API_KEYS_PATH}')
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, 'button'))
    )
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    texts = [b.text.lower() for b in buttons]
    assert any('key' in t or 'create' in t or 'generate' in t or 'new' in t or '+' in t for t in texts)
