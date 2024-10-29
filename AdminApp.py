import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)
from PIL import Image
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

import Sentiment
import Topic

import sqlite3
conn = sqlite3.connect("Data.db") # db - database
cursor = conn.cursor() # Cursor object

# ======= Read Data ==========
df = pd.read_sql_query("SELECT * FROM Hotels;", conn)
df2 = pd.read_sql_query("SELECT * FROM Reviews;", conn)

# Page configuration
st.set_page_config(
    page_title="Hotel Admin Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded")

image = Image.open('Images/logo12.png')
st.image(image)

# ================================
if "page" not in st.session_state:
    st.session_state.page = 0
if "name" not in st.session_state:
    st.session_state.name = ""

def nextpage(hotel_name):
    st.session_state.page += 1 # Go to next page
    st.session_state.name = hotel_name

def restart(): st.session_state.page = 0 # Go back to beginning

# ================= Trigger Dashboard Screen ======================
placeholder = st.empty()
def dashboard_widgets(hotel_name):
    nextpage(hotel_name)

# SQL
def get_all(name: str):
    """Fetch all rows from reviews table from a provided hotel name"""
    response = cursor.execute("""SELECT * FROM Reviews
                                        WHERE name='{}';""".format(name))
    return response.fetchall()
def get_sentimet(name: str, sentiment: str):
    """Fetch all rows from reviews table that belong to a provided hotel name and sentiment"""
    response = cursor.execute("""SELECT * FROM Reviews
                                        WHERE name='{}' and Review_Sentiment='{}';""".format(name, sentiment))
    return response.fetchall()
def get_topic(name: str, topic: str):
    """Fetch all rows from reviews table that belong to a provided hotel name and topic"""
    response = cursor.execute("""SELECT * FROM Reviews
                                        WHERE name='{}' and Topics='{}'
                                        ORDER BY RANDOM()
                                        LIMIT 3;""".format(name, topic))
    return response.fetchall()
# ================ Page 1 ==================
if st.session_state.page == 0:

    with placeholder.container():

        st.subheader("Are you a hotel business owner?")
        st.caption("Access realtime analysis of reviews on your hotel...")

        tab1, tab2 = st.tabs(["Search and View", "Dont Find Your Hotel? Click Here"])
        with tab1: # Search and view
            search_input = st.text_input(label="see",label_visibility="hidden",placeholder="Type hotel name to search", value="")

            # ===============================
            # Filter the dataframe using masks
            m1 = df["name"].str.contains(search_input)
            m2 = df["province"].str.contains(search_input)
            df_search = df[m1 | m2]

            N_cards_per_row = 3
            if search_input:
                for n_row, row in df_search.reset_index().iterrows():
                    i = n_row%N_cards_per_row
                    if i==0:
                        st.write("---")
                        cols = st.columns(N_cards_per_row, gap="large")
                    # draw the card
                    with cols[n_row%N_cards_per_row]:
                        #st.caption(f"{row['Evento'].strip()} - {row['Lugar'].strip()} - {row['Fecha'].strip()} ")
                        st.caption(f"{row['city'].strip()}, - {row['province'].strip()}")
                        if st.button(f"**{row['name'].strip()}**"):
                            dashboard_widgets(row['name'])
        with tab2: # Add new

            col1, col2, col3 = st.columns([2,6,2])
            with col2:
                st.caption("If you don't find your hotel after searching. We can help you get onboarded easily.")

            col1, col2, col3 = st.columns([2,6,2])
            with col2:
                hotel_name = st.text_input('Hotel name', placeholder="Type hotel name to search")
                
                if st.button("Add Hotel"):
                    pass

# ================ Page 2 ==================
elif st.session_state.page == 1:
    with placeholder.container():

        getall = get_all(name=st.session_state.name)

        c1, c2, c3 = st.columns([5,6,4])

        with c1:
             if st.button("Back"):
                  restart()
        with c2:
            st.header(body="Reviews Summary Dashboard")
            st.caption(unsafe_allow_html=True,body=f"<b>{getall[0][0]}</b>")
            st.caption(body=f"{getall[0][3]}, {getall[0][4]}, {getall[0][5]}.")

        # Total number of reviews
        reviews = 'Total Reviews'
        number = len(getall)
        _ = '100K'
        st.metric(label=reviews, value=number, delta=None)
        st.write("------------------------------------------------------------")
        st.subheader("Sentiment analysis")
        c1, c2, c3 = st.columns(3)
        with c1: # Positve Reviews
            get_positive = get_sentimet(name=st.session_state.name,sentiment='Positive')
            st.metric(label="Positive Reviews", value=len(get_positive), delta = str(round((len(get_positive) / len(getall)) * 100))+'%')
        with c2: # Neutral Reviews
            get_positive = get_sentimet(name=st.session_state.name,sentiment='Neutral')
            st.metric(label="Neutral Reviews", value=len(get_positive), delta = str(round((len(get_positive) / len(getall)) * 100))+'%')
        with c3: # Negative Reviews
            get_positive = get_sentimet(name=st.session_state.name,sentiment='Negative')
            st.metric(label="Negative Reviews", value=len(get_positive), delta = str(round((len(get_positive) / len(getall)) * 100))+'%')
        # Pie Chart
        df_hotel=df2[df2['name'] == st.session_state.name]
        df_Sentiments=df_hotel['Review_Sentiment'].value_counts().to_frame().reset_index()
        fig = go.Figure([go.Pie(labels=df_Sentiments['Review_Sentiment'], values=df_Sentiments['count'],hole=0.2,marker_colors=px.colors.sequential.RdBu)])
        fig.update_traces(hoverinfo='label+percent', textinfo='value+percent', textfont_size=12,insidetextorientation='radial')
        st.plotly_chart(fig, use_container_width=True)
        st.write("------------------------------------------------------------")
        st.subheader("Word compositions")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.caption(unsafe_allow_html=True,body="A <b>Wordcloud</b> of commonly used words in reviews on your hotel.\n\nThe Bigger the word the more it is used.")
        with c2: # Word Cloud
            extras = ["Hotel","seattle","hyatt","san","francisco","orleans","diego","hampton","orlando","florida","chicago","philadelphia","atlanta",\
            "us","waikiki"]
            stop_words = list(STOPWORDS).extend(extras)
            wordcloud = WordCloud(colormap = 'magma',background_color = "white", stopwords = stop_words, width = 400, height = 400).generate(str(df_hotel['review']+df_hotel['title']).replace("hotel","").replace("Hotel",""))
            plt.rcParams['figure.figsize'] = (2, 2)
            plt.axis('off')
            plt.imshow(wordcloud, interpolation = "bilinear")
            st.pyplot(use_container_width=True)
        st.write("------------------------------------------------------------")
        st.subheader("Topic analysis")
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Others", "Guest Complaints and Hotel Issues", "Positive Guest Experiences and Hotel Amenities", "Noise and Comfort Considerations in Accommodations", "Hotel Guest Feedback and Interactions"])

        with tab1:
            get_topic1 = get_topic(name=st.session_state.name,topic="Others")
            for i in range(len(get_topic1)):
                    st.caption(unsafe_allow_html=True, body='<b>'+get_topic1[i][1]+'</b>'+'\n\n'+str(get_topic1[i][2]))
                    st.write("------------------------------------------------------------")
        with tab2:
            get_topic2 = get_topic(name=st.session_state.name,topic="Guest Complaints and Hotel Issues")
            for i in range(len(get_topic2)):
                    st.caption(unsafe_allow_html=True, body='<b>'+get_topic2[i][1]+'</b>'+'\n\n'+str(get_topic2[i][2]))
                    st.write("------------------------------------------------------------")
            if len(get_topic2) != 0:
                c1, c2, c3 = st.columns(3)
                with c2:
                    df2_hotel=df2[(df2['name'] == st.session_state.name) & (df2['Topics'] == "Guest Complaints and Hotel Issues")]
                    df_sentiment=df2_hotel['Review_Sentiment'].value_counts().to_frame().reset_index()

                    fig = go.Figure(go.Bar(
                        x=df_sentiment['Review_Sentiment'],y=df_sentiment['count'],
                        marker={'color': df_sentiment['count'], 
                        'colorscale': 'Viridis'},  
                        text=df_sentiment['count'],
                        textposition = "outside",
                    ))
                    st.plotly_chart(fig, use_container_width=True)
        with tab3:
            get_topic3 = get_topic(name=st.session_state.name,topic="Positive Guest Experiences and Hotel Amenities")
            for i in range(len(get_topic3)):
                    st.caption(unsafe_allow_html=True, body='<b>'+get_topic3[i][1]+'</b>'+'\n\n'+str(get_topic3[i][2]))
                    st.write("------------------------------------------------------------")
            if len(get_topic3) != 0:
                c1, c2, c3 = st.columns(3)
                with c2:
                    df2_hotel=df2[(df2['name'] == st.session_state.name) & (df2['Topics'] == "Positive Guest Experiences and Hotel Amenities")]
                    df_sentiment=df2_hotel['Review_Sentiment'].value_counts().to_frame().reset_index()

                    fig = go.Figure(go.Bar(
                        x=df_sentiment['Review_Sentiment'],y=df_sentiment['count'],
                        marker={'color': df_sentiment['count'], 
                        'colorscale': 'Viridis'},  
                        text=df_sentiment['count'],
                        textposition = "outside",
                    ))
                    st.plotly_chart(fig, use_container_width=True)
        with tab4:
            get_topic4 = get_topic(name=st.session_state.name,topic="Noise and Comfort Considerations in Accommodations")
            for i in range(len(get_topic4)):
                    st.caption(unsafe_allow_html=True, body='<b>'+get_topic4[i][1]+'</b>'+'\n\n'+str(get_topic4[i][2]))
                    st.write("------------------------------------------------------------")
            if len(get_topic4) != 0:
                c1, c2, c3 = st.columns(3)
                with c2:
                    df2_hotel=df2[(df2['name'] == st.session_state.name) & (df2['Topics'] == "Noise and Comfort Considerations in Accommodations")]
                    df_sentiment=df2_hotel['Review_Sentiment'].value_counts().to_frame().reset_index()

                    fig = go.Figure(go.Bar(
                        x=df_sentiment['Review_Sentiment'],y=df_sentiment['count'],
                        marker={'color': df_sentiment['count'], 
                        'colorscale': 'Viridis'},  
                        text=df_sentiment['count'],
                        textposition = "outside",
                    ))
                    st.plotly_chart(fig, use_container_width=True)
        with tab5:
            get_topic5 = get_topic(name=st.session_state.name,topic="Hotel Guest Feedback and Interactions")
            for i in range(len(get_topic5)):
                    st.caption(unsafe_allow_html=True, body='<b>'+get_topic5[i][1]+'</b>'+'\n\n'+str(get_topic5[i][2]))
                    st.write("------------------------------------------------------------")
            if len(get_topic5) != 0:
                c1, c2, c3 = st.columns(3)
                with c2:
                    df2_hotel=df2[(df2['name'] == st.session_state.name) & (df2['Topics'] == "Hotel Guest Feedback and Interactions")]
                    df_sentiment=df2_hotel['Review_Sentiment'].value_counts().to_frame().reset_index()

                    fig = go.Figure(go.Bar(
                        x=df_sentiment['Review_Sentiment'],y=df_sentiment['count'],
                        marker={'color': df_sentiment['count'], 
                        'colorscale': 'Viridis'},  
                        text=df_sentiment['count'],
                        textposition = "outside",
                    ))
                    st.plotly_chart(fig, use_container_width=False)
                


