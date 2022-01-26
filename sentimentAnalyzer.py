import streamlit as st
from textblob import TextBlob
import preprocessing
import commentScrapper
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.graph_objects as go
from plotly.offline import iplot
import pandas as pd

def polarity_convert(x):
    if x < 0:
        return "Negative"
    if x > 0:
        return "Positive"
    else:
        return "Neutral"


def sentiment_from_TB(df):
    positive = 0
    negative = 0
    neutral = 0

    for i in df["Sentiment(TB)"].values:
        if i == "Positive":
            positive += 1
        elif i == "Negative":
            negative += 1
        elif i == "Neutral":
            neutral += 1

    return [positive, negative, neutral]


def sentiment_from_VS(row):
    si_analyzer = SentimentIntensityAnalyzer()
    polarity_score = si_analyzer.polarity_scores(row)['compound']
    if polarity_score >= 0.05:
        return "Positive"
    elif polarity_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"


def sentiment_pie(sentiments):
    x = ["Positive", "Negative", "Neutral"]

    fig = go.Figure(
        data=[go.Pie(labels=x, values=sentiments, textinfo='label', textfont_size=15)])
    fig.update_traces(marker_line_width=2.5, opacity=0.8)
    # fig.show()
    return fig


def positive_from_VS(row):
    si_analyzer = SentimentIntensityAnalyzer()
    polarity_score = si_analyzer.polarity_scores(row)['pos']
    return polarity_score * 100;


def negative_from_VS(row):
    si_analyzer = SentimentIntensityAnalyzer()
    polarity_score = si_analyzer.polarity_scores(row)['neg']
    return polarity_score * 100;


def neutral_from_VS(row):
    si_analyzer = SentimentIntensityAnalyzer()
    polarity_score = si_analyzer.polarity_scores(row)['neu']
    return polarity_score * 100;


def sentiment_from_VS2(df):
    positive = 0
    negative = 0
    neutral = 0

    for i in df["Sentiment(VS)"].values:
        if i == "Positive":
            positive += 1
        elif i == "Negative":
            negative += 1
        elif i == "Neutral":
            neutral += 1

    return [positive, negative, neutral]


def compare_sentiments(sentiments1, sentiments2):
    fig = go.Figure(data = [
        go.Bar(name = "TextBlob Analysis", x = ["Positive", "Negative", "Neutral"], y = sentiments1, marker_color = "indianred"),
        go.Bar(name = "Vader Analysis", x = ["Positive", "Negative", "Neutral"], y = sentiments2, marker_color = "lightsalmon")
    ])
    fig.update_layout(barmode = "group")
    return fig



def app():
    try:
        st.title("Youtube Comments Sentiment Analysis")
        #st.subheader("Enter the YouTube URL:")

        #url = st.text_input("YouTube URL", placeholder="YouTube URL")
        # df = commentScrapper.scrape_youtube_comments(url)

        st.subheader("Upload the comments file:")
        st.write("Or Scrape by using the Scrapping Module")

        uploaded_file = st.file_uploader("Choose a file")
        df = pd.read_csv(uploaded_file)
        df.drop(columns=df.columns[0],
                axis=1,
                inplace=True)
        st.write("Original DataFrame")
        st.write(df)


        df = preprocessing.preprocessing(df)
        df = preprocessing.remove_emoji(df)

        temp_df = df.copy(deep=True)

        st.subheader("The Scrapped and Preprocessed comments are:")
        st.write(df)

        df["Sentiment(TB)"] = df["Comment"].apply(lambda row : TextBlob(row).sentiment.polarity)
        df["Sentiment(TB)"] = df["Sentiment(TB)"].apply(lambda row : polarity_convert(row))

        st.subheader("Comments with the Sentiments(Using TextBlob):")
        st.write(df)

        sentiments1 = sentiment_from_TB(df)
        st.subheader("Overall Sentiments of the Comments(Using TextBlob):")
        st.plotly_chart(sentiment_pie(sentiments1))


        temp_df["Sentiment(VS)"] = temp_df["Comment"].apply(lambda row : sentiment_from_VS(row))
        temp_df["Positive %"] = temp_df["Comment"].apply(lambda row: positive_from_VS(row))
        temp_df["Negative %"] = temp_df["Comment"].apply(lambda row: negative_from_VS(row))
        temp_df["Neutral %"] = temp_df["Comment"].apply(lambda row: neutral_from_VS(row))
        st.subheader("Comments with the Sentiments(Using VADER):")
        st.write(temp_df)

        sentiments2 = sentiment_from_VS2(temp_df)

        st.subheader("Overall Sentiments of the Comments(Using VADER):")
        st.plotly_chart(sentiment_pie(sentiments2))

        st.subheader("Comparing TextBlob Predictions with Vader Predictions:")
        st.plotly_chart(compare_sentiments(sentiments1, sentiments2))

    except:
        pass

