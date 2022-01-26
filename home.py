import streamlit as st
import xa, xa2, sentimentAnalyzer, homePage, kmeans




pages = {"Home" : homePage,
         "Scrapper" : xa,
         "Visualizer" : xa2,
         "Sentiment Analysis" : sentimentAnalyzer,
         "K-Means Clustering Analysis" : kmeans
         }

option = st.sidebar.selectbox(
    "What would you like to open?",
    ("Home", "Scrapper", "Visualizer", "Sentiment Analysis", "K-Means Clustering Analysis")
)


page = pages[option]
page.app()