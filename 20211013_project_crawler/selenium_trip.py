from selenium import webdriver
from selenium.webdriver.chrome.options import Options
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
driver = webdriver.Chrome(chrome_options=opts)


driver.get("https://tc.trip.com/flights/taibei-to-seoul/tickets-tpe-sel?dcity=tpe&acity=sel&ddate=2021-12-03&rdate=2021-12-06&flighttype=ow&class=y&quantity=1&searchboxarg=t")


element = driver.find_element_by_class_name("show-more-icon fi-icon fi-icon_dropdown_line")

print(element)