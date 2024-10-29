import streamlit as st
from PIL import Image
import pandas as pd

import Sentiment
import Topic

import sqlite3
conn = sqlite3.connect("Data.db") # db - database
cursor = conn.cursor() # Cursor object

# Page configuration
st.set_page_config(
    page_title="Hotel Reviews",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded")

# ======= Read Data ==========
df = pd.read_sql_query("SELECT * FROM Hotels;", conn)

image = Image.open('Images/logo11.png')
st.image(image)

st.write("")

# ================================
if "page" not in st.session_state:
    st.session_state.page = 0
if "name" not in st.session_state:
    st.session_state.name = ""

def nextpage(hotel_name):
    st.session_state.page += 1 # Go to next page
    st.session_state.name = hotel_name

def restart(): st.session_state.page = 0 # Go back to beginning

# ================= Trigger Review Screen ======================
placeholder = st.empty()
def review_widgets(hotel_name):
    nextpage(hotel_name)

# SQL
def get_reviews(sentiment: str,name: str):
    
    response = cursor.execute("""SELECT title, review FROM Reviews
                                        WHERE Review_Sentiment='{}' and name='{}'
                                        ORDER BY RANDOM()
                                        LIMIT 3;""".format(sentiment, name))
    return response.fetchall()

# ================ Page 1 ==================
if st.session_state.page == 0:

    with placeholder.container():

        st.subheader("Review previously visited hotels")
        st.caption("Help others make better decisions by leaving reviews on your expereinces...")

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
                        review_widgets(row['name'])

# ================ Page 2 ==================
elif st.session_state.page == 1:
    with placeholder.container():
        c1, c2, c3 = st.columns([1,6,1])

        with c1:
             if st.button("Back"):
                  restart()
        with c2:
            st.subheader(body=f"User reviews on :red[{st.session_state.name}]")

        pos_reviews = get_reviews(sentiment="Positive", name=st.session_state.name)
        neu_reviews = get_reviews(sentiment="Neutral", name=st.session_state.name)
        neg_reviews = get_reviews(sentiment="Negative", name=st.session_state.name)

        tab1, tab2, tab3 = st.tabs(["😃:green[Positive]", "😐Neutral", "😫:red[Negative]"])

        with tab1:
                for i in range(len(pos_reviews)):
                    st.caption(unsafe_allow_html=True, body='<b>'+pos_reviews[i][0]+'</b>'+'\n\n'+str(pos_reviews[i][1]))
                    st.write("------------------------------------------------------------")
        with tab2:
                for i in range(len(neu_reviews)):
                    st.caption(unsafe_allow_html=True, body='<b>'+neu_reviews[i][0]+'</b>'+'\n\n'+str(neu_reviews[i][1]))
                    st.write("------------------------------------------------------------")
        with tab3:
                for i in range(len(neg_reviews)):
                    st.caption(unsafe_allow_html=True, body='<b>'+neg_reviews[i][0]+'</b>'+'\n\n'+str(neg_reviews[i][1]))
                    st.write("------------------------------------------------------------")
             
        title = st.text_input('Review title', placeholder="Wonderful experience")
        collect_review = st.text_area(label='Share your experience with {}'.format(st.session_state.name))
        if st.button("Send"):
            if collect_review == '' or title == '':
                st.toast("You can't submit an empty review or title", icon='❌')
            elif collect_review.isdigit() or title.isdigit():
                 st.toast("You can't submit a number as a review or title", icon='❌')
            elif len(collect_review.split()) < 10:
                 st.toast('Insufficient words, type in more words', icon='❌')
            else:
                try:
                    response1 = cursor.execute("""SELECT city, province, address FROM Hotels
                                        WHERE name='{}';
                                        """.format(st.session_state.name))
                    result = response1.fetchall()

                    # =========== Sentiment =============
                    sentiment = Sentiment.get_sentiment(collect_review)

                    # ============= Topic ===============
                    topic = Topic.get_topic(collect_review)

                    # Insert into Reviews table
                    cursor.execute("""INSERT INTO Reviews VALUES ("{}","{}","{}","{}","{}","{}","{}","{}");
                                    """.format(st.session_state.name, title, collect_review,result[0][2],
                                                result[0][0], result[0][1],sentiment,topic))
                    
                    conn.commit()
                    conn.close()
                    st.toast('Response recorded, Thank you', icon='✅')
                except Exception as e:
                    st.toast('ERROR: '+str(e)+'', icon='❌')

        