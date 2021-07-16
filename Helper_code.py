import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from IPython.display import Image
import datetime
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import math
from time import sleep
from stqdm import stqdm
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

def get_URL(url):
    Enter_URL=url
    driver.get(Enter_URL)

    element = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH ,'//*[@id="reviews-medley-footer"]/div[2]/a')))
    element.click()
    strUrl = driver.current_url;
    URL_turn_page= strUrl+ "&pageNumber="
    
    SR = []
    LR = []
    p=math.ceil(int("".join([i for i in ( driver.find_element_by_xpath('//*[@id="filter-info-section"]/div/span')).text.split("|")[1] if i.isdigit()]))/10)
    print('No. of pages to scrape : ',p)   
    
    for i in stqdm(range(1,p+1)):
        driver.get(URL_turn_page+str(i))

        for j in stqdm(range(1,11)):
            sleep(0.5)
            try:
                if(driver.find_elements_by_xpath("//*[contains(text(), 'From other countries')]")): #for foreign review the path has slight change
                    SR.append(driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[5]/div[3]/div/div['+str(j)+']/div/div/div[2]/span[2]/span').text)
                    LR.append(driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[5]/div[3]/div/div['+str(j)+']/div/div/div[4]/span/span').text)
                else: #for Indian reviews
                    SR.append(driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[5]/div[3]/div/div['+str(j)+']/div/div/div[2]/a[2]/span').text)
                    LR.append(driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[5]/div[3]/div/div['+str(j)+']/div/div/div[4]/span/span').text)
            except NoSuchElementException:
                continue   
            
    d = zip(SR,LR)
    mapped = list(d)
    df = pd.DataFrame(mapped, columns =['Short_review', 'Long_Review'])
    
    def sentiment_scores(sentence): # Vader sentiment analyzer
        sid_obj = SentimentIntensityAnalyzer()
        sentiment_dict = sid_obj.polarity_scores(sentence) 
        
        if sentiment_dict['compound'] >= 0.05 :
            return 'pos'
     
        elif sentiment_dict['compound'] <= - 0.05 :
            return 'neg'
     
        else :
            return 'neutral'

            
    df['Sentiment'] = df['Short_review'].apply(lambda x:sentiment_scores(x)) 

    return df