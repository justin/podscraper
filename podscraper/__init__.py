from categories import CategoryScraper

FILENAME = 'categories.csv'
scraper = CategoryScraper(fileName=FILENAME)
scraper.scrape()
print("Done fetching and writing categories.")
