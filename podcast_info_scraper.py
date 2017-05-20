import csv
import requests
import json
import re
from pprint import pprint

ITUNES_API = "https://itunes.apple.com/lookup?id=%s"
PODCASTS_FILE = 'podcasts.csv'
RSS_FILE = 'rss.csv'
REGEX = r"\s*\/id([0-9]*)"
PODCASTS = {}

# Step 3: Open our previous podcasts CSV and start getting info about them 1 by 1.
with open(PODCASTS_FILE, 'r') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_ALL)
    # Iterate over each URL and scrape its individual podcast URLs
    for row in reader:
        title = row[0]
        url = row[1]
        id = re.search(REGEX, url).group(1)

        # Generate the lookup URL
        current_url = ITUNES_API % id
        result = requests.get(current_url, timeout=5.0)
        if result.status_code != 200:
            pprint("No 200 returned for URL %s" % current_url)
            break

        data = json.loads(result.text)
        results = data['results']
        for result in results:
            pprint("Saving off %s" % title)
            PODCASTS[title] = result['feedUrl']  # Just need title and feed URL for now.

f.close()

# OK, now write the PODCASTS to their own CSV.

pprint("Opening %s" % RSS_FILE)
with open(RSS_FILE, 'w') as ff:
    writer = csv.writer(ff, delimiter=',', quoting=csv.QUOTE_ALL)
    for title, url in PODCASTS.iteritems():
        pprint("Writing %s: %s" % (title.encode('utf-8').strip(), url))
        writer.writerow([title.encode('utf-8').strip(), url.encode('utf-8').strip()])

ff.close()
print("Done parsing and writing RSS urls for each podcast.")
