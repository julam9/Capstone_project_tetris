#import library
import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import base64 
from pathlib import Path  
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

#Wide orientation
st.set_page_config(layout="wide")

#import data
# change the path into desired path
df = pd.read_csv("netlix_data.csv")

#title 
st.markdown("<h1 style='text-align: center; color: red;'>Explore Netflix Dashboard</h1>", unsafe_allow_html=True)

#function to extract image to bytes
def image_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded 
#function to extract bytes to html 
def img_to_html(img_path):
    img_html = "<img src = 'data:image/png; base64, {}' class='img-fluid'>".format(image_to_bytes(img_path))
    return img_html
#netflix logo 
st.markdown("<p style='text-align: center; color:grey; '>"+img_to_html('netflix_logo.jpg')+"</p>", unsafe_allow_html=True)

#markdown 
statista_url = "https://www.statista.com/statistics/250934/quarterly-number-of-netflix-streaming-subscribers-worldwide/"
st.markdown("Netflix is an OTT (Over The Top) streaming platform which has become one of the most favorite streaming platform in the world. Per *[Statista](%s)*, in Q2 2023, Netflix has around 238 million paid subscribers. The growth of netflix is high, especially since COVID-19 which makes people have to stay at home. One of Netflix's strength is the variety of the content. The contents of Netflix are known come from many countries and consists of many genres")

#first section
st.subheader("How many data do you want to see?")
row = st.number_input("Insert a row", min_value=1, max_value=len(df), value=None, step=1, placeholder="Type a number...")
st.dataframe(df.head(row))

# Type of show
fig=plt.figure(figsize=(5,4))
sns.countplot(data=df, x="type", color="red", width=.3).set(title="How many movie and tv show in the data?")
st.pyplot(fig)

# Age certif content 
st.markdown("<h2 style='text-align: center; color: grey;'>Age Certification</h1>", unsafe_allow_html=True)
fig = go.Figure(
    go.Pie(
    labels = df['age_certification'].unique(),
    values = df['age_certification'].value_counts(),
    hoverinfo = "label",
    textinfo = "percent"
))
st.plotly_chart(fig, use_container_width=True)

# Runtime of content 
st.markdown("<h2 style='text-align: center; color: grey;'>Runtime of Content</h1>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:    
    fig1 = plt.figure(figsize=(5, 4))
    sns.histplot(data=df, x=df.query('type == "MOVIE"')['runtime'], color='red')
    plt.title("Movie")
    plt.xlabel('Minute')
    plt.xlim([0, max(df.query('type == "MOVIE"')['runtime'])])
    st.pyplot(fig1)
with col2:
    fig2 = plt.figure(figsize=(5, 4))
    sns.histplot(data=df, x=df.query('type == "SHOW"')['runtime'], color='red')
    plt.title("Show")
    plt.xlabel('Episode')
    plt.xlim([0, max(df.query('type == "SHOW"')['runtime'])])
    st.pyplot(fig2)

# seasons (only for series) 
st.markdown("<h2 style='text-align: center; color: grey;'>Seasons (Show)</h1>", unsafe_allow_html=True)
fig=plt.figure()
sns.histplot(data=df, x='seasons', color='red', bins=10).set(title='Distribution of seasons')
plt.xlim([min(df['seasons']), max(df['seasons'])])
st.plotly_chart(fig, use_container_width=True)

#number of content over the years
st.markdown("<h2 style='text-align: center; color: grey;'>Content over the year</h1>", unsafe_allow_html=True)
fig = plt.figure()
release_year_df = df["release_year"].value_counts().reset_index()
sns.lineplot(data = release_year_df, x = 'release_year', y='count', color = 'red').set(title="Content released per year")
plt.xticks(rotation=45)
plt.ylim([0, max(release_year_df['count'])])
st.plotly_chart(fig, use_container_width=True)

# wordcloud genre 
st.markdown("<h2 style='text-align: center; color: grey;'>Genre Wordcloud</h1>", unsafe_allow_html=True)
genre_text = " ".join(gen for gen in df.genres) 
stopword_genre = set(STOPWORDS)
# Create and generate a word cloud image:
wordcloud_genre = WordCloud(width=1600, height=800, stopwords=stopword_genre).generate(genre_text)
# Display the generated image:  
fig = plt.figure(facecolor='k', figsize=(20, 10))
plt.imshow(wordcloud_genre, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0) 
plt.show()
st.pyplot(fig) 

# wordcloud production country
st.markdown("<h2 style='text-align: center; color: grey;'>Prodcution Countries Wordcloud</h1>", unsafe_allow_html=True)
prodcountry_text = " ".join(gen for gen in df.production_countries)
stopword_prodcountry = set(STOPWORDS)
# Create and generate a word cloud image:
wordcloud_prodcountry = WordCloud(width=1600, height=800, stopwords=stopword_prodcountry).generate(prodcountry_text)
# Display the generated image:
fig=plt.figure(figsize=(20, 10), facecolor="k")
plt.imshow(wordcloud_prodcountry, interpolation='bilinear')
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()
st.pyplot(fig)

# rating and score 
st.markdown("<h2 style='text-align: center; color: grey;'>Rating of Contents</h1>", unsafe_allow_html=True)
col1,col2 = st.columns(2)
with col1:    
    fig1 = plt.figure()
    sns.boxplot(data=df, y='imdb_score', color='red').set(title='Imdb score distribution')
    plt.xlabel('IMDb score')
    st.pyplot(fig1)
with col2:
    fig2 = plt.figure()
    sns.boxplot(data=df, y='tmdb_score', color='red').set(title='Tmdb score distribution')
    plt.xlabel('Tmdb score')
    st.pyplot(fig2)

# Relationship between rating imdb and runtime
st.markdown("<h2 style='text-align: center; color: grey;'>Relationship between Runtime and Imdb Score </h1>", unsafe_allow_html=True)
col1,col2 = st.columns(2)
#movie
with col1:
    fig1=plt.figure()
    sns.scatterplot(data=df.query('type == "MOVIE"'), x='runtime', y='imdb_score', color='red').set(title="Movie")
    st.pyplot(fig1)
#show
with col2:
    fig2=plt.figure()
    sns.scatterplot(data=df.query('type == "SHOW"'), x='runtime', y='imdb_score', color='red').set(title="Show")
    st.pyplot(fig2)

# Relationship between popularity tmdb and runtime 
st.markdown("<h2 style='text-align: center; color: grey;'>Relationship between runtime and Tmdb popularity </h1>", unsafe_allow_html=True)
col1,col2 = st.columns(2)
#movie
with col1:
    fig1=plt.figure()
    sns.scatterplot(data=df.query('type == "MOVIE"'), x='runtime', y='tmdb_popularity', color='red').set(title="Movie")
    st.pyplot(fig1)
#show
with col2:
    fig2=plt.figure()
    sns.scatterplot(data=df.query('type == "SHOW"'), x='runtime', y='tmdb_popularity', color='red').set(title="Show")
    st.pyplot(fig2)

# Highest rated genre
#st.markdown("<h2 style='text-align: center; color: grey;'> Highest Average Rated Genre </h1>", unsafe_allow_html=True)
#col1, col2 = st.columns(2)
# imdb 
#with col1:
#    fig1=plt.figure()
#    top10_imdb_genres = df.groupby('genres')['imdb_score'].mean().sort_values(ascending=False).reset_index().head(10) 
#    st.dataframe(top10_imdb_genres)
# tmdb
#with col2:
#    fig1=plt.figure()
#    top10_tmdb_genres = df.groupby('genres')['tmdb_score'].mean().sort_values(ascending=False).reset_index().head(10) 
#    st.dataframe(top10_tmdb_genres)

# production_countries with highest average imdb score 
#st.markdown("<h2 style='text-align: center; color: grey;'> Highest Average Rated Prodducer Countries </h1>", unsafe_allow_html=True)
#col1, col2 = st.columns(2)
# imdb 
#with col1:
#    top10_imdb_prodcountries = df.groupby('production_countries')['imdb_score'].mean().sort_values(ascending=False).reset_index().head(10) 
#    st.dataframe(top10_imdb_prodcountries)
# tmdb
#with col2:
#    top10_tmdb_prodcountries = df.groupby('production_countries')['tmdb_score'].mean().sort_values(ascending=False).reset_index().head(10)
#    st.dataframe(top10_tmdb_prodcountries)  
    
# average imdb and tmdb score over the years  
st.markdown("<h2 style='text-align: center; color: grey;'> Average Rating Over the Years </h1>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
# imdb 
with col1:
    fig1=plt.figure()
    imdb_year = df.groupby('release_year', as_index=False)['imdb_score'].mean()
    sns.lineplot(data=imdb_year, x='release_year', y='imdb_score', color='red')
    st.pyplot(fig1)
# tmdb
with col2:
    fig2=plt.figure()
    imdb_year = df.groupby('release_year', as_index=False)['tmdb_score'].mean()
    sns.lineplot(data=imdb_year, x='release_year', y='tmdb_score', color='red')
    st.pyplot(fig2)

st.markdown('Data source : https://www.kaggle.com/datasets/victorsoeiro/netflix-tv-shows-and-movies')