from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()
options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
browser = webdriver.Chrome(
    executable_path='./venv/chromedriver.exe',
    options=options,
)
browser.get('http://localhost:8000')

header_text = browser.find_element_by_tag_name('header').text
assert 'django' in header_text

browser.quit()