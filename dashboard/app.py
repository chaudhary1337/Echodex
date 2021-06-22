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
        time_change = timedelta(days=30)
        submitted = st.form_submit_button("Submit")
        time_values = st.slider(
            "Select the date range:", value=((time_now - time_change), time_now))
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


print(user_input)
st.title("hello")
# fetching data
if user_input:

    news_data = scrappy.scrape_news(page_size=1)
    # reddit_data = scrappy.scrape_reddit()
    # twitter_data = scrappy.scrape_twitter()
    print(news_data)
    # print(reddit_data)
    # print(twitter_data)

    # st.title(f"News fetched for {user_input}")
    # for news_obj in news_data:
    #     analysis_obj = get_analysis(news_obj["title"])
    #     update_global_sentiments(analysis_obj['sentiments'][0])
    #     title_text = mark_entities(news_obj["title"], analysis_obj['entities'])
    #     st.write(f"""
    #         Title: {title_text}

    #         Score: {analysis_obj['sentiments'][0]}

    #         Url: {news_obj["url"]}

    #     """)

    # st.title(f"Reddit data fetched for {user_input}")
    # for subreddit in reddit_data:
    #     for title in reddit_data[subreddit]:
    #         analysis_obj = get_analysis(title)
    #         update_global_sentiments(analysis_obj['sentiments'][0])
    #         title_text = mark_entities(title, analysis_obj['entities'])
    #         st.write(f"""
    #             Title: {title_text}

    #             Score: {analysis_obj['sentiments'][0]}

    #             Subreddit: {subreddit}

    #         """)

    # st.title(f"Twitter data fetched for {user_input}")
    # for twitter_obj in twitter_data:
    #     analysis_obj = get_analysis(twitter_obj["tweet"])
    #     update_global_sentiments(analysis_obj['sentiments'][0])
    #     title_text = mark_entities(
    #         twitter_obj["tweet"], analysis_obj['entities'])
    #     st.write(f"""
    #         Tweet: {title_text}

    #         Username: {twitter_obj["username"]}

    #         Likes: {twitter_obj["likes_count"]}

    #         Score: {analysis_obj['sentiments'][0]}
    #     """)

    # st.pyplot(sentiment_piechart(sentiment_scores))
    # print(sentiment_scores)

# sentence = "I am a good boy."
# x = Scrapper('bitcoin')
# print(x.scrape_twitter())
# print(get_analysis(sentence))
