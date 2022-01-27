import streamlit as st
import numpy as np
import pandas as pd
import selenium
from selenium import webdriver
from sklearn.feature_extraction.text import CountVectorizer
import plotly.graph_objects as go
from plotly.offline import iplot
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from time import sleep
import csv
import io
import demoji
from wordcloud import STOPWORDS
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import csv
import io
import pandas as pd
from io import BytesIO
import base64
import os

import commentScrapper
import preprocessing
#import xa2
#import sentimentAnalyzer
#import homePage
#from pyxlsb import open_workbook as open_xlsb

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')





def app():

    st.title("YouTube Comments Scrapper")
    st.subheader("Enter the YouTube Video URL to scrape")
    url = st.text_input("YouTube URL", placeholder = "Enter YouTube URL")
    df = commentScrapper.scrape_youtube_comments(url)
    st.subheader("The Original Scrapped Data:")
    st.write(df)
    
    #no need to preprocess the scrapped data in the scrapper module. We will do the preprocessing in the visualizer and sentimentAnalyzer module
    
    #processed_df = preprocessing.preprocessing(df)
    #preprocessing.remove_emoji(processed_df)
    #st.subheader("After Preprocessing the Scrapped Data:")
    #st.write(processed_df)

    csv = convert_df(df)

    filename = 'comments.csv'

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=filename,
        mime='text/csv',
    )



#app()
