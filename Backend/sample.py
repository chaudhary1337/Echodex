from scrapper import Scrapper
from pprint import pprint

scraper = Scrapper(query="tesla", date_to="2021-06-22", date_from="2021-06-18")

# # REDDIT: WORKS!
# d = scraper.scrape_reddit(
#     max_lines=7,
#     subreddit_max_size=5,
#     sort_param="score",
#     sort_type="desc",
# )
# pprint(d)

# results = scraper.scrape_news()
# pprint(len(results))
# # pprint(results)
