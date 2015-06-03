from troposphere.autoscaling import AutoScalingGroup, LaunchConfiguration
from tropopause import Base

__author__ = 'drews'

class Group(Base):
    def __init__(self, private, title):
        super().__init__()
        self.is_private= private
        self.title = title
        self.security_groups = []
        self.ami_id = None
        self.key_name = None
        self.instanceType = None

    def add_security_group(self, security_group):
        self.security_groups.append(security_group)


    def render(self):

        #TODO   Expand this to handle merging of options for the launch configurations and autoscaling group.
        #TODO     ie, have a default config set and let the user override portions of it.
        if self.cfn_launchconfiguration is None:
            self.cfn_launchconfiguration = LaunchConfiguration(
                self.title+"LaunchConfiguration"
            )
        if self.cfn_autoscaling is None:
            self.cfn_autoscaling = AutoScalingGroup(
                self.title+"AutoScalingGroup",
                DesiredCapacity=1,
            )
