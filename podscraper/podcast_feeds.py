import csv
import requests
import json
import re
import logging


class PodcastFeedScraper(object):
    def __init__(self, info, fileName):
        self.fileName = fileName
        self.info = info
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=10)
        self.session.mount('https://', adapter)

    def scrape(self):
        ITUNES_API = "https://itunes.apple.com/lookup?id=%s"
        REGEX = r"\s*\/id([0-9]*)"
        PODCASTS = {}

        # Step 3: Open our previous podcasts CSV and start getting info about them 1 by 1.
        logging.debug("Opening categories file at path: %s", self.info)
        with open(self.info, 'r') as f:
            reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL)
            # Iterate over each URL and scrape its individual podcast URLs
            for row in reader:
                title = row[0]
                url = row[1]
                id = re.search(REGEX, url).group(1)

                # Generate the lookup URL
                current_url = ITUNES_API % id
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
                    logging.debug("Saving off %s" % title)
                    PODCASTS[title] = result['feedUrl']  # Just need title and feed URL for now.

        f.close()

        logging.info("Time to write %i podcasts to file", len(PODCASTS))

        # OK, now write the PODCASTS to their own CSV.
        logging.debug("Opening %s to write." % self.fileName)
        with open(self.fileName, 'w') as ff:
            writer = csv.writer(ff, delimiter=',', quoting=csv.QUOTE_ALL)
            for title, url in PODCASTS.items():
                logging.debug("Writing %s: %s" % (title.strip(), url))
                writer.writerow([title.strip(), url.strip()])

        ff.close()
