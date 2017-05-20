from categories import CategoryScraper
from podcast_feeds import PodcastInfoScraper

FILENAME = 'categories.csv'
scraper = CategoryScraper(fileName=FILENAME)
scraper.scrape()
print("Done fetching and writing categories.")


PODCASTS_FILE = 'podcasts.csv'
scraper = PodcastInfoScraper(fileName=PODCASTS_FILE)
scraper.scrape()
print("Done parsing and writing RSS urls for each podcast.")
