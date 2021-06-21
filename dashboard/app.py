import streamlit as st
from expert_ai.main import get_analysis
from Backend.scrapper import Scrapper
from Backend.visualizations import sentiment_piechart
from pprint import pprint

user_input = st.text_input("Search", value='')

scrappy = Scrapper(user_input)
sentiment_scores = {"positive": 0, "neutral": 0, "negative": 0}

# fetching data
if user_input:
    news_data = scrappy.scrape_news()
    reddit_data = scrappy.scrape_reddit()
    twitter_data = scrappy.scrape_twitter()

    st.title(f"News fetched for {user_input}")
    for news_obj in news_data:
        analysis_obj = get_analysis(news_obj["title"])
        if analysis_obj['sentiments'][0] > 0:
            sentiment_scores['positive'] += 1
        elif analysis_obj['sentiments'][0] < 0:
            sentiment_scores['negative'] += 1
        else:
            sentiment_scores['neutral'] += 1
        st.write(f"""
            Title: {news_obj["title"]}

            Score: {analysis_obj['sentiments'][0]}
            
            Url: {news_obj["url"]}

        """)

    st.title(f"Reddit data fetched for {user_input}")
    for subreddit in reddit_data:
        for title in reddit_data[subreddit]:
            analysis_obj = get_analysis(title)
            if analysis_obj['sentiments'][0] > 0:
                sentiment_scores['positive'] += 1
            elif analysis_obj['sentiments'][0] < 0:
                sentiment_scores['negative'] += 1
            else:
                sentiment_scores['neutral'] += 1
            st.write(f"""
                Title: {title}

                Score: {analysis_obj['sentiments'][0]}

                Subreddit: {subreddit}

            """)

    st.title(f"Twitter data fetched for {user_input}")
    for twitter_obj in twitter_data:
        analysis_obj = get_analysis(twitter_obj["tweet"])
        if analysis_obj['sentiments'][0] > 0:
            sentiment_scores['positive'] += 1
        elif analysis_obj['sentiments'][0] < 0:
            sentiment_scores['negative'] += 1
        else:
            sentiment_scores['neutral'] += 1
        st.write(f"""
            Tweet: {twitter_obj["tweet"]}

            Username: {twitter_obj["username"]}
            
            Likes: {twitter_obj["likes_count"]}

            Score: {analysis_obj['sentiments'][0]}
        """)

    st.pyplot(sentiment_piechart(sentiment_scores))
    print(sentiment_scores)

# sentence = "I am a good boy."
# x = Scrapper('bitcoin')
# print(x.scrape_twitter())
# print(get_analysis(sentence))
