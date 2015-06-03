from tropopause import Base, BaseAction
from troposphere.ec2 import VPC
from troposphere import Template

__author__ = 'drews'

class Project(Base):
    def __init__(self, title, description, zone_name=None):
        super().__init__()
        self.project = self
        self.description = description
        this.title = title
        self.region = None
        self.default_ami = None
        self.default_instance_size = None
        self.zone_name = zone_name
        self.compute_groups = []

    def add_compute_group(self, compute_group):
        self.compute_groups.append(compute_group)
        compute_group.project = self

    def generate_troposphere(self):
        return ActionCompileProject(self).compile().cfn_template


# Builds a troposphere object based on a project object
# Keep the compilation work seperate from the data object.
class ActionCompileProject(BaseAction):
    def __init__(self, project):
        self.project = project
        self.cfn_template = Template()
        self.cfn_vpc = None

    def compile(self):
        self.cfn_template.add_description(self.project.description)
        self.cfn_vpc = self.cfn_template.add_resource(VPC(
            self.project.title,
            CidrBlock=self.project.cidr_block+'/'+str(self.project.cidr_range)
        ))
        self.compute_network_structure()
        return self

    def compute_network_structure(self):
        public_subnet = False
        private_subnet = False
        for compute_group in self.project.compute_groups:
            if compute_group.is_private:
                private_subnet = True
            else:
                public_subnet = True

        if public_subnet:
            public_subnet = self.generate_public_subnet()
            self.generate_igw()
        if private_subnet:
            private_subnet = self.generate_private_subnet()

        self.generate_routing_table(
            private_subnet=private_subnet,
            public_subnet=public_subnet
        )

