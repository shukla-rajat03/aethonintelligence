from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ROUTING_PATH = '/dashboard/routing'
BAD_MARKERS = ['404', 'page not found', 'something went wrong', 'application error', 'internal server error']


def test_routing_page_loads(logged_in_driver, base_url):
    driver = logged_in_driver
    driver.get(f'{base_url}{ROUTING_PATH}')
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )
    assert '/login' not in driver.current_url
    body_text = driver.find_element(By.TAG_NAME, 'body').text
    assert len(body_text.strip()) > 20, 'Page body appears empty'
    lower = body_text.lower()
    for marker in BAD_MARKERS:
        assert marker not in lower, f'Page shows error content: {marker!r}'
