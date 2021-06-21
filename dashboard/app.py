import streamlit as st
from expert_ai.main import get_analysis
from Backend.scrapper import Scrapper
from pprint import pprint

user_input = st.text_input("Search", value='')

scrappy = Scrapper(user_input)

# fetching data
if user_input:
    news_data = scrappy.scrape_news()
    reddit_data = scrappy.scrape_reddit()
    twitter_data = scrappy.scrape_twitter()

    st.title(f"News fetched for {user_input}")
    for news_obj in news_data:
        st.write(f"""
            Title: {news_obj["title"]}

            Url: {news_obj["url"]}

        """)

    st.title(f"Reddit data fetched for {user_input}")
    for subreddit in reddit_data:
        for title in reddit_data[subreddit]:
            st.write(f"""
                Title: {title}

                Subreddit: {subreddit}

            """)
    st.title(f"Twitter data fetched for {user_input}")
    for twitter_obj in twitter_data:
        st.write(f"""
            Tweet: {twitter_obj["tweet"]}

            Username: {twitter_obj["username"]}
            
            Likes: {twitter_obj["likes_count"]}
        """)
# sentence = "I am a good boy."
# x = Scrapper('bitcoin')
# print(x.scrape_twitter())
# print(get_analysis(sentence))
