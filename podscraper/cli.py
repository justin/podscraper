__all__ = ['cli', 'main']

import click
from click_didyoumean import DYMGroup
from podscraper import Podscraper


@click.group(cls=DYMGroup)
@click.pass_context
def cli(context):
    """A poorly written scraper for the Apple Podcast Directory"""
    scraper = Podscraper()
    context.obj = scraper


@cli.command(help='Scrape the podcast directory')
@click.option('--output-dir', help='The directory to store CSVs')
@click.pass_context
def scrape(context, **kwargs):
    scraper = context.obj
    scraper.config.update(**kwargs)
    categories = scraper.categories(fileName="categories.csv")
    info = scraper.podcast_info(categories=categories, fileName="podcasts.csv")
    scraper.rss_feeds(info=info, fileName="rss.csv")


def main():
    cli()
