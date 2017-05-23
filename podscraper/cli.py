__all__ = ['cli', 'main']

from pathlib import Path
import click
from click_didyoumean import DYMGroup
from podscraper import Podscraper
import logging


@click.group(cls=DYMGroup)
@click.option('--verbose', default=False, is_flag=True, help="Verbose logging.")
@click.pass_context
def cli(context, verbose):
    """A poorly written scraper for the Apple Podcast Directory"""
    scraper = Podscraper()
    context.obj = scraper
    level = logging.DEBUG if verbose else logging.INFO
    logger = logging.getLogger()
    logger.setLevel(level)


@cli.command(help='Scrape the podcast directory')
@click.option('--output-dir', type=click.Path(), help='The directory to store CSVs')
@click.pass_context
def scrape(context, output_dir, **kwargs):
    scraper = context.obj
    scraper.config.update(**kwargs)
    path = Path(output_dir).expanduser()
    scraper.categories(path)
    scraper.podcast_info(path)


def main():
    cli()
