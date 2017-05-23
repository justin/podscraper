__all__ = ['Config', 'config']
from pathlib import Path


class Config(object):
    """Initialize a new instance of Config"""

    def __init__(self):
        self.output_dir = Path.cwd()
        self.verbose = False

    def update(self, **kwargs):
        """Update the config values with the passed in kwargs"""
        for key, value in sorted(kwargs.items()):
            if value:
                if hasattr(self, key):
                    setattr(self, key, value)


config = Config()
