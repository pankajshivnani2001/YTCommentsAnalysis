import streamlit as st
import pandas as pd
import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
import plotly.graph_objects as go
from plotly.offline import iplot
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk.stem import WordNetLemmatizer
import plotly.graph_objects as go
import numpy as np
nltk.download('averaged_perceptron_tagger')
 nltk.download('sentiwordnet')

def freq_words_in_clusters(cluster_word_map, cluster_number):
    words = cluster_word_map[cluster_number]
    freq = {word:0 for word in words}
    for word in words:
        freq[word] += 1
    sorted_freq = sorted(freq.items(), key=lambda kv: -1*kv[1])
    #top_20 = [key[0] for key in sorted_freq]
    return sorted_freq


def plot_word_freq_chart(word_freq_list):
    x = []
    y = []

    for word, freq in word_freq_list:
        x.append(word)
        y.append(freq)

    data = [go.Bar(
        x=y,
        y=x,
        orientation='h'
    )]

    fig = go.Figure(data=data)
    fig.update_layout(
        title="Top Words",
        xaxis_title="Word",
        yaxis_title="Frequency"
    )
    fig.update_traces(marker_color='lightgreen', marker_line_color='navy',
                      marker_line_width=2.5, opacity=0.6)
    #iplot(fig)
    return fig


def get_tokens_pos_tag(words):#words contain word and its freq
    words_pos = nltk.pos_tag([word[0] for word in words])
    res = []
    for word_pos in words_pos:
        if word_pos[1].startswith('J'):
            res.append([word_pos[0], wn.ADJ])
        elif word_pos[1].startswith('N'):
            res.append([word_pos[0], wn.NOUN])
        elif word_pos[1].startswith('R'):
            res.append([word_pos[0],wn.ADV])
        elif word_pos[1].startswith('V'):
            res.append([word_pos[0], wn.VERB])
    return res


def get_word_sentiment(word, pos):  # 0 neutral, 1 positive, -1 negative, -2 not found
    lemmatizer = WordNetLemmatizer()
    lemma = lemmatizer.lemmatize(word, pos=pos)
    if not lemma:
        return -2

    synsets = wn.synsets(word, pos=pos)
    if not synsets:
        return -2

    synset = synsets[0]
    swn_synset = swn.senti_synset(synset.name())

    if (swn_synset.pos_score() - swn_synset.neg_score() > 0):
        return 1
    elif (swn_synset.pos_score() - swn_synset.neg_score() < 0):
        return -1
    else:
        return 0


def cluster_sentiment(cluster_top_words):

    words_pos = get_tokens_pos_tag(cluster_top_words)
    sentiments = 0
    for word_pos in words_pos:
        word = word_pos[0]
        pos = word_pos[1]
        sentiment = get_word_sentiment(word, pos)
        if sentiment != -2:
            sentiments += sentiment
    return sentiments



def app():
    st.title("Text Clustering Using K-Means")
    st.subheader("Upload the comments file:")
    st.write("Or Scrape by using the Scrapping Module")

    uploaded_file = st.file_uploader("Choose a file")
    df = pd.read_csv(uploaded_file)
    df.drop(columns=df.columns[0],
            axis=1,
            inplace=True)
    st.subheader("Original DataFrame")
    st.write(df)

    processed_df = preprocessing.preprocessing(df)
    preprocessing.remove_emoji(processed_df)
    st.subheader("Processed DataFrame")
    st.write(processed_df)

    comments = df['Comment'].values  # returns an array of comments

    tf_idf_vectorizer = TfidfVectorizer()
    tf_idf = tf_idf_vectorizer.fit_transform(comments)

    kmeans = KMeans(n_clusters=3, init="k-means++", random_state=1)
    kmeans.fit(tf_idf)

    # assigning each word to its cluster
    cluster_word_map = {0: [], 1: [], 2: []}
    for i in range(len(kmeans.labels_)):
        comment = comments[i]
        for word in comment.split():
            cluster_word_map[kmeans.labels_[i]].append(word)

    st.subheader("Cluster 1 Frequent Words")
    st.plotly_chart(plot_word_freq_chart(freq_words_in_clusters(cluster_word_map, 0)[:20]))

    st.subheader("Cluster 2 Frequent Words")
    st.plotly_chart(plot_word_freq_chart(freq_words_in_clusters(cluster_word_map, 1)[:20]))

    st.subheader("Cluster 3 Frequent Words")
    st.plotly_chart(plot_word_freq_chart(freq_words_in_clusters(cluster_word_map, 2)[:20]))

    sentiment_cluster1 = cluster_sentiment(freq_words_in_clusters(cluster_word_map,0)[:20])
    sentiment_cluster2 = cluster_sentiment(freq_words_in_clusters(cluster_word_map,1)[:20])
    sentiment_cluster3 = cluster_sentiment(freq_words_in_clusters(cluster_word_map,2)[:20])



    cluster_counts = np.unique(kmeans.labels_, return_counts=True)
    labels = ["Cluster 1: " + str(sentiment_cluster1), "Cluster 2: " + str(sentiment_cluster2),
              "Cluster 3: " + str(sentiment_cluster3)]

    st.subheader("Cluster Sentiments Pie Chart")

    fig = go.Figure(data=
                    [go.Pie(labels=labels,
                            values=cluster_counts[1])])
    fig.update_layout(title="Cluster Sentiment Scores")
    fig.update_traces(marker_line_width=2.5, opacity=0.8)

    st.plotly_chart(fig)


