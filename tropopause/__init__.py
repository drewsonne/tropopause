__author__ = 'drews'

class Base:

    def __init__(self):
        self.project = None

    def compile(self, template):
        raise NotImplementedError("You must implement a method to compile your component to troposphere objects.")

class BaseAction:
    pass