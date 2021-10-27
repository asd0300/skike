# import os
# import time
import threading,json
# from fake_useragent import UserAgent
# from bs4 import BeautifulSoup
# import pandas as pd
import requests

HEADERS = {
    'Cookie':'cookiePricesDisplayed=TWD; ibulanguage=HK; ibulocale=zh_hk; IBU_FLT_HEAD_INFO=T_X8codPi-7T8IUICcpdEQ==',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'referer': 'https://hk.trip.com/flights/taibei-to-osaka/tickets-tpe-osa?FlightWay=OW&class=Y&Quantity=1&ChildQty=0&BabyQty=0&dcity=tpe&acity=osa&ddate=2022-01-04',
    'cookie': 'cookiePricesDisplayed=TWD; _abtest_userid=c9a403a4-5a35-4ac9-b77e-cda4d88ab996; _gcl_au=1.1.22915204.1634111486; _RSG=kVaUkRhJm2DYFZYojM.Dl8; _RGUID=d0b04eb6-ee7a-47ee-8bcd-f96b728a33e2; _RDG=28bff0fb631abf2dcb1bb119dc6b6dfdc5; intl_ht1=h4%3D219_6112682; hotel=26562709; ibulanguage=HK; ibulocale=zh_hk; _gid=GA1.2.449869172.1634461177; ibu_online_permission_cls_ct=2; ibu_online_permission_cls_gap=1634461178358; Union=AllianceID=1272710&SID=3456924&OUID=WegoAdsTW_CU&SourceID=&AppID=&OpenID=&Expires=1637053193499&createtime=1634461193; IBU_TRANCE_LOG_P=18095419643; IBU_TRANCE_LOG_URL=%2Fhotels%2F; g_state={"i_p":1634548318536,"i_l":2}; IBU_FLT_HEAD_INFO=T_X8codPi-7T8IUICcpdEQ==; _RF1=59.120.195.65; _uetsid=a75bd1402f2811ecacca45fdcb9c1c7c; _uetvid=ecbdcf902cb511eca0e9a92191716a1b; _bfa=1.1634111485004.3fwpku.1.1634519136449.1634523550046.7.167; _bfs=1.1; _combined=transactionId%3Da19b6f4d-4598-4534-8989-5bdfa137d74b%26usedistributionchannels%3DTrue%26channel%3DTWSite%26uuid%3D66b1b131-266b-4591-9f74-fe4cce2f705b; _ga_X437DZ73MR=GS1.1.1634523549.7.1.1634523550.0; _bfi=p1%3D10320667452%26p2%3D10320667452%26v1%3D167%26v2%3D166; _ga=GA1.2.1003449919.1634111485; _dc_gtm_UA-109672825-6=1; _gat_UA-109672825-3=1d',
    'Connection':'keep-alive',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept':'*/*',
    'Content-Type':'application/json',
    'Cache-Control':'no-cache',
    'Vary':'Accept-Encoding',
    'x-gate-region':'SHAXY',
    'x-frame-options':'SAMEORIGIN',
    'x-xss-protection':'1; mode=block',
    'x-content-type-options':'nosniff',
    'x-download-options':'noopen'
}
# cookies = {'enwiki_session': '17ab96bd8ffbe8ca58a78657a918558'}

def crawler_url_next(url):
    """design for get many NEXT url"""
    pid_next =[]
    print("URL:", url)
    try:
        jd = json.loads('{"operationName":"intlFlightListSearch","variables":{"request":{"Head":{"Currency":"TWD","ExtendFields":{"SpecialSupply":"false"}},"mode":0,"searchNo":1,"criteriaToken":"","productKeyInfo":"null","searchInfo":{"tripType":"OW","cabinClass":"YS","searchSegmentList":[{"dCityCode":"TPE","aCityCode":"OSA","dDate":"2022-01-04"}],"travelerNum":{"adult":1,"child":0,"infant":0},"openRtMergeSearch":"false"}}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"d1d4e8962c73c4adc3a0f667f315b550f1d4f1228ad264da65e6aa51110d21a8"}}}')
        # r = requests.get(url, headers=HEADERS, cookies=cookies)
        r = requests.post(url, headers=HEADERS, json=jd)
        print(jd)
        print("OK")
        return pid_next
    except Exception as e:
        print("ERROR:", url, e)


crawler_url_next("https://hk.trip.com/flights/graphql/intlFlightListSearch")