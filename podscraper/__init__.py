__all__ = ['Podscraper']

from pathlib2 import Path
from .categories import CategoryScraper
from .podcast_feeds import PodcastInfoScraper
from .podcast_info import PodcastInfo


class Podscraper(object):
    def __init__(self, root_path=None):
        if not root_path:
            root_path = Path.cwd()

    def categories(self, fileName):
        # CATEGORIES_FILE = 'categories.csv'
        scraper = CategoryScraper(fileName=fileName)
        scraper.scrape()
        print("Done fetching and writing categories.")

    def podcast_info(self, fileName):
        # PODCASTS_FILE = 'podcasts.csv'
        scraper = PodcastInfoScraper(fileName=fileName)
        scraper.scrape()
        print("Done parsing and writing RSS urls for each podcast.")

    def rss_feeds(self, fileName):
        # RSS_FILE = 'rss.csv'
        scraper = PodcastInfo(fileName=fileName)
        scraper.scrape()
        print("Done fetching and writing out iTunes URLs for each podcast.")
