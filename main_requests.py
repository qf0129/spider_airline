
import requests

URL = 'http://www.ceair.com/otabooking/flight-search!doFlightSearch.shtml'

headers = {
    "Host": "www.ceair.com",
    "Connection": "keep-alive",
    "Content-Length": "440",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "http://www.ceair.com",
    "Referer": "http://www.ceair.com/booking/sha-lhw-201114_CNY.html?seriesid=d43b5fe0226e11ebb42a0ff5e35d51d6",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "ceairWebType=new; smidV2=20201109110405783bf2a5637c576f6f16223b940f136f0010b95342f5c2160; gr_user_id=d27a28d8-6928-48f9-8cbd-e4b1c50711b1; grwng_uid=e4972c04-6b36-473b-b7cf-2fcb1eac5b27; Webtrends=dee59b17.5b3a41bdcb84b; language=zh_CN; ecrmWebtrends=58.32.3.101.1604892307239; user_ta_session_id=e0120439-b2eb-41cb-aa86-95cadd01a131; _ga=GA1.2.1903080830.1604892309; _gid=GA1.2.322076021.1604892309; user_cookie=true; JSESSIONID=zUFeKTNfOmUrl+K+tEmgS3li.laputaServer6; 84bb15efa4e13721_gr_session_id=9448e521-a01c-4f1d-b8c0-be137d44d689; 84bb15efa4e13721_gr_session_id_9448e521-a01c-4f1d-b8c0-be137d44d689=true; _gat=1; _gat_UA-80008755-11=1",
}

data = {
    '_': 'd43b5fe0226e11ebb42a0ff5e35d51d6',
    'searchCond': {"adtCount":1,"chdCount":0,"infCount":0,"currency":"CNY","tripType":"OW","recommend":False,
        "reselect":"", "page":"0", "sortType":"a", "sortExec":"a", "seriesid":"d43b5fe0226e11ebb42a0ff5e35d51d6", "version":"A.1.0",
        "segmentList":[
            {"deptCd":"SHA","arrCd":"LHW","deptDt":"2020-11-14","deptAirport":"","arrAirport":"","deptCdTxt":"上海","arrCdTxt":"兰州","deptCityCode":"SHA","arrCityCode":"LHW"}
        ]}
}

ret = requests.post(URL, headers=headers, data=data)
# import pdb; pdb.set_trace()
print(ret.json())
