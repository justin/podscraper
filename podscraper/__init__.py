__all__ = ['Podscraper']

from pathlib import Path
from .config import config
from .categories import CategoryScraper
from .podcast_feeds import PodcastInfoScraper
from .podcast_info import PodcastInfo


class Podscraper(object):
    def __init__(self):
        self.config = config

    def categories(self, fileName):
        path = Path(self.config.output_dir).joinpath(fileName)
        scraper = CategoryScraper(path=path)
        scraper.scrape()
        print("Done fetching and writing categories.")

    def podcast_info(self, fileName):
        # PODCASTS_FILE = 'podcasts.csv'
        path = self.config.output_dir.joinpath(fileName)
        scraper = PodcastInfoScraper(fileName=path)
        scraper.scrape()
        print("Done parsing and writing RSS urls for each podcast.")

    def rss_feeds(self, fileName):
        # RSS_FILE = 'rss.csv'
        path = self.config.output_dir.joinpath(fileName)
        scraper = PodcastInfo(fileName=path)
        scraper.scrape()
        print("Done fetching and writing out iTunes URLs for each podcast.")
