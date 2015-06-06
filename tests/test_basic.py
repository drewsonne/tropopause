import json
import unittest
from tropopause.components import compute
from tropopause.project import Project
from tropopause.components.db import MySQL

__author__ = 'drews'

class TestBasic(unittest.TestCase):

    def setup_project(self,with_zone=True):
        if not with_zone:
            with_zone=None
        else:
            with_zone='testproject'
        test_project = Project(
            title='TestProject',
            zone_name=with_zone,
            description='Make sure we have a basic template'
        )
        test_project.region = 'eu-west-1'
        test_project.default_ami = 'ami-123456'
        test_project.default_instance_size = 't2.micro'
        return test_project

    # Gets a json document from the resources dir and returns
    # that json doc as a parsed dict.
    def get_json_resource(self, resource_path):
        with open('resources/'+resource_path) as fp:
            return json.load(fp)

    def test_basic_project(self):
        src_cfn_dict = self.get_json_resource('cfn_templates/basic.cfn')
        project = self.setup_project()

        cfn_dict = json.loads(project\
            .generate_troposphere()\
            .to_json()
        )
        self.assertDictEqual(src_cfn_dict, cfn_dict)
        # MAKE ASSERTIONS!!!

    def test_addcompute(self):
        test_project = self.setup_project()
        awslinux = compute.Group(
            title='AWSLinux',
            private=False
        )
        awslinux.ami_id = 'ami-a10897d6'
        test_project.add_compute_group(compute.Group(
            title='AWSLinux',
            private=False,

        ))
        cfn_json = test_project\
            .generate_troposphere()\
            .to_json()
        cfn_dict = json.loads(cfn_json)
        with open('add_compute.cfn', 'w') as fp:
            fp.write(cfn_json)
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
