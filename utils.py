#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Libraries

from selenium import webdriver # exe to simulate browser
from selenium.webdriver.common.keys import Keys # to send data for website
from webdriver_manager.chrome import ChromeDriverManager # to install exe
from selenium.webdriver.chrome.options import Options # set options to broser
from selenium.webdriver.support.ui import WebDriverWait # wait conditions to scrap data
from selenium.webdriver.support import expected_conditions as EC # set conditions
from selenium.webdriver.common.by import By # way to scrap data
from os import remove
import pandas as pd # read and write excel
import datetime # set today
import time


# set Headless tab
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--window-size=1920,1080")

# set the day
hj = datetime.datetime.now()
hj = hj.strftime("%d%m%Y")


# In[2]:


def connect_page():
    # set drive
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),options=chrome_options)
    # get the page
    driver.get("https://www.anbima.com.br/pt_br/informar/sistema-reune.htm")
    return driver


# In[3]:


def connect_page_web():
    # set drive
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    # get the page
    driver.get("https://www.anbima.com.br/pt_br/informar/sistema-reune.htm")
    return driver


# In[4]:


def set_iframe(driver):
    # get the iframes
    frame = driver.find_elements_by_tag_name("iframe")
    # choose iframe
    driver.switch_to.frame(frame[0])
    return driver


# In[5]:


def choose_data(data,driver):
    # Find data element
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.NAME, "Dt_Ref")))
    elem = driver.find_element_by_name('Dt_Ref')
    # Send keys to data element
    elem.clear()
    elem.send_keys(data)


# In[6]:


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


# In[7]:


def choose_visualization(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='escolha']")))
    radio = driver.find_elements_by_name("escolha")
    radio[1].click()


# In[8]:


def choose_ext(ext,driver):
    # choose to extension
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value= '" + ext +  "']")))
    driver.find_element_by_css_selector("input[type='radio'][value= '" + ext +  "']").click()


# In[9]:


def donwload_file(driver):
    # Donwload the file
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "img[name='Consultar']")))
    driver.find_element_by_css_selector("img[name='Consultar']").click()


# In[10]:


def read_clean_write(hj):
    # read data
    data = pd.read_csv('REUNE_Acumulada_%s.csv'%(hj),
                           skiprows=[i for i in range(0,3)],
                           encoding="Latin-1",sep = ";")
    # clean data
    data_clean = data[data.columns[~data.columns.isin(['Unnamed: 1'])]]
    data_clean["data"] = datetime.date.today()
    data_clean_filter = data_clean[['CETIP','Tipo','Preço Médio','Faixa de Volume','data']]
    # write data
    data_old = pd.read_excel('base.xlsx')
    data_new = data_old.append(data_clean_filter)
    data_new.to_excel('base.xlsx',index=False)
    # removinda old data
    remove('REUNE_Acumulada_%s.csv'%(hj))


# In[13]:


def get_index(data = hj,index="CRA",ext = "csv"):
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
    # Sleep code
    time.sleep(5)
    # join the database
    try:
        read_clean_write(data)
    except:
        print("Nao ha dados para esse dia")

# In[14]:        
        
def loop_data(start_date,end_date):
    datas = pd.date_range(start=start_date,end=end_date)
    for data in datas:
        current_data = data.strftime("%d%m%Y")
        utils.get_index(data = current_data)