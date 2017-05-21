import csv
import requests
from bs4 import BeautifulSoup
import logging


class iTunesURLScraper(object):
    def __init__(self, categories, fileName):
        self.categories = categories
        self.fileName = fileName
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=10)
        self.session.mount('https://', adapter)

    def scrape(self):
        PODCASTS = {}

        # Step 2: Open our previous categories file and get all our podcasts.
        with open(self.categories, 'r') as f:
            reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL)
            # Iterate over each URL and scrape its individual podcast URLs
            for row in reader:
                current_url = row[1]

                try:
                    result = self.session.get(current_url, timeout=5.0)
                except requests.exceptions.Timeout:
                    logging.error("Timeout for %s" % current_url)
                    break

                if result.status_code != 200:
                    logging.error("No 200 returned for URL %s" % current_url)
                    break

                html_contents = result.content
                soup = BeautifulSoup(html_contents, "lxml")
                # Currently each page has 3 columns of podcasts. Let's get their URLs.
                for column in soup.select('div.column ul li a'):
                    title = column.getText().encode('utf-8').strip()
                    url = column.get("href")
                    logging.debug("Fetching %s: %s." % (title, url))
                    PODCASTS[title] = url

        f.close()

        # OK, now write the PODCASTS to their own CSV.
        with open(self.fileName, 'w') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)
            for title, url in PODCASTS.items():
                logging.debug("Writing %s: %s" % (title, url))
                writer.writerow([title, url])

        f.close()
