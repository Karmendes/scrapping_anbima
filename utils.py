#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Libraries

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

# set Headless tab
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--window-size=1920,1080")


# In[3]:


def connect_page():
    # set drive
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),options=chrome_options)
    # get the page
    driver.get("https://www.anbima.com.br/pt_br/informar/sistema-reune.htm")
    return driver


# In[4]:


def connect_page_web():
    # set drive
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    # get the page
    driver.get("https://www.anbima.com.br/pt_br/informar/sistema-reune.htm")
    return driver


# In[5]:


def set_iframe(driver):
    # get the iframes
    frame = driver.find_elements_by_tag_name("iframe")
    # choose iframe
    driver.switch_to.frame(frame[0])
    return driver


# In[6]:


def choose_data(data,driver):
    # Find data element
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.NAME, "Dt_Ref")))
    elem = driver.find_element_by_name('Dt_Ref')
    # Send keys to data element
    elem.clear()
    elem.send_keys(data)


# In[7]:


def choose_index(index,driver):
    # find index element
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.TAG_NAME, "option")))
    all_options = driver.find_elements_by_tag_name("option")
    # choose index element
    for option in all_options:
        print("Value is: %s" % option.get_attribute("value"))
        if option.get_attribute("value") == index:
            option.click()


# In[8]:


def choose_visualization(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='escolha']")))
    radio = driver.find_elements_by_name("escolha")
    radio[1].click()


# In[9]:


def choose_ext(ext,driver):
    # choose to extension
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value= '" + ext +  "']")))
    driver.find_element_by_css_selector("input[type='radio'][value= '" + ext +  "']").click()


# In[10]:


def donwload_file(driver):
    # Donwload the file
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img[name='Consultar']")))
    driver.find_element_by_css_selector("img[name='Consultar']").click()


# In[11]:


def get_index(data,index="CRA",ext = "xls"):
    # get page
    driver = connect_page()
    print("get page ok")
    # set iframe
    driver = set_iframe(driver)
    print("set frame ok")
    # choose data
    choose_data(data,driver)
    print("choose data ok")
    # choose index
    choose_index(index,driver)
    print("choose index ok")
    # choose visualization
    choose_visualization(driver)
    print("choose visu ok")
    # choose ext
    choose_ext(ext,driver)
    # download
    donwload_file(driver)

