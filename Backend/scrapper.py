from newsapi.newsapi_client import NewsApiClient
import urllib.request
import json
import re
import twint
from pprint import pprint


class Scrapper:
    """Contains scraper function definitions.
    Currently available scrappers: Reddit, Twitter, News
    """

    def __init__(self, query, date_from, date_to):
        self.newsapi = NewsApiClient(api_key="4e8ea7f6b6224eeba684c0051f32397c")
        self.subreddits = [
            "investing",
            "personalfinance",
            "cryptocurrency",
            "securityanalysis",
            "finance",
        ]
        self.query = query
        self.date_from = date_from
        self.date_to = date_to
        # self.reddit_days = "7"
        # self.reddit_size = 30
        self.twint_config = twint.Config()
        self.twint_config.Limit = 1
        self.twint_config.Hide_output = True
        self.twint_config.Store_object = True
        self.twint_config.Since = date_from
        self.twint_config.Until = date_to

    def scrape_news(self, language="en", page_size=20, sort_by="relevancy"):
        """Scraps news using NewsApi

        Args:
            # query:
                # Query to search for on news
            language:
                lmao
            page_size:
                number of results
            sort_by:
                values possible: relevancy, popularity, publishedAt
        Returns:
            A list of dictionaries:
            [
                {
                  'author': 'https://www.engadget.com/about/editors/jon-fingas',
                  'content': "You might have to forego dreams of driving Tesla's ..."
                  'description': "Elon Musk claims the Tesla Model S Plaid+ is 'canceled' as "
                  'publishedAt': '2021-06-06T21:18:04Z',
                  'source': {'id': 'engadget', 'name': 'Engadget'},
                  'title': "Elon Musk says Tesla Model S Plaid+ is 'canceled'",
                  'url': 'https://www.engadget.com/elon-musk-says-tesla-model-s-plaid-plus-canceled-211804141.html',
                  'urlToImage': 'https://s.yimg.com/os/creatr-uploaded-images/2021-03/a53fc4a0-8d72-11eb-bffa-fac9a7f8b050'
                }
            ]
        """
        query = self.query
        data = self.newsapi.get_everything(
            q=query,
            language="en",
            page_size=page_size,
            from_param=self.date_from,
            to=self.date_to,
            sort_by=sort_by,
        )

        articles = data["articles"]

        # sources = self.newsapi.get_sources()
        # outputs = []
        # for x in top_headlines["articles"]:
        #     output = {}
        #     output["title"] = x["title"]
        #     output["url"] = x["url"]
        #     outputs.append(output)
        return articles

    def scrape_reddit(
        self,
        max_lines=10,
        subreddit_max_size=30,
        sort_param="score",
        sort_type="dsc",
    ):
        """Scraps reddit using pushshift API

        Args:
            # query:
                # Query to search for on news
            date_in_last:
                5d means in the last 5 days
            subreddit_max_size:
                30 means max number of comments that can be returned
            score_param:
                "score", "num_comments", "created_utc"
            sort_type:
                asc/desc
        Returns:
            A dictionary:
            {
                "subreddit1": [
                  {"body": "this is some text", "score": 6},
                  {"body": "this is some wow text", "score": 9},
                ],
                "subreddit2": [
                  {"body": "this is some bad text", "score": 3},
                ],
            }
        """
        query = self.query
        query = query.replace(" ", "%20")
        comments = {}
        for subreddit in self.subreddits:
            pre_url = (
                f"https://api.pushshift.io/reddit/search/comment/?q={query}"
                + f"&subreddit={subreddit}"
                + f"&after={self.date_from}&before={self.date_to}"
                + f"&size={subreddit_max_size}"
                + f"&fields=body,score&sort_type={sort_param}&sort={sort_type}"
                # + f"&aggs=created_utc&frequency=hour"
            )
            url = urllib.request.urlopen(pre_url)
            data = json.loads(url.read().decode())
            data_list = data["data"]
            # data_list = data_list[:5]
            comments[subreddit] = [
                item for item in data_list if len(item["body"].split("\n")) < max_lines
            ]
            # body = []
            # for x in data_list:
            #     sentences = x["body"].split("\n")
            #     c = 0
            #     for sentence in sentences:
            #         if len(sentence) > 50 and c <= 2:
            #             body.append(sentence)
            #             c += 1
            # comments[subreddit] = body
            # comments[subreddit] = {sentences}
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

    def scrape_twitter(
        self,
        limit=10,
        filter_retweets=False,
        popular_tweets=True,
        verified=False,
        min_likes=20,
        sort_desc=True,
    ):
        """Scraps twitter using twint

        Args:
            # query:
                # Query to search for on twitter
            limit:
                doesnt work yet
            filter_retweets:
                True/False
            popular_tweets:
                True/False
            verifies:
                verified profiles only. True/False
            min_likes:
                20. atleast 20 likes should be there
            sort_desc:
                sorts the tweets by the likes_count in descending order


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
        # resetting configs
        self.twint_config.Limit = limit
        self.twint_config.Filter_retweets = filter_retweets
        self.twint_config.Popular_tweets = popular_tweets
        self.twint_config.Verified = verified
        self.twint_config.Min_likes = min_likes

        query = self.query
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

        sorted_data = sorted(
            formatted_data, key=lambda tweet: tweet["likes_count"], reverse=sort_desc
        )
        return sorted_data
