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
