__all__ = ['cli', 'main']

import click
from podscraper import Podscraper


@click.group()
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
    cat = scraper.categories(fileName="categories.csv")
    cat.scrape()


def main():
    cli()
