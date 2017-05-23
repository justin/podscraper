from bs4 import BeautifulSoup
import csv
import requests
import logging


class CategoryScraper(object):
    def __init__(self, path):
        self.path = path.joinpath("categories")
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=10)
        self.session.mount('https://', adapter)

    def scrape(self):
        URLs = []
        TIMEOUT = 5.0
        ITUNES_BASE_URL = "https://itunes.apple.com/us/genre/"

        CATEGORIES = {
            'arts': "podcasts-arts/id1301",
            'business': "podcasts-business/id1321",
            'comedy': "podcasts-comedy/id1303",
            'education': "podcasts-education/id1304",
            'games_and_hobbies': "podcasts-games-hobbies/id1323",
            'government_and_organizations':
                "podcasts-government-organizations/id1325",
            'health': "podcasts-health/id1307",
            'kids_and_family': "podcasts-kids-family/id1305",
            'music': "podcasts-music/id1310",
            'news_and_politics': "podcasts-news-politics/id1311",
            'religion_and_spirituality':
                "podcasts-religion-spirituality/id1314",
            'science_and_medicine':
                "podcasts-science-medicine/id1315",
            'society_and_culture': "podcasts-society-culture/id1324",
            'sports_and_recreation':
                "podcasts-sports-recreation/id1316",
            'technology': "podcasts-tv-film/id1309",
            'tv_and_film': "podcasts-technology/id1318"
        }

        # Create the 'categories' directory if it doesn't exist.
        if not self.path.exists():
            self.path.mkdir(parents=True)

        for category, slug in CATEGORIES.items():
            current_url = "%s%s" % (ITUNES_BASE_URL, slug)
            logging.info("Scraping Category: %s." % slug)

            try:
                result = self.session.get(current_url, timeout=TIMEOUT)
            except requests.exceptions.Timeout:
                logging.error("Timeout for %s" % current_url)
                break

            if result.status_code != 200:
                logging.error("No 200 returned for URL %s" % current_url)
                break

            html_contents = result.content
            soup = BeautifulSoup(html_contents, "lxml")
            for pagination_tag in soup.select('div.column ul li a'):
                page_url = pagination_tag.get("href")
                URLs.append(page_url)

            self._writeCategory(category, URLs)

    def _writeCategory(self, category, urls):
        filePath = self.path.joinpath("%s.csv" % category).expanduser()
        with open(filePath, 'w') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)

            for url in urls:
                logging.debug("Writing URL %s" % url)
                writer.writerow([url])

        f.close()
