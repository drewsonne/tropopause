import unittest
from tropopause.components import compute
from tropopause.project import Project
from tropopause.components.db import MySQL


__author__ = 'drews'

class TestBasic(unittest.TestCase):
    def test_something(self):
        test_project = Project(
            title='TestProject',
            zone_name='testproject',
            description='Make sure we have a basic template'
        )
        test_project.region = 'eu-west-1'
        test_project.default_ami = 'ami-123456'
        test_project.default_instance_size = 't2.micro'

        test_project.add_compute_group(compute.Group(
            title='BastionHost',
            private=False
        ))

        test_project.add_database(MySQL())


        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
