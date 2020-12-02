# coding=utf-8
from flask import Flask, render_template, jsonify
from flask.globals import request
from selenium import webdriver
import time
from airport_code import AIRPORT_CODE


CITY_LIST = [(c[0], ','.join(c)) for c in AIRPORT_CODE]
CODES = [c[0] for c in AIRPORT_CODE]

def _get_browser():
    CHROME_DRIVER_PATH = './dirver/chromedriver_mac'
    LOG_PATH = '.log/chromedriver.log'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    # return webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
    return webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=chrome_options, service_args=['--verbose', LOG_PATH])

browser = _get_browser()
app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
    return render_template('index.html', city_list=CITY_LIST, airports=AIRPORT_CODE)

@app.route('/tickets')
def get_tickets():
    city1 = request.args.get('c1', '').upper()
    city2 = request.args.get('c2', '').upper()
    start_date = request.args.get('d', '')

    print(city1, city2)
    print('Date: {}, From: {}, To: {}'.format(start_date, city1, city2))
    if city1 not in CODES or city2 not in CODES:
        return jsonify(msg='invalid city'), 400

    URL = "http://www.ceair.com/booking/%s-%s-%s_CNY.html" % (city1, city2, start_date)
    browser.get(URL)
    tickets = _get_tictet()
    return jsonify(tickets=tickets)

def _get_tictet():
    elements = []
    for i in range(10):
        print('Loop: %s' % str(i))
        time.sleep(1)
        elements=browser.find_elements_by_class_name("flight")
        if len(elements) > 1:
            break

    tickets = []
    for el in elements:
        title_list = el.find_element_by_class_name("title").text.replace(' ', '').split("|")
        time_divs = el.find_elements_by_class_name("airport")
        time_list = [t.text.replace('\n', '') for t in time_divs]
        price_divs = el.find_element_by_class_name('detail').find_elements_by_tag_name("dd")
        price_list = [p.text for p in price_divs]
        tickets.append({
            'company': title_list[0],
            'code': title_list[1],
            'direct': title_list[2],
            'price_list': price_list,
            'time_list': time_list,
        })
    return tickets

app.run(debug=True)
