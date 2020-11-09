from flask import Flask, render_template
from app_spider.browser import get_browser

app = Flask(__name__)

browser = get_browser()

@app.route('/')
def index():
    URL = "http://www.ceair.com/booking/sha-lhw-201114_CNY.html"
    browser.get(URL)

    return render_template('index.html')


def _get_tictet():
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
    return tickets

app.run(debug=True)
