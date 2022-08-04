#import library
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
#from wordcloud import WordCloud
#from wordcloud import ImageColorGenerator
#from wordcloud import STOPWORDS

#Wide orientation
st.set_page_config(layout="wide")

#import data
df = pd.read_csv('nflx2.csv')

st.title("Kenali Konten Netflix Lebih Dalam")
col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')

with col2:
    st.image('netflix_logo.jpg', caption='Logo Netflix, sumber : https://blog.logomyway.com/netflix-logo/')

with col3:
    st.write(' ')

st.subheader("Pilihan Konten")
st.write("Per Juli 2022, terdapat", df['title'].value_counts().sum(), "film/series di Netflix")

#Jumlah konten berdasarkan tipe
st.subheader("Tipe konten")
fig = plt.figure(figsize=(4,1.5))
plt.barh(y=df['type'].unique(), width=df['type'].value_counts())
plt.xlabel('Banyak konten')
plt.ylabel('Tipe konten')
st.pyplot(fig)

#jumlah konten berdasarkan tahun
st.subheader("Jumlah konten berdasarkan tahun rilis")
relye_df = pd.DataFrame(df['release_year'].value_counts())
relye_df.rename(columns={'value_counts':'banyak konten'}, inplace=True)
st.line_chart(relye_df)

#sertifikasi umur konten
st.subheader("Persentase konten berdasarkan sertifikasi umur")
fig = go.Figure(
    go.Pie(
    labels = df['age_certification'].unique(),
    values = df['age_certification'].value_counts(),
    hoverinfo = "label",
    textinfo = "percent"
))
st.plotly_chart(fig)

#durasi konten
st.subheader('Durasi konten')
col1,col2 = st.columns(2)
with col1:    
    fig1 = plt.figure(figsize=(8,6))
    sns.distplot(df[df['type']=='MOVIE']['runtime'])
    plt.title('Distribusi durasi movie(film)')
    plt.xlabel('durasi (menit)')
    st.pyplot(fig1)
with col2:
    fig2 = plt.figure(figsize=(8,6))
    sns.distplot(df[df['type']=='SHOW']['runtime'])
    plt.title('Distribusi durasi show(series)')
    plt.xlabel('durasi (jam)')
    st.pyplot(fig2)

#banyak genre dalam konten
st.subheader('Banyak genre dalam konten')
genre_count=[]
for i in df['genres']:
    genre_count.append(len(i.split()))
df['genre_count'] = genre_count
fig = plt.figure(figsize=(10,8))
ax = plt.barh(y=df['genre_count'].unique(), width=df['genre_count'].value_counts(), color=['black', 'red', 'green', 'blue', 'cyan'])
plt.xlabel('Banyak konten')
plt.ylabel('Banyak genre')
st.pyplot(fig)

#banyak negara yang memproduksi produksi konten
st.subheader('Banyak negara yang memproduksi konten')
prod_ctry_count= []
for i in df['production_countries']:
   prod_ctry_count.append(len(i.split()))
fig = plt.figure(figsize=(10,8))
df['prod_ctry_count'] = prod_ctry_count
plt.barh(y=df['prod_ctry_count'].unique(), width=df['prod_ctry_count'].value_counts(), color=['red', 'yellow', 'black', 'blue', 'orange'])
plt.xlabel('Banyak konten')
plt.ylabel('Banyak negara')
st.pyplot(fig)

#Sebaran seasons dalam series
st.subheader('Banyak Seasons dalam konten show(series)')
fig1 = plt.figure(figsize=(10,8))
sns.distplot(df[df['type']=='SHOW']['seasons'])
plt.title('Distribusi seasons show(series)')
plt.xlabel('Jumlah seasons')
st.pyplot(fig1)

#Rata-rata imdb score konten
st.subheader('Skor IMDb')
st.write("Rata-rata skor IMDb movie(film) :",round(df[df['type']=='MOVIE']['imdb_score'].mean(),1))
st.write("Rata-rata skor IMDb show(series) :",round(df[df['type']=='SHOW']['imdb_score'].mean(),1))

#Sebaran votes imdb
st.subheader('Banyak votes di IMDb')
col1,col2 = st.columns(2)
with col1:    
    fig1 = plt.figure(figsize=(8,6))
    sns.distplot(df[df['type']=='MOVIE']['imdb_votes'])
    plt.title('Distribusi banyak votes di IMDb untuk kategori movie(film)')
    plt.xlabel('IMDb votes')
    st.pyplot(fig1)
with col2:
    fig2 = plt.figure(figsize=(8,6))
    sns.distplot(df[df['type']=='SHOW']['imdb_votes'])
    plt.title('Distribusi banyak votes di IMDb untuk kategori show(series)')
    plt.xlabel('IMDb votes')
    st.pyplot(fig2)

#Rata-rata tmdb score konten
st.subheader('Skor TMDB')
st.write('Rata-rata rating movie(film) :', round(df[df['type']=='MOVIE']['tmdb_score'].mean(),1))
st.write('Rata-rata rating show(series) :', round(df[df['type']=='SHOW']['tmdb_score'].mean(),1))

#Sebaran popularitas tmdb
st.subheader('Popularitas TMDb')
col1,col2 = st.columns(2)
with col1:    
    fig1 = plt.figure(figsize=(8,6))
    sns.distplot(df[df['type']=='MOVIE']['tmdb_popularity'])
    plt.title('Distribusi TMDB popularity untuk kategori movie(film)')
    plt.xlabel('TMDb popularity')
    st.pyplot(fig1)
with col2:
    fig2 = plt.figure(figsize=(8,6))
    sns.distplot(df[df['type']=='SHOW']['tmdb_popularity'])
    plt.title('Distribusi TMDB popularity untuk kategori show(series)')
    plt.xlabel('TMDB popularity')
    st.pyplot(fig2)

#Filter data
st.subheader("Cari film/series berdasarkan judul")
title = st.text_input('Judul film/series')
st.dataframe(df[df['title']== title])

st.subheader("Cari film/series berdasarkan tahun rilis")
st.write("Tahun rilis yang tersedia : ", df['release_year'].min(),"hingga", df['release_year'].max())
year = st.number_input('Masukkan tahun')
st.dataframe(df[df['release_year']== round(year,0)])

st.subheader("Cari film/series berdasarkan genre")
genre = st.selectbox("Pilih genre", df['genres'].unique())
st.dataframe(df[df['genres'] == genre])

st.subheader("Cari film/series berdasarkan negara produksi")
prod_country = st.selectbox("Pilih negara produksi", df['production_countries'].unique())
st.dataframe(df[df['production_countries'] == prod_country])

st.subheader("Cari film/series berdasarkan IMDBb score")
imdb_score = st.slider(label='Film dengan skor imdb >=', min_value=0.0, max_value=9.5)
st.dataframe(df[df['imdb_score'] >= imdb_score])

st.subheader("Cari film/series berdasarkan TMDB score")
tmdb_score = st.slider(label='Film dengan skor tmdb >=', min_value=1.0, max_value=10.0)
st.dataframe(df[df['tmdb_score'] >= tmdb_score])

st.subheader("Cari film/series berdasarkan TMDB popularity")
min_tmdb_pop = df['tmdb_popularity'].min().astype(int)
max_tmdb_pop = df['tmdb_popularity'].max().astype(int)
tmdb_popularity = st.slider(label='Film dengan popularitas tmdb >=', min_value=0.6, max_value=2274.044)
st.dataframe(df[df['tmdb_popularity'] >= tmdb_popularity])

st.write('Data source : https://www.kaggle.com/datasets/victorsoeiro/netflix-tv-shows-and-movies')