import streamlit as st
from expert_ai.main import get_analysis
from Backend.scrapper import Scrapper
from Backend.visualizations import sentiment_piechart
from pprint import pprint
from datetime import date, timedelta, datetime

time_now = date(2021, 6, 21)

with st.sidebar:
    st.title('Echodex')
    with st.form("my_form"):
        user_input = st.text_input("Search", value='')
        time_change = timedelta(days=44)
        submitted = st.form_submit_button("Submit")
        time_values = st.slider(
            "Select the date range:", value=((time_now - time_change), time_now), format="DD-MM")
        if submitted:
            from_date = time_values[0].strftime('%Y-%m-%d')
            until_date = time_values[1].strftime('%Y-%m-%d')
            scrappy = Scrapper(
                query=user_input, date_from=from_date, date_to=until_date)

sentiment_scores = {"positive": 0, "neutral": 0, "negative": 0}


def update_global_sentiments(value):
    if value > 0:
        sentiment_scores['positive'] += 1
    elif value < 0:
        sentiment_scores['negative'] += 1
    else:
        sentiment_scores['neutral'] += 1


def mark_entities(text, entities):
    for entity in entities:
        text = text.replace(entity, f'**{entity}**')
    return text


# fetching data
if user_input:

    twitter_data = scrappy.scrape_twitter()
    news_data = scrappy.scrape_news()
    reddit_data = scrappy.scrape_reddit()
    print(reddit_data)
    #news_data, twitter_data = [], []

    with st.beta_expander("News"):
        st.title(f"News fetched for {user_input}")
        for news_obj in news_data:
            analysis_obj = get_analysis(news_obj["title"])
            update_global_sentiments(analysis_obj['sentiments'][0])
            title_text = mark_entities(
                news_obj["title"], analysis_obj['entities'])
            st.write(f"""
                Title: {title_text}

                Score: {analysis_obj['sentiments'][0]}

                Url: {news_obj["url"]}

            """)

    with st.beta_expander("Reddit"):
        st.title(f"Reddit data fetched for {user_input}")
        for subreddit in reddit_data:
            for content in reddit_data[subreddit]:
                title = content["body"]
                analysis_obj = get_analysis(title)
                update_global_sentiments(analysis_obj['sentiments'][0])
                title_text = mark_entities(title, analysis_obj['entities'])
                st.write(f"""
                    Title: {title_text}

                    Score: {analysis_obj['sentiments'][0]}

                    Subreddit: {subreddit}

                    Url: {content['permalink']}

                """)
    with st.beta_expander("Twitter"):
        st.title(f"Twitter data fetched for {user_input}")
        for twitter_obj in twitter_data:
            analysis_obj = get_analysis(twitter_obj["tweet"])
            update_global_sentiments(analysis_obj['sentiments'][0])
            title_text = mark_entities(
                twitter_obj["tweet"], analysis_obj['entities'])
            st.write(f"""
                Tweet: {title_text}

                Username: {twitter_obj["username"]}

                Likes: {twitter_obj["likes_count"]}

                Score: {analysis_obj['sentiments'][0]}

                Url: {twitter_obj["link"]}

            """)

    st.sidebar.pyplot(sentiment_piechart(sentiment_scores))
