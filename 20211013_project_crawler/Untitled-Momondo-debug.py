#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


# In[2]:


options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
opt = webdriver.ChromeOptions()
opt.add_argument('--user-agent=%s' % user_agent)
driver = webdriver.Chrome(executable_path=r'C:\Users\Ben Fan\Desktop\py\buyPS5-momo\chromedriver.exe' , options=opt)
driver.set_window_size(1024, 960)


# In[3]:


driver.get("https://www.momondo.tw/flight-search/TPE-KIX/2021-10-31?sort=bestflight_a")


# In[4]:


a = driver.find_elements_by_class_name("price-text")


# In[5]:


result = []
for item in a:
    result.append(item.get_attribute('innerHTML'))


# In[6]:


print(result)


# In[7]:


time.sleep(1)


# In[8]:


driver.get("https://www.momondo.tw/flight-search/TPE-KIX/2021-11-01?sort=bestflight_a")


# In[9]:


a = driver.find_elements_by_class_name("price-text")


# In[10]:


result = []
for item in a:
    result.append(item.get_attribute('innerHTML'))


# In[11]:


print(result)


# In[12]:


time.sleep(1)


# In[13]:


driver.get("https://www.momondo.tw/flight-search/TPE-KIX/2021-11-02?sort=bestflight_a")


# In[14]:


a = driver.find_elements_by_class_name("price-text")


# In[15]:


result = []
for item in a:
    result.append(item.get_attribute('innerHTML'))


# In[16]:


print(result)


# In[17]:


time.sleep(1)


# In[ ]:




