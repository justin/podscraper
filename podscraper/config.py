__all__ = ['Config', 'config']
from pathlib import Path


class Config(object):
    def __init__(self):
        self.output_dir = Path.cwd()

    def update(self, **kwargs):
        for key, value in sorted(kwargs.items()):
            if value:
                if hasattr(self, key):
                    setattr(self, key, value)


config = Config()
