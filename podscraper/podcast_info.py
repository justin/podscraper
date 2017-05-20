import csv
import requests
from bs4 import BeautifulSoup


class PodcastInfo(object):
    def __init__(self, categories, fileName):
        self.categories = categories
        self.fileName = fileName

    def scrape(self):
        PODCASTS = {}

        # Step 2: Open our previous categories file and get all our podcasts.
        with open(self.categories, 'r') as f:
            reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL)
            # Iterate over each URL and scrape its individual podcast URLs
            for row in reader:
                current_url = row[1]
                result = requests.get(current_url, timeout=5.0)
                if result.status_code != 200:
                    print("No 200 returned for URL %s" % current_url)
                    break

                html_contents = result.content
                soup = BeautifulSoup(html_contents, "lxml")
                # Currently each page has 3 columns of podcasts. Let's get their URLs.
                for column in soup.select('div.column ul li a'):
                    title = column.getText().encode('utf-8').strip()
                    url = column.get("href")
                    print("Fetching %s: %s." % (title, url))
                    PODCASTS[title] = url

        f.close()

        # OK, now write the PODCASTS to their own CSV.
        with open(self.fileName, 'w') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)
            for title, url in PODCASTS.items():
                print("Writing %s: %s" % (title, url))
                writer.writerow([title, url])

        f.close()
