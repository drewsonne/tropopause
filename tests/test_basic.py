import json
import unittest
from tropopause.components import compute
from tropopause.project import Project
from tropopause.components.db import MySQL


__author__ = 'drews'

class TestBasic(unittest.TestCase):

    def setup_project(self):
        test_project = Project(
            title='TestProject',
            zone_name='testproject',
            description='Make sure we have a basic template'
        )
        test_project.region = 'eu-west-1'
        test_project.default_ami = 'ami-123456'
        test_project.default_instance_size = 't2.micro'
        return test_project

    def test_something(self):
        cfn_json = self.setup_project()\
            .generate_troposphere()\
            .to_json()
        cfn_dict = json.loads(cfn_json)
        # MAKE ASSERTIONS!!!

    def test_addcompute(self):
        test_project = self.setup_project()
        test_project.add_compute_group(compute.Group(
            title='BastionHost',
            private=False
        ))
        cfn_json = test_project\
            .generate_troposphere()\
            .to_json()
        cfn_dict = json.loads(cfn_json)
        # MAKE ASSERTIONS!!!

    def test_adddb(self):
        test_project = self.setup_project()
        test_project.add_database(MySQL())
        cfn_json = test_project\
            .generate_troposphere()\
            .to_json()
        cfn_dict = json.loads(cfn_json)
        # MAKE ASSERTIONS!!!


if __name__ == '__main__':
    unittest.main()
