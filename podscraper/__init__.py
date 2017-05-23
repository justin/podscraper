__all__ = ['Podscraper']

from .config import config
from .categories import CategoryScraper
from .itunes_scraper import iTunesURLScraper
import logging


class Podscraper(object):
    """Initialize a new instance of Podscraper"""

    def __init__(self):
        self.config = config
        self.path = self.config.output_dir.expanduser()

    def categories(self, output_dir):
        scraper = CategoryScraper(path=output_dir)
        scraper.scrape()
        logging.info("Done fetching and writing categories.")

    def podcast_info(self, output_dir):
        scraper = iTunesURLScraper(path=output_dir)
        scraper.scrape()
        logging.info("Done fetching and writing out RSS URLs for each podcast.")
