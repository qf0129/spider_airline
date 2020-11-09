from selenium import webdriver
from time import sleep

URL = "http://www.ceair.com/booking/sha-lhw-201114_CNY.html"

CHROME_DRIVER_PATH = './dirver/chromedriver.exe'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')

browser = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_options, service_args=['--verbose', './chromedriver.log'])
# browser = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
browser.get(URL)

sleep(3)
# browser.refresh()
# browser.set_window_size(1400,800)

elements=browser.find_elements_by_class_name("flight")

tickets = []
for el in elements:
    title_list = el.find_element_by_class_name("title").text.replace(' ', '').split("|")
    time_divs = el.find_elements_by_class_name("airport")
    price_divs = el.find_element_by_class_name('detail').find_elements_by_tag_name("dd")
    price_list = [p.text for p in price_divs]
    tickets.append({
        'company': title_list[0],
        'code': title_list[1],
        'direct': title_list[2],
        'price_list': price_list
    })

for t in tickets:
    print(t)

