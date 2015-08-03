from troposphere import Template
from tropopause import Base, BaseAction
from tropopause.action.CompileProject import CompileProject

__author__ = 'drews'

class Project(Base):
    def __init__(self, title, description, zone_name=None):
        super().__init__()
        self.project = self
        self.description = description
        self.title = title
        self.region = None
        self.default_ami = None
        self.default_instance_size = None
        self.zone_name = zone_name
        self.compute_groups = []
        self.cidr_block = '10.0.0.0'
        self.cidr_range = '16'

    def add_compute_group(self, compute_group):
        self.compute_groups.append(compute_group)
        compute_group.project = self

    def generate_troposphere(self):
        template = Template()
        return CompileProject(self, template).compile().cfn_template

    def add_database(self, database):
        pass