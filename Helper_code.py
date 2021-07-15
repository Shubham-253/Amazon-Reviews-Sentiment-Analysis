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
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
import math
from time import sleep
from stqdm import stqdm

PATH ="C:\Program Files\chromedriver.exe"

options = Options()
options.headless = True

driver = webdriver.Chrome(PATH,options=options)

def get_URL(url):
    Enter_URL=url
    driver.get(Enter_URL)

    element = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH ,'//*[@id="reviews-medley-footer"]/div[2]/a')))
    element.click()
    strUrl = driver.current_url;
    URL_turn_page= strUrl+ "&pageNumber="
    
    SR = []
    LR = []
    p=math.ceil([int(word) for word in ( driver.find_element_by_xpath('//*[@id="filter-info-section"]/div/span')).text.split("|")[1].split(" ") if word.isdigit()][0]/10)
    print('No. of pages to scrape : ',p)   
    
    for i in stqdm(range(1,p+1)):
        driver.get(URL_turn_page+str(i))
        #t=np.random.randint(1,6, size=1) #to make sleep time variable to avoid bot detection
        #print('sleep time : ',t[0])
        #time.sleep(t)
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


''' ## TO CHECK THE CODE OUTSIDE STREAMLIT JUST RUN THIS FILE ITSELF ##

url=input("enter url : ")
df=get_URL(url)

print(" Positive Reponses")
print(df[df['Sentiment']=='pos']['Short_review'].reset_index(drop=True).head(10))
        
print(" Negative Reponses")
print(df[df['Sentiment']=='neg']['Short_review'].reset_index(drop=True).head(10))
'''