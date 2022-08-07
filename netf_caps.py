#import library
import streamlit as st
import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from wordcloud import STOPWORDS

#Wide orientation
st.set_page_config(layout="wide")

#import data
df = pd.read_csv('nflx2.csv')

st.title("Kenali Konten Netflix Lebih Dalam")
col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')

with col2:
    st.image('netflix_logo.jpg', caption='Sumber : https://blog.logomyway.com/netflix-logo/')

with col3:
    st.write(' ')

st.markdown('Netflix adalah layanan yang memungkinkan pengguna menonton tayangan kesukaan di mana pun, kapan pun, dan hampir lewat medium apa pun, seperti smartphone, _smartTV_, tablet, PC, dan laptop. (https://tekno.kompas.com/read/2016/01/07/13085347/Akhirnya.Masuk.Indonesia.Netflix.Itu.Apa.?)')

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
fig = plt.figure()
relye_df = pd.DataFrame(df['release_year'].value_counts())
relye_df.rename(columns={'release_year':'banyak_konten'}, inplace=True)
sns.lineplot(x = relye_df.index, y='banyak_konten', data=relye_df)
plt.xlabel('Tahun rilis')
plt.ylabel('Banyak konten')
plt.title('Banyak konten per tahun rilis')
st.pyplot(fig)

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
    fig1 = plt.figure()
    sns.distplot(df[df['type']=='MOVIE']['runtime'])
    plt.title('Distribusi durasi movie(film)')
    plt.xlabel('Durasi (menit)')
    st.pyplot(fig1)
with col2:
    fig2 = plt.figure()
    sns.distplot(df[df['type']=='SHOW']['runtime'])
    plt.title('Distribusi durasi show(series)')
    plt.xlabel('Durasi (jam)')
    st.pyplot(fig2)

#alternatif
#banyak genre dalam konten
#st.subheader('Banyak genre dalam konten')
#genre_count=[]
#for i in df['genres']:
#    genre_count.append(len(i.split()))
#df['genre_count'] = genre_count
#fig = plt.figure(figsize=(10,8))
#ax = plt.barh(y=df['genre_count'].unique(), width=df['genre_count'].value_counts(), color=['black', 'red', 'green', 'blue', 'cyan'])
#plt.xlabel('Banyak konten')
#plt.ylabel('Banyak genre')
#st.pyplot(fig)

st.subheader("Genre")
fig = plt.figure()
genre_wc = " ".join(i for i in df.genres)
stopwords = set(STOPWORDS)
wordcloud = WordCloud(background_color = "white", stopwords = stopwords).generate(genre_wc)
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.title("Wordcloud genre")
plt.axis("off")
st.pyplot(fig)

#alternatif
#banyak negara yang memproduksi produksi konten
#st.subheader('Banyak negara yang memproduksi konten')
#prod_ctry_count= []
#for i in df['production_countries']:
#   prod_ctry_count.append(len(i.split()))
#fig = plt.figure(figsize=(10,8))
#df['prod_ctry_count'] = prod_ctry_count
#plt.barh(y=df['prod_ctry_count'].unique(), width=df['prod_ctry_count'].value_counts(), color=['red', 'yellow', 'black', 'blue', 'orange'])
#plt.xlabel('Banyak konten')
#plt.ylabel('Banyak negara')
#st.pyplot(fig)

#Wordcloud negara produksi
st.subheader("Negara produksi")
fig = plt.figure()
prodctry_wc = " ".join(i for i in df.production_countries)
stopwords = set(STOPWORDS)
wordcloud = WordCloud(background_color = "white", stopwords = stopwords).generate(prodctry_wc)
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.title("Wordcloud negara produksi")
plt.axis("off")
st.pyplot(fig)

#Sebaran seasons dalam series
st.subheader('Seasons dalam show(series)')
fig = plt.figure()
sns.distplot(df[df['type']=='SHOW']['seasons'])
plt.title('Distribusi seasons show(series)')
plt.xlabel('Jumlah season')
st.pyplot(fig)

#Rata-rata imdb score konten
st.subheader('Skor IMDb')
st.write("Rata-rata skor IMDb movie(film) :",round(df[df['type']=='MOVIE']['imdb_score'].mean(),1))
st.write("Rata-rata skor IMDb show(series) :",round(df[df['type']=='SHOW']['imdb_score'].mean(),1))

#Sebaran votes imdb
st.subheader('Banyak votes di IMDb')
col1,col2 = st.columns(2)
with col1:    
    fig1 = plt.figure()
    sns.distplot(df[df['type']=='MOVIE']['imdb_votes'])
    plt.title('Distribusi banyak votes di IMDb untuk kategori movie(film)')
    plt.xlabel('IMDb votes')
    st.pyplot(fig1)
with col2:
    fig2 = plt.figure()
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

#Hubungan antara runtime dan imdb rating
st.subheader("Hubungan antara durasi dengan rating IMDb")
col1,col2 = st.columns(2)
#movie
with col1:
    fig1=plt.figure()
    plt.scatter(y=df[df['type']=='MOVIE']['imdb_score'], x=df[df['type']=='MOVIE']['runtime'])
    plt.xlabel('Durasi (menit)')
    plt.ylabel('Rating IMDb')
    plt.title('Hubungan antara durasi dan rating imdb film')
    st.pyplot(fig1)
#show
with col2:
    fig2=plt.figure()
    plt.scatter(y=df[df['type']=='SHOW']['imdb_score'], x=df[df['type']=='SHOW']['runtime'])
    plt.xlabel('Durasi (jam)')
    plt.ylabel('Rating IMDb')
    plt.title('Hubungan antara durasi dan rating imdb series')
    st.pyplot(fig2)

st.subheader("Hubungan antara durasi dengan popularitas TMDB")
#movie
col1,col2 = st.columns(2)
with col1:
    fig1=plt.figure()
    plt.scatter(y=df[df['type']=='MOVIE']['tmdb_popularity'], x=df[df['type']=='MOVIE']['runtime'])
    plt.xlabel('Durasi (menit)')
    plt.ylabel('Rating IMDb')
    plt.title('Hubungan antara durasi dan popularitas tmdb film')
    st.pyplot(fig1)
#show
with col2:
    fig2=plt.figure()
    plt.scatter(y=df[df['type']=='SHOW']['tmdb_popularity'], x=df[df['type']=='SHOW']['runtime'])
    plt.xlabel('Durasi (jam)')
    plt.ylabel('Rating IMDb')
    plt.title('Hubungan antara durasi dan popularitas tmdb series')
    st.pyplot(fig2)

st.subheader("Top genre")
#genre dengan skor imdb tertinggi
gn_imdb = df.groupby('genres')['imdb_score'].mean().sort_values(ascending=False).reset_index(name='imdb_score').head(5)
fig=plt.figure() 
sns.barplot(y='genres', x='imdb_score', data=gn_imdb)
plt.title("5 Genre dengan rata-rata rating IMDb tertinggi")
st.pyplot(fig)
#genre dengan  popoularitas tmdb tertinggi
gn_tmdb = df.groupby('genres')['tmdb_popularity'].mean().sort_values(ascending=False).reset_index(name='tmdb_popularity').head(5)
fig=plt.figure() 
sns.barplot(y='genres', x='tmdb_popularity', data=gn_tmdb)
plt.title("5 Genre dengan rata-rata popularitas TMDB tertinggi")
st.pyplot(fig)

st.subheader("Top negara produksi")
#negara produksi dengan skor imdb tertinggi
prctry_imdb = df.groupby('production_countries')['imdb_score'].mean().sort_values(ascending=False).reset_index(name='imdb_score').head(5)
fig=plt.figure() 
sns.barplot(y='production_countries', x='imdb_score', data=prctry_imdb)
plt.title("5 Negara produksi dengan rata-rata rating imdb tertinggi")
st.pyplot(fig)
#negara produksi dengan popularitas tmdb tertinggi
prctry_tmdb = df.groupby('production_countries')['tmdb_popularity'].mean().sort_values(ascending=False).reset_index(name='tmdb_popularity').head(5)
fig=plt.figure() 
sns.barplot(y='production_countries', x='tmdb_popularity', data=prctry_tmdb)
plt.title("5 Negara produksi dengan rata-rata popularitas tmdb tertinggi")
st.pyplot(fig)

st.subheader("Top tahun rilis")
#tahun rilis dengan skor imdb tertinggi
rlyr_imdb = df.groupby('release_year')['imdb_score'].mean().sort_values(ascending=False).reset_index(name='imdb_score').head(5)
fig=plt.figure() 
sns.barplot(x='release_year', y='imdb_score', data=rlyr_imdb)
plt.title("5 Tahun rilis dengan rata-rata rating imdb tertinggi")
st.pyplot(fig)
#tahun rilis dengan popularitas tmdb tertinggi
rlyr_tmdb = df.groupby('release_year')['tmdb_popularity'].mean().sort_values(ascending=False).reset_index(name='tmdb_popularity').head(5)
fig=plt.figure() 
sns.barplot(x='release_year', y='tmdb_popularity', data=rlyr_tmdb)
plt.title("5 Tahun rilis dengan rata-rata popularitas tmdb tertinggi")
st.pyplot(fig)

st.subheader("Top genre & negara produksi")
#genre dan negara produksi dengan skor imdb tertinggi
grpcy_imdb = df.groupby(['genres','production_countries'])['imdb_score'].mean().sort_values(ascending=False).reset_index(name='imdb_score').head(5)
grpcy_imdb['genre & production country'] = grpcy_imdb[['genres','production_countries']].agg('&'.join, axis=1)
fig=plt.figure() 
sns.barplot(x='imdb_score', y='genre & production country', data=grpcy_imdb)
plt.title("5 Genre & Negara produksi dengan rata-rata rating imdb tertinggi")
st.pyplot(fig)
#genre dan negara produksi dengan popularitas tmdb tertinggi
grpcy_tmdb = df.groupby(['genres','production_countries'])['tmdb_popularity'].mean().sort_values(ascending=False).reset_index(name='tmdb_popularity').head(5)
grpcy_tmdb['genre & production country'] = grpcy_tmdb[['genres','production_countries']].agg('&'.join, axis=1)
fig=plt.figure() 
sns.barplot(x='tmdb_popularity', y='genre & production country', data=grpcy_tmdb)
plt.title("5 Genre & Negara produksi dengan rata-rata popularitas tmdb tertinggi")
st.pyplot(fig)

#Rata-rata jam per episode show
st.subheader("Rata-rata jam per episode series")
df['rata-rata jam per season'] = df[df['type']=='SHOW']['seasons']/df[df['type']=='SHOW']['runtime']
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.dropna(inplace=True)
fig=plt.figure()
sns.distplot(df['rata-rata jam per season'])
plt.title('Distribusi rata-rata jam per season')
plt.xlabel('Rata-rata jam per season')
st.pyplot(fig)

#Filter data
st.header("Cari film favoritmu")
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

st.markdown('Sumber data : https://www.kaggle.com/datasets/victorsoeiro/netflix-tv-shows-and-movies')