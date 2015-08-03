from troposphere import cloudformation
from troposphere.autoscaling import AutoScalingGroup, LaunchConfiguration
from tropopause import Base
from collections import namedtuple
__author__ = 'drews'

AutoScaleConfig = namedtuple('AutoScaleConfig', 'packages groups users sources files commands services')
ConfigSets = namedtuple('ConfigSets', 'ascending descending')

class Group(Base):
    def __init__(self, title, private=False, **kwargs):
        # Set defaults
        self.security_groups = []
        self.ami_id = None
        self.key_name = None
        self.instanceType = None
        self.configsets = None
        # Initialise parent
        super().__init__(*kwargs)
        # Override/extend parent
        self.is_private= private
        self.title = title
        self._config = {"default":AutoScaleConfig({},{},{},{},{},{},{})}

    # Get a particular configset.
    def config(self,name='default'):
        return self._config[name]

    # Specify the order for setup and tear down of the stack
    # If descending parameter is omitted, then use the
    # ascending parameter in reverse.
    def set_configsets(self, ascending, descending=None):
        if descending is None:
            descending = reversed(ascending)
        self.configsets = ConfigSets(ascending, descending)

    def add_security_group(self, security_group):
        self.security_groups.append(security_group)


    def compile(self):

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
