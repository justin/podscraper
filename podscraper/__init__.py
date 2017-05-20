from categories import CategoryScraper
from podcast_feeds import PodcastInfoScraper
from podcast_info import PodcastInfo

CATEGORIES_FILE = 'categories.csv'
scraper = CategoryScraper(fileName=CATEGORIES_FILE)
scraper.scrape()
print("Done fetching and writing categories.")

PODCASTS_FILE = 'podcasts.csv'
scraper = PodcastInfoScraper(fileName=PODCASTS_FILE)
scraper.scrape()
print("Done parsing and writing RSS urls for each podcast.")

RSS_FILE = 'rss.csv'
scraper = PodcastInfo(fileName=RSS_FILE)
scraper.scrape()
print("Done fetching and writing out iTunes URLs for each podcast.")
