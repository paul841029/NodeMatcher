from .tools import Scraper
# wiki_scraper = Scraper("source.html", "../data/wiki")
# wiki_scraper.wiki_run()

amz_parser = Scraper("amazon_sourcce.html", "../data/amz")
amz_parser.amz_run()