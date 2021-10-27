from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
if __name__ == "__main__":
    options = Options()
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
    opt = webdriver.ChromeOptions()
    opt.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Chrome(executable_path=r'C:\Users\Ben Fan\Desktop\py\buyPS5-momo\chromedriver.exe' , options=opt)
    driver.set_window_size(1024, 960)
    driver.get("https://www.skyscanner.com.tw/transport/flights-from/tpet/211031/211031/?adults=1&adultsv2=1&cabinclass=economy&children=0&childrenv2=&inboundaltsenabled=false&infants=0&originentityid=27547236&outboundaltsenabled=false&preferdirects=false&preferflexible=false&ref=home&rtn=1")
    
    

    time.sleep(5)

    # 使用 xpath 找到搜尋欄並填入 hello world
    # inputs = driver.find_element(:class, 'chevron-down')
    driver.close
