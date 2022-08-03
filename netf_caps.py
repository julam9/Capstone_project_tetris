#import library
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go


#Wide orientation
st.set_page_config(layout="wide")

#import data
df = pd.read_csv('nflx2.csv')

st.title("Kenali Konten Netflix Lebih Dalam")

st.subheader("Pilihan Konten")
st.write("Per Juli 2022, kamu bisa mengakses", df['title'].value_counts().sum(), "film/series di Netflix")

#set the plot
st.subheader("Tipe konten")
fig = plt.figure(figsize=(10,6))
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
    fig1 = plt.figure(figsize=(12,10))
    sns.distplot(df[df['type']=='MOVIE']['runtime'])
    plt.title('Distribusi durasi movie(film)')
    plt.xlabel('durasi (menit)')
    st.pyplot(fig1)
with col2:
    fig2 = plt.figure(figsize=(12,10))
    sns.distplot(df[df['type']=='SHOW']['runtime'])
    plt.title('Distribusi durasi show(series)')
    plt.xlabel('durasi (jam)')
    st.pyplot(fig2)










