from troposphere.ec2 import Instance

__author__ = 'drews'

class Base(Instance):
    def __init__(self, **kwargs):
        kwargs = self.baseline_tags(kwargs)
        super().__init__(*kwargs)

    def baseline_tags(self, kwargs):
        pass
