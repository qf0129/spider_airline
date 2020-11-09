from selenium import webdriver
from time import sleep

URL = "http://www.ceair.com/booking/sha-lhw-201114_CNY.html"

CHROME_DRIVER_PATH = './dirver/chromedriver.exe'
LOG_PATH = '.log/chromedriver.log'


def get_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    # browser = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
    return webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_options, service_args=['--verbose', LOG_PATH])
