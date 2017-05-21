__all__ = ['Podscraper']

from pathlib import Path
from .config import config
from .categories import CategoryScraper
from .podcast_feeds import PodcastFeedScraper
from .itunes_scraper import iTunesURLScraper


class Podscraper(object):
    def __init__(self):
        self.config = config

    def categories(self, fileName):
        path = Path(self.config.output_dir).joinpath(fileName).expanduser()
        scraper = CategoryScraper(path=path)
        scraper.scrape()
        print("Done fetching and writing categories.")
        return path

    def podcast_info(self, categories, fileName):
        path = Path(self.config.output_dir).joinpath(fileName).expanduser()
        scraper = iTunesURLScraper(categories=categories, fileName=path)
        scraper.scrape()
        print("Done fetching and writing out iTunes URLs for each podcast.")
        return path

    def rss_feeds(self, info, fileName):
        path = Path(self.config.output_dir).joinpath(fileName).expanduser()
        scraper = PodcastFeedScraper(info=info, fileName=path)
        scraper.scrape()
        print("Done parsing and writing RSS urls for each podcast.")
        return path
