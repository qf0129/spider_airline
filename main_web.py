# coding=utf-8
from flask import Flask, render_template, jsonify
from flask.globals import request
from selenium import webdriver
import time


CITY_LIST = (("上海", "sha"), ("北京", "pek"), ("沈阳", "she"), ("福州", "foc"), ("广州", "can"), ("深圳", "szx"), ("海口", "hak"), ("襄樊", "xfn"), ("长沙", "csx"), ("常德", "cgd"), ("浦东", "pvg"), ("丹东", "ddg"), ("锦州", "juz"), ("杭州", "hgh"), ("宁波", "ngb"), ("天津", "tsn"), ("南昌", "khn"), ("郑州", "cgo"), ("重庆", "ckg"), ("长春", "cgq"), ("昆明", "kmg"), ("青岛", "tao"), ("烟台", "ynt"), ("常州", "czx"), ("成都", "ctu"), ("贵阳", "kwe"), ("温州", "wnz"), ("厦门", "xmn"), ("太原", "tyn"), ("南京", "nkg"), ("大连", "dlx"), ("宜昌", "yih"), ("北海", "bhy"), ("晋江", "jjn"), ("三亚", "syx"), ("合肥", "hfe"), ("西安", "sia"), ("武汉", "wuh"), ("徐州", "xuz"), ("湛江", "zha"), ("济南", "tna"), ("广汉", "ghn"), ("大同", "dat"), ("黄山", "txn"), ("桂林", "kwl"), ("兰州", "lhw"), ("延吉", "ynj"), ("延安", "eny"), ("九江", "jiu"), ("安康", "aka"), ("南宁", "nng"), ("伯力", "khv"), ("汉中", "hzg"), ("长治", "ciu"), ("榆林", "uyn"), ("黄岩", "hyn"), ("安庆", "aqc"), ("汕头", "swa"), ("赣州", "kow"), ("朝阳", "chg"), ("万县", "wxn"), ("包头", "bav"), ("南阳", "nny"), ("沙市", "shs"), ("吉林", "jil"), ("西昌", "xic"), ("银川", "inc"), ("珠海", "zuh"), ("黑河", "hek"), ("衡阳", "hny"), ("庐山", "luz"), ("铜仁", "ten"), ("拉萨", "lxa"), ("洛阳", "lya"), ("汉城", "sel"), ("西宁", "xnn"), ("衢州", "juz"), ("香港", "hkg"), ("临沂", "lyi"), ("南充", "nao"), ("南通", "ntg"), ("达县", "dax"), ("恩施", "enh"), ("澳门", "mfm"), ("台北", "tpe"), ("柳州", "lzh"), ("丹山", "hsn"), ("宜宾", "ybp"), ("梁平", "lia"), ("丽江", "ljg"), ("赤峰", "cif"), ("绵阳", "mig"), ("广元", "gys"), ("无锡", "wux"), ("吉安", "knc"), ("通辽", "tgo"), ("潍坊", "wef"), ("威海", "weh"), ("绵阳", "mig"), ("珠海", "zuh"), ("盐城", "ynz"), ("烟台", "ynt"), ("泸州", "lzo"), ("昆明", "kmg"), ("敦煌", "dnh"), ("和田", "htn"), ("喀什", "khg"), ("义乌", "yiw"), ("高雄", "khh"), ("澳门", "qmp"), ("九寨沟", "jzh"), ("呼和浩特", "het"), ("哈尔滨", "hrb"), ("张家界", "dyg"), ("海拉尔", "hld"), ("佳木斯", "jmu"), ("库尔勒", "krl"), ("连云港", "lyg"), ("乌鲁木齐", "urc"), ("牡丹江", "mdg"), ("石家庄", "sjw"), ("攀枝花", "pzi"), ("齐齐哈尔", "ndg"), ("阿勒泰", "aat"), ("阿克苏", "aku"), ("嘉峪关", "jgn"), ("武夷山", "wus"), ("锡林浩特", "xil"), ("克拉玛依", "kry"), ("山海关", "shp"), ("景德镇", "jdz"))
CITY_DICT = {c[1]: c[0] for c in CITY_LIST}

def _get_browser():

    URL = "http://www.ceair.com/booking/sha-lhw-201114_CNY.html"

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
    return render_template('index.html', city_list=CITY_LIST)

@app.route('/tickets')
def get_tickets():
    city1 = request.args.get('c1', '').lower()
    city2 = request.args.get('c2', '').lower()
    start_date = request.args.get('d', '')

    print('Date: {}, From: {}, To: {}'.format(start_date, city1, city2))
    if city1 not in CITY_DICT.keys() or city2 not in CITY_DICT.keys():
        return jsonify(msg='invalid city'), 400

    URL = "http://www.ceair.com/booking/%s-%s-%s_CNY.html" % (city1, city2, start_date)
    browser.get(URL)
    tickets = _get_tictet()
    return jsonify(tickets=tickets)

def _get_tictet():
    elements = []
    for i in range(5):
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
