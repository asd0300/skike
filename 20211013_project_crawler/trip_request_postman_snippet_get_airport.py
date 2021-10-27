import requests,time
import json



def getAirport(key):
  url = "https://hk.trip.com/flights/graphql/poiSearch"

  payload = json.dumps({
    "operationName": "poiSearch",
    "variables": {
      "key": "{}".format(key),
      "mode": "0",
      "tripType": "OW"
    },
    "extensions": {
      "persistedQuery": {
        "version": 1,
        "sha256Hash": "3c5078329815323617129d575e3ce3bf49c1a89dee3314fd160bcda754c51130"
      }
    }
  })
  headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'referer': 'https://hk.trip.com/hotels/home',
    'cookie': 'cookiePricesDisplayed=TWD; _abtest_userid=c9a403a4-5a35-4ac9-b77e-cda4d88ab996; _gcl_au=1.1.22915204.1634111486; _RSG=kVaUkRhJm2DYFZYojM.Dl8; _RGUID=d0b04eb6-ee7a-47ee-8bcd-f96b728a33e2; _RDG=28bff0fb631abf2dcb1bb119dc6b6dfdc5; ibulocale=zh_hk; _gid=GA1.2.449869172.1634461177; ibu_online_permission_cls_ct=2; ibu_online_permission_cls_gap=1634461178358; IBU_TRANCE_LOG_P=18095419643; IBU_TRANCE_LOG_URL=%2Fhotels%2F; g_state={"i_p":1634548318536,"i_l":2}; cticket=54B8FA2D6995EF0A6A2C871BFCDFE940FD844ABA8FECF942FBC70FAF15930247; ticket_ctrip=bJ9RlCHVwlu1ZjyusRi+ypZ7X2r4+yojQBs5yAteRtJUPMMNOT+SyRpl0pXF5gepAwGHqGujQMZNqu5Np9RRpATD41ZlnhnbAbsjedVc3eKnceYddsVGVumT0zU9Bnivj6BAEPDEIzNRpEGOMN4Hu+MYNlHbby12UHiGvm7YBBvHa6Gv02d8ycPSh5rouc5NqvuPoKhR/wq/X8mU+KhF8QRf+0WyGmPyoc+i/T5BhBgEKcZnLYx+zyBL3/dEcpRyQ6nkk0gQH4+YZlwIb7tckbJsGo/Hp3LPfDiaUziecR8=; DUID=u=25F7AAE4752EAC34609CD6D155357263&v=0; IsNonUser=T; ibu_h5_isquick=1; _combined=transactionId%3D3dd51fde-d03d-42b7-9e03-4ea485778639%26usedistributionchannels%3DTrue%26channel%3DTWSite%26uuid%3D66b1b131-266b-4591-9f74-fe4cce2f705b; Union=AllianceID=18500&SID=446383&OUID=5968_1588917737_20677554da3d837022edc664fd0fa817&SourceID=&AppID=&OpenID=&Expires=1637128277741&createtime=1634536277; ibulanguage=HK; carsearch=residency%3D1%26age%3D30; OsdSessionId=5a2150ae5d534fd8bd4d80e2ae9abc0d; _tp_search_latest_channel_name=hotels; librauuid=Q7AMCkfGHo0aCbmO; IBU_showtotalamt=0; intl_ht1=h4%3D219_48903776%2C219_6112682; hotel=48903776; ibu_online_home_language_match={"isFromTWNotZh":false,"isFromIPRedirect":false,"isFromLastVisited":false,"isRedirect":false,"isShowSuggestion":false,"lastVisited":"https://hk.trip.com?locale=zh-hk"}; _RF1=1.200.7.185; _uetsid=a75bd1402f2811ecacca45fdcb9c1c7c; _uetvid=ecbdcf902cb511eca0e9a92191716a1b; _ga_X437DZ73MR=GS1.1.1634547264.13.1.1634547308.0; _bfa=1.1634111485004.3fwpku.1.1634545222673.1634547264357.13.438; _bfs=1.2; _ga=GA1.2.1003449919.1634111485; _bfi=p1%3D10320668150%26p2%3D10320668150%26v1%3D438%26v2%3D437; cookiePricesDisplayed=TWD; ibulanguage=HK; ibulocale=zh_hk; IBU_FLT_HEAD_INFO=T_X8codPi-7T8IUICcpdEQ==',
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)
  result = response.json()
  resultflight = result['data']['poiSearch']['results']
  # print(resultflight)
  airport = []
  # airportSet = set()
  # for item in resultflight:
  #   if item['childResults']:
  #     for itemChild in item['childResults']:
  #       if itemChild['countryName'] == "日本":
  #         airport.append(itemChild['airportCode'])
  #   else:
  #     # print(item['airportCode'])
  #     if item['countryName'] == "日本":
  #       airport.append(item['airportCode'])
  #   print("ok")
  for item in resultflight:
    if item['childResults']:
      for itemChild in item['childResults']:
        if itemChild['countryName'] == "日本":
          airport.append(itemChild['cityCode'])
    else:
      # print(item['airportCode'])
      if item['countryName'] == "日本":
        airport.append(item['cityCode'])
    print("ok")
  airport = list(filter(None, airport))
  # airportSet = set(airport)
  # print(airport, airportSet)
  time.sleep(3)
  return airport


jpList = ['北海道','尾花澤市','東京','大阪','京都','箱根','和歌山市','金澤','小樽','別府','長崎','宮古島']
cityFList = []
print("1")
for item in jpList: 
  cityFList.extend(getAirport(item))
  # print(airportFList)
cityFListListSet = set(cityFList)
print(cityFListListSet)
jpAirport = ['ITM', 'OKD', 'MSJ', 'KMQ', 'OKI', 'TSJ', 'NRT', 'CTS', 'HND', 'UKB', 'NGO', 'SHI', 'SHM', 'IKI', 'MMY', 'FUJ', 'NGS', 'KIX']
# getAirport(item)
cityFList = ['OBO', 'MSJ', 'KMQ', 'NGS', 'HKD', 'TYO', 'TSJ', 'SHM', 'AKJ', 'OKI', 'IBR', 'KUH', 'NGO', 'MMY', 'FUJ', 'TAK', 'IKI', 'SPK', 'SHI', 'OSA']