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
nltk.download('punkt')

def createCloud(text, title, size=(10, 7)):
    # Processing Text
    wordcloud = WordCloud(width=800, height=400,
                          collocations=False
                          ).generate(" ".join(text))

    # Output Visualization
    fig = plt.figure(figsize=size, dpi=80, facecolor='k', edgecolor='k')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=25, color='w')
    plt.tight_layout(pad=0)
    return fig


def top_n_words(text, ngram, n):
    if (ngram == 1):
        vec = CountVectorizer().fit(text)
    else:
        vec = CountVectorizer(ngram_range=(ngram, ngram)).fit(text)

    bag_of_words = vec.transform(text)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq[:n]


def plot_word_freq_chart(word_freq_list):
    x = []
    y = []

    for word, freq in word_freq_list:
        x.append(word)
        y.append(freq)

    data = [go.Bar(
        x=x,
        y=y
    )]

    fig = go.Figure(data=data)
    fig.update_layout(
        title="Top 10 Words",
        xaxis_title="Word",
        yaxis_title="Frequency",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        ),
    )
    fig.update_traces(marker_color='lightsalmon', marker_line_color='navy',
                      marker_line_width=2.5, opacity=0.6)
    #iplot(fig)
    return fig


def pos_tagger(row, tags):
    for word, tag in nltk.pos_tag(nltk.word_tokenize(row)):
        tags.append(tag)


def plot_tag_count(df):
    tags = []
    df["Comment"].apply(lambda row : pos_tagger(row, tags))
    tag_count = {}
    for tag in tags:
        if tag in tag_count:
            tag_count[tag] += 1
        else:
            tag_count[tag] = 1

    tag_count = {k: v for k, v in sorted(tag_count.items(), key=lambda item: item[1])}

    x = []
    y = []
    for tag in tag_count:
        x.append(tag)
        y.append(tag_count[tag])
    x.reverse()
    y.reverse()

    data = [go.Bar(
           x = x,
           y = y
        )]

    fig = go.Figure(data=data)
    fig.update_layout(
        title = "POS Tag Counts",
        xaxis_title = "POS Tag",
        yaxis_title = "Frequency",
        font=dict(
                 family="Courier New, monospace",
                 size=18,
                 color="#2f7f7f"
                )
        )
    fig.update_traces(marker_color='orange', marker_line_color='blue',
                  marker_line_width=2.5, opacity=0.6)
    #iplot(fig)
    return fig


#most common words used in top 10 most liked comments
def common_words_in_most_liked_comments(df):
    sorted_df = df.sort_values("Likes", ascending = False)
    top_10 = sorted_df.nlargest(10, "Likes")
    st.plotly_chart(plot_word_freq_chart(top_n_words(top_10["Comment"], 1, 10)))


def common_words_in_least_liked_comments(df):
    sorted_df = df.sort_values("Likes", ascending = True)
    top_10 = sorted_df.nsmallest(10, "Likes")
    st.plotly_chart(plot_word_freq_chart(top_n_words(top_10["Comment"], 1, 10)))


def length_box_plot(df):
    length = [len(text) for text in df["Comment"]]
    plot = go.Figure()
    plot.add_trace(go.Box(y=length, boxpoints="all", name = "Length", marker_color = 'lightseagreen'))
    #plot.show()
    return plot


def extract_emojis(text, emojis):
    for c in text:
        if c in emoji.UNICODE_EMOJI['en']:
            emojis.append(c)


def plot_emoji_count(df):
    emojis = []
    df["Comment"].apply(lambda row: extract_emojis(row, emojis))

    emoji_count = {}
    for emoji in emojis:
        if emoji in emoji_count:
            emoji_count[emoji] += 1;
        else:
            emoji_count[emoji] = 1

    x = []
    y = []
    for emoji in emoji_count:
        x.append(emoji)
        y.append(emoji_count[emoji])

    data = [go.Bar(
        x=x,
        y=y
    )]

    fig = go.Figure(data=data)
    fig.update_layout(
        title="Emoji Counts",
        xaxis_title="Emoji",
        yaxis_title="Frequency",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#2f7f7f"
        )
    )
    fig.update_traces(marker_color='yellow', marker_line_color='navy',
                      marker_line_width=2.5, opacity=0.6)
    #iplot(fig)
    return fig


def emoji_pie_chart(df):
    emojis = []
    df["Comment"].apply(lambda row: extract_emojis(row, emojis))

    emoji_count = {}
    for emoji in emojis:
        if emoji in emoji_count:
            emoji_count[emoji] += 1;
        else:
            emoji_count[emoji] = 1

    emoji_count = {k: v for k, v in sorted(emoji_count.items(), key=lambda item: item[1])}

    x = []
    y = []
    for emoji in emoji_count:
        x.append(emoji)
        y.append(emoji_count[emoji])

    x.reverse()
    y.reverse()

    fig = go.Figure(
        data=[go.Pie(labels=x[:5], values=y[:5], textinfo='label', textfont_size=30, pull=[0.05, 0, 0, 0, 0])])
    fig.update_traces(marker_line_width=2.5, opacity=0.8)
    #fig.show()
    return fig


def app():
    st.title("Comments Visualizations")
    st.subheader("Enter the Scrapped Comments File Name:")
    file = st.text_input("File Name", placeholder="File Name")
    st.write(type(file))
    df = xa.preprocessing(file)

    st.pyplot(createCloud(df["Comment"], "Comments Word Cloud"))
    st.plotly_chart(plot_word_freq_chart(top_n_words(df["Comment"], 1, 10)))
    st.plotly_chart(plot_word_freq_chart(top_n_words(df["Comment"], 2, 10)))
    st.plotly_chart(plot_word_freq_chart(top_n_words(df["Comment"], 3, 10)))
    st.plotly_chart(plot_tag_count(df))
    common_words_in_most_liked_comments(df)
    common_words_in_least_liked_comments(df)
    st.plotly_chart(length_box_plot(df))
    st.plotly_chart(plot_emoji_count(df))
    st.plotly_chart(emoji_pie_chart(df))


