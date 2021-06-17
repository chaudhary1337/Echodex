from newsapi import NewsApiClient
import urllib.request, json
import re
import twint
from pprint import pprint


class Scrapper:
    """Contains scraper function definations.
    Currently available scrappers: Reddit, Twitter, News
    """

    def __init__(self):
        self.newsapi = NewsApiClient(api_key="")
        self.subreddits = [
            "investing",
            "personalfinance",
            "cryptocurrency",
            "securityanalysis",
            "finance",
        ]
        self.reddit_days = "7"
        self.reddit_size = 30
        self.twint_config = twint.Config()
        self.twint_config.Limit = 1
        self.twint_config.Hide_output = True
        self.twint_config.Store_object = True

    def scrape_news(self, query):
        """Scraps news using NewsApi

        Args:
            query: Query to search for on news

        Returns:
            A list of dictionaries:
            [
                {"title": "title1", "url": "url1"},
                {"title": "title2", "url": "url2"},
                ...
            ]
        """
        top_headlines = self.newsapi.get_everything(q=query, language="en")
        sources = self.newsapi.get_sources()
        outputs = []
        for x in top_headlines["articles"]:
            output = {}
            output["title"] = x["title"]
            output["url"] = x["url"]
            outputs.append(output)
        return outputs

    def scrape_reddit(self, query):
        """Scraps reddit using pushshift API

        Args:
            query: Query to search for on news

        Returns:
            A dictionary:
            {
                "subreddit1": [
                  "comment1",
                  "comment2",
                ],
                "subreddit2": [
                  "comment1",
                  "comment2",
                ],
            }
        """
        query = query.replace(" ", "%20")
        comments = {}
        for subreddit in self.subreddits:
            url = urllib.request.urlopen(
                f"https://api.pushshift.io/reddit/search/comment/?q={query}"
                + f"&subreddit={subreddit}&after={self.reddit_days}"
                + f"d&size={self.reddit_size}"
                + f"&fields=body,score&sort_type=score&sort=desc"
            )
            data = json.loads(url.read().decode())
            data_list = data["data"]
            data_list = data_list[:5]
            body = []
            for x in data_list:
                sentences = x["body"].split("\n")
                c = 0
                for sentence in sentences:
                    if len(sentence) > 50 and c <= 2:
                        body.append(sentence)
                        c += 1
            comments[subreddit] = body
        return comments

    def __clean_tweet(self, tweet):
        """Cleans a specific tweet to a cleaned format.
            Removed hashtags, mentions, multiple spaces and non-ascii 
            characters.

        Args:
            tweet: A string containing the tweet

        Returns:
            A string, the cleaned tweet
        """
        # Remove hashtags
        tweet = re.sub("#\w*", "", tweet)
        # Remove @
        tweet = re.sub("@\w*", "", tweet)
        tweet = re.sub("&amp", "", tweet)
        # Remove multiple spaces
        tweet = re.sub("\s{2,}", " ", tweet)
        # Remove non-ascii
        tweet = tweet.encode("ascii", "ignore").decode("ascii")
        tweet = tweet.strip()
        return tweet

    def scrape_twitter(self, query):
        """Scraps twitter using twint

        Args:
            query: Query to search for on twitter

        Returns:
            A list of dictionaries:
            [
                {
                    "hashtags": [#hashtag1, #hashtag2],
                    "id": "tweet-id",
                    "likes_count": likes_count,
                    "tweet": "tweet-text",
                    "username": "twitter-username"
                },
                ...
            ]
        """
        self.twint_config.Search = query
        twint.output.clean_lists()
        twint.run.Search(self.twint_config)
        data = twint.output.tweets_list
        formatted_data = []
        for y in data:
            try:
                each_entry = {}
                each_entry["username"] = y.username
                tweet = self.__clean_tweet(y.tweet)
                each_entry["tweet"] = tweet
                each_entry["hashtags"] = y.hashtags
                each_entry["likes_count"] = y.likes_count
                each_entry["id"] = y.id_str
                formatted_data.append(each_entry)
            except Exception as e:
                pprint(e)
                continue
        return formatted_data
