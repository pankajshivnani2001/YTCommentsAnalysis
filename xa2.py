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
import xa
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import emoji


#import commentScrapper
import preprocessing
import visualizer

def app():
    st.title("Comments Visualizations")
    st.subheader("Upload the comments file:")
    st.write("Or Scrape by using the Scrapping Module")

    uploaded_file = st.file_uploader("Choose a file")
    df = pd.read_csv(uploaded_file)
    df.drop(columns=df.columns[0],
            axis=1,
            inplace=True)
    st.write("Original DataFrame")
    st.write(df)


    #url = st.text_input("YouTube URL", placeholder="YouTube URL")
    #df = commentScrapper.scrape_youtube_comments(url)

    df = preprocessing.preprocessing(df)
    st.write("Processed DataFrame")
    st.write(df)

    st.subheader("Word Cloud")
    st.pyplot(visualizer.createCloud(df["Comment"], "Comments Word Cloud"))

    st.subheader("Top 10 Unigrams")
    st.plotly_chart(visualizer.plot_word_freq_chart(visualizer.top_n_words(df["Comment"], 1, 10)))

    st.subheader("Top 10 Bigrams")
    st.plotly_chart(visualizer.plot_word_freq_chart(visualizer.top_n_words(df["Comment"], 2, 10)))

    st.subheader("Top 10 Trigrams")
    st.plotly_chart(visualizer.plot_word_freq_chart(visualizer.top_n_words(df["Comment"], 3, 10)))

    st.subheader("Part-Of-Speech(POS) Tags")
    st.plotly_chart(visualizer.plot_tag_count(df))

    st.subheader("Top 10 words in the most liked comments")
    visualizer.common_words_in_most_liked_comments(df)

    st.subheader("Top 10 words in the least liked comments")
    visualizer.common_words_in_least_liked_comments(df)

    st.subheader("Box Plot about the length of the Comments")
    st.plotly_chart(visualizer.length_box_plot(df))

    st.subheader("Emojis and their Counts")
    st.plotly_chart(visualizer.plot_emoji_count(df))

    st.subheader("Top Emojis")
    st.plotly_chart(visualizer.emoji_pie_chart(df))


#app()
