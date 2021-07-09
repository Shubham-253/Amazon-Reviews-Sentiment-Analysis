import pandas as pd

import base64
from io import BytesIO

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from Amazon_Streamlit import get_URL

st.set_page_config(layout="wide")
st.title("Amazon Reviews Scrapper")

url = st.text_input('Enter the product URL (from Amazon.in only)')
#url='https://www.amazon.in/Lenovo-Ideapad-Windows-GeForce-81LK01QTIN/dp/B092MTLNBB/ref=pd_rhf_dp_s_sspa_dk_rhf_detail_pt_sub_0_1/258-6805332-1093032?_encoding=UTF8&pd_rd_i=B092MTLNBB&pd_rd_r=b31634b9-505b-4978-82e3-b255bcfe1058&pd_rd_w=wTAnh&pd_rd_wg=u5hzQ&pf_rd_p=e15cf8fc-ef83-4ad7-9241-34c5c4e01547&pf_rd_r=JCDT29MBRAQFW6YWJX3Y&refRID=JCDT29MBRAQFW6YWJX3Y&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExTzdNN1UwUDI2VDdFJmVuY3J5cHRlZElkPUEwODM5NjEzM0xaV0xLRzE4UVA0ViZlbmNyeXB0ZWRBZElkPUEwODY2Mjg3M0s2NFZOTVg5RFhFQyZ3aWRnZXROYW1lPXNwX3JoZl9kZXRhaWwmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl&th=1'

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>' #;base64,{b64}
    return href


if url != '':
    try:
        df = get_URL(url)
        st.subheader(" Positive Reponses")
        st.table(df[df['Sentiment']=='pos']['Short_review'].reset_index(drop=True).head(10))
        
        st.subheader(" Negative Reponses")
        st.table(df[df['Sentiment']=='neg']['Short_review'].reset_index(drop=True).head(10))
        
        #download scraped data
        st.markdown(get_table_download_link(df), unsafe_allow_html=True)
        
        #Printing Pie Chart
        plt.style.use('dark_background')
        plt.figure(figsize=(1,1))
        sizes = [df['Sentiment'].value_counts()[0],df['Sentiment'].value_counts()[1],df['Sentiment'].value_counts()[2]]
        labels=['Positive','Neutral','Negative']
        fig1, ax1 = plt.subplots()
        my_color=['Orange','Blue','Green']
        myexplode = [0.1, 0.1,0]
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', explode=myexplode ,colors=my_color)
        ax1.axis('equal')
        st.pyplot(fig1) 
        
    except:
        st.subheader("Invalid URL")