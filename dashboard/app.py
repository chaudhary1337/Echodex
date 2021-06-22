import streamlit as st
from expert_ai.main import get_analysis
from Backend.scrapper import Scrapper
from Backend.visualizations import sentiment_piechart
from pprint import pprint
from datetime import date, timedelta, datetime

time_now = date(2021, 6, 21)


def changeNewsLabel(news_sort_by):
    if news_sort_by == 'Publisher':
        news_sort_by = 'publishedAt'
    news_sort_by = news_sort_by[0].lower() + news_sort_by[1:]
    return news_sort_by


def changeRedditLabel(input):
    sort_by_list = ('Score', 'Number of Comments', 'Date')
    if input in sort_by_list:
        new = ('score', 'num_comments', 'created_utc')
        x = sort_by_list.index(input)
        return new[x]
    elif input == 'Ascending':
        return 'asc'
    else:
        return 'dsc'


with st.sidebar:
    st.title('Echodex')
    with st.form("my_form"):
        user_input = st.text_input("Search", value='')
        time_change = timedelta(days=14)
        submitted = st.form_submit_button("Submit")
        time_values = st.slider(
            "Select the date range:", value=((time_now - time_change), time_now), format="DD-MM")

        st.write('Advanced Configuration Options')

        with st.beta_expander("News"):
            news_size = st.number_input('Limit', value=20)
            news_sort_by = st.selectbox(
                'Sort By', ('Relevancy', 'Popularity', 'Publisher'), index=0)
            news_sort_by = changeNewsLabel(news_sort_by)

        with st.beta_expander("Reddit"):
            reddit_max_chars = st.number_input('Maximum Characters', value=250)
            reddit_max_content = st.number_input(
                'Number of comments to return', value=30)
            reddit_sort_by = st.selectbox(
                'Sort By', ('Score', 'Number of Comments', 'Date'), index=0)
            reddit_sort_order = st.selectbox(
                'Sort Order', ('Ascending', 'Descending'), index=1)
            reddit_sort_by = changeRedditLabel(reddit_sort_by)
            reddit_sort_order = changeRedditLabel(reddit_sort_order)

        with st.beta_expander("Twitter"):
            twitter_filter_retweets = st.checkbox('Filter Retweets')
            twitter_popular_tweets = st.checkbox(
                'Include Popular Tweets', value=True)
            twitter_verified = st.checkbox('Verified Profiles Only')
            twitter_minimum_likes = st.number_input('Minimum Likes', value=20)
            twitter_sort = st.checkbox('Sort by Descending Order', value=True)

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

    twitter_data = scrappy.scrape_twitter(filter_retweets=twitter_filter_retweets,
                                          popular_tweets=twitter_popular_tweets,
                                          verified=twitter_verified,
                                          min_likes=twitter_minimum_likes,
                                          sort_desc=twitter_sort)
    news_data = scrappy.scrape_news(page_size=news_size, sort_by=news_sort_by)
    reddit_data = scrappy.scrape_reddit(max_chars=reddit_max_chars,
                                        subreddit_max_size=reddit_max_content,
                                        sort_param=reddit_sort_by,
                                        sort_type=reddit_sort_order)
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
