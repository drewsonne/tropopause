__author__ = 'drews'

class Base:

    def __init__(self, **kwargs):
        self.project = None
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def compile(self, template):
        raise NotImplementedError("You must implement a method to compile your component to troposphere objects.")

class BaseAction:
    pass

class Plugins:
    def load():
        plugin = Plugins()
        # 1 - Find config file
        # 2 - Read config defaults
        # 3 - Merge config and defaults
        # 4 -
        pass
