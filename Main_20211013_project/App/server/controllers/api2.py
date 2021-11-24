import requests
import json

url = "https://www.trivago.com.tw/graphql"

payload = json.dumps({
  "operationName": "getGallery",
  "variables": {
    "input": {
      "nsids": [
        {
          "id": 25306542,
          "ns": 100
        }
      ]
    },
    "pagination": {
      "limit": 30
    },
    "shouldGetAdvertiserLinks": False,
    "advertiserLinksInput": {
      "linkType": "IMAGE",
      "stayPeriod": {
        "arrival": "2021-11-19",
        "departure": "2021-11-20"
      },
      "rooms": [
        {
          "adults": 2,
          "children": []
        }
      ]
    }
  },
  "extensions": {
    "persistedQuery": {
      "version": 1,
      "sha256Hash": "92e168f0849d34d063e0a69a3f3e8e7680d4f62c783a1add689814855967c5a2"
    }
  }
})
headers = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
  'authority': 'www.trivago.com.tw',
  'method': 'POST',
  'path': '/graphql',
  'scheme': 'https',
  'content-type': 'application/json',
  'origin': 'https://www.trivago.com.tw',
  'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'x-trv-app-id': 'HS_WEB_APP',
  'x-trv-cst': '32046,38217,45104,45749,45766,46136,46164,46535,47828,47908,48405,48506,48508,48542,48681,49291,49382,49419,49696,49752,49777,50553,50567,50805,50950,51032,51076,51246,51458,51591,51619,51886,51913,52217,52219,52345,52366,52551,52590,52756,52830,52891,52949,53005,53018,53183,53192,53231,53393,53508,53513,53593,53687,53852,53894,54061,54244,54273,54333,54362,54596,54827,54858,54889,54999,55003,55113,55133,55134,55136,55145,55353,55451,55628,55690,55739,55866,56275-3,56467-1,56477,56578,56633,56861-3,56937-2,57155,57488,57889-2,58038,58205,58324-1,58328-1,58387,58433',
  'x-trv-language': 'zh-Hant-TW',
  'x-trv-platform': 'tw',
  'x-trv-tid': '0882dd417534e3d783b2d8155d',
  'accept': '*/*',
  'accept-encoding': 'gzip, deflate, br',
  'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
  'apollographql-client-name': 'hs-web',
  'apollographql-client-version': 'v93_10_5_ae_f07e1e495a0',
  'Cookie': 'ak_bmsc=2F85A1AEDFDAF2358CE695956720FCB1~000000000000000000000000000000~YAAQhz7cPfZmFyx9AQAAFS15Sw1px02olyRVYUKlW9tZMyMjRwZiQBdJ1IwBWL1Aw+05iMMUhQyxnBOv7pMrihNjEg0qSKt5k7L/nr7z115Fx4qpCHWyIThEyHbya68co7fYYb4gDp0V3RHb/1t8W3LAVeHyMatFs2NUcO3DSH+zmcW1ifDMU0RR0ORMNj8a8LE3Ev+mhAQP5dy+ipXy7uwt9KDQ/EtiArq57gfemsIzofQON2j4Yv8WBpP4Q/Jh9tCg0TcikYZ3lKaHd2vKNIqxXiQHdiZzMbw3GAdqPjn+/v4g09khMeExxKhxNEwCr3vrd6CNkA7cobBWDQmxa287wYomDUvtUJCs4c+pkQOBCqcOdhAme5SNG448OArW; edge_tid=0882dd417534e3d783b2d8155d; edge_tid_s=0882dd417534e3d783b2d8155d'
}

response = requests.request("POST", url, headers=headers, data=payload)
result = response.json()

print(result['data']['getAccommodationDetails']['accommodationDetails'])
