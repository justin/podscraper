import csv
import requests
import json
import re
import logging


class iTunesURLScraper(object):
    """Initialize a new instance of iTunesURLScraper"""

    def __init__(self, path):
        self.path = path
        self.categories = self.path.joinpath("categories").expanduser()
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=10)
        self.session.mount('https://', adapter)

    def scrape(self):
        """Go through the process of iterating a category csv and writing out the resulting
        RSS info."""
        # Step 2: Open our previous categories files and get all our podcasts.
        for path in self.categories.iterdir():
            if path.suffix == '.csv':
                results = self._scrape(path)
                self._write(path.name, results)

    def _scrape(self, path):
        """Scrap the passed in CSV file at path and query the iTunes API for its RSS feed."""
        REGEX = r"\s*\/id([0-9]*)"
        ITUNES_API = "https://itunes.apple.com/lookup?id=%s"
        podcasts = {}
        logging.info("Opening categories file at path: %s", path)
        with open(path, 'r') as f:
            reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL)
            rows = list(reader)
            # Iterate over each URL and scrape its individual podcast URLs
            logging.info("Reading %i rows", len(rows))
            for row in rows:
                itunes_url = row[0]
                id = re.search(REGEX, itunes_url).group(1)

                # Generate the lookup URL
                current_url = ITUNES_API % id
                logging.info("Requesting %s" % current_url)

                try:
                    result = self.session.get(current_url, timeout=5.0)
                except requests.exceptions.Timeout:
                    logging.error("Timeout for %s" % current_url)
                    break

                if result.status_code != 200:
                    logging.error("No 200 returned for URL %s" % current_url)
                    break

                data = json.loads(result.text)
                results = data['results']
                for result in results:
                    # Just need title and feed URL for now.
                    title = result["collectionName"]
                    podcasts[title] = result['feedUrl']

        f.close()

        return podcasts

    def _write(self, fileName, results):
        """Write a CSV file out with the passed in results."""
        logging.info("Time to write %i podcasts to file", len(results))

        # OK, now write the PODCASTS to their own CSV in the "itunes" directory
        itunes_dir = self.path.joinpath("itunes")
        if not itunes_dir.exists():
            itunes_dir.mkdir(parents=True)

        with open(itunes_dir.joinpath(fileName).expanduser(), 'w') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)
            for title, url in results.items():
                logging.debug("Writing %s: %s" % (title, url))
                writer.writerow([title, url])

        f.close()
