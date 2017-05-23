__all__ = ['Podscraper']

from pathlib import Path
from .config import config
from .categories import CategoryScraper
from .itunes_scraper import iTunesURLScraper
import logging


class Podscraper(object):
    def __init__(self):
        self.config = config
        print(self.config)
        self.path = Path(self.config.output_dir).expanduser()
        print(self.path)

    def categories(self):
        scraper = CategoryScraper(path=self.path)
        scraper.scrape()
        logging.info("Done fetching and writing categories.")

    def podcast_info(self):
        scraper = iTunesURLScraper(path=self.path)
        scraper.scrape()
        logging.info("Done fetching and writing out RSS URLs for each podcast.")
