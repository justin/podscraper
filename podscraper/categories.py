import string
import csv
import requests
from bs4 import BeautifulSoup


class CategoryScraper(object):
    def __init__(self, fileName):
        self.fileName = fileName

    def scrape(self):
        TIMEOUT = 5.0
        ITUNES_BASE_URL = "https://itunes.apple.com/us/genre/"

        CATEGORIES = {
            'arts': "podcasts-arts/id1301?mt=2",
            'business': "podcasts-business/id1321?mt=2",
            'comedy': "podcasts-comedy/id1303?mt=2",
            'education': "podcasts-education/id1304?mt=2",
            'games_and_hobbies': "podcasts-games-hobbies/id1323?mt=2",
            'government_and_organizations':
                "podcasts-government-organizations/id1325?mt=2",
            'health': "podcasts-health/id1307?mt=2",
            'kids_and_family': "podcasts-kids-family/id1305?mt=2",
            'music': "podcasts-music/id1310?mt=2",
            'news_and_politics': "podcasts-news-politics/id1311?mt=2",
            'religion_and_spirituality':
                "podcasts-religion-spirituality/id1314?mt=2",
            'science_and_medicine':
                "podcasts-science-medicine/id1315?mt=2",
            'society_and_culture': "podcasts-society-culture/id1324?mt=2",
            'sports_and_recreation':
                "podcasts-sports-recreation/id1316?mt=2",
            'technology': "podcasts-tv-film/id1309?mt=2",
            'tv_and_film': "podcasts-technology/id1318?mt=2"
        }

        alphabet = string.ascii_uppercase + '*'
        with open(self.fileName, 'w') as f:
            writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_ALL)
            for key, value in CATEGORIES.items():
                for letter in alphabet:
                    # Determine how many pages there are.
                    current_url = "%s%s&letter=%s" % (ITUNES_BASE_URL, value, letter)
                    result = requests.get(current_url, timeout=TIMEOUT)
                    if result.status_code != 200:
                        print("No 200 returned for URL %s" % current_url)
                        break

                    html_contents = result.content
                    soup = BeautifulSoup(html_contents, "lxml")
                    for pagination_tag in soup.select('ul.paginate li a'):
                        page_url = pagination_tag.get("href")
                        print("Writing URL %s" % page_url)
                        writer.writerow([key, page_url])

        f.close()
