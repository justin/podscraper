from setuptools import setup

setup(
    name="podscraper",
    version="0.0.2",
    license="MIT",
    author="Justin Williams",
    author_email="justinw@me.com",
    description="Convenience scripts to scrape the iTunes podcsast directory.",
    packages=['podscraper'],
    install_requires=[
        'beautifulsoup4',
        'click',
        'click-didyoumean',
        'lxml',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        podscraper=podscraper.cli:main
        ''',
)
