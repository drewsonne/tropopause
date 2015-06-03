__author__ = 'drews'

from troposphere.ec2 import VPC
from troposphere import Template

class Project:
    def __init__(self, **kwargs):
        self.cfn_template = Template()
        self.cfn_template.add_resource(VPC(
            title=kwargs.title
        ))
    pass