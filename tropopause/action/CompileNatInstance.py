from tropopause import BaseAction
from tropopause.plugin.instance.nat import NATInstance

__author__ = 'drews'

# Builds a nat instance and attaches it to the existing troposhere object in the project.
# Keep the compilation work seperate from the data object.
class CompileNatInstance(BaseAction):
    def __init__(self, project, template):
        self.project = project
        self.template = template
        pass

    def compile(self, route_table_name):
        # self.nat_ami = self.get_nat_image()
        self.template.add_resource(NATInstance(region=self.project.region))
        pass