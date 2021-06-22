from scrapper import Scrapper
from pprint import pprint

scraper = Scrapper(query="tesla", date_to="2021-06-22", date_from="2021-06-01")

# # REDDIT: WORKS!
# d = scraper.scrape_reddit(
#     max_lines=7,
#     subreddit_max_size=5,
#     sort_param="score",
#     sort_type="desc",
# )
# pprint(d)

# NEWS: WORKS!
# results = scraper.scrape_news(language="en", page_size=1, sort_by="relevancy")
# pprint(len(results))
# pprint(results)
