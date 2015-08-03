from operator import attrgetter
import boto.ec2
from troposphere import Base64, Join, Tags
from troposphere.ec2 import Instance

__author__ = 'drews'

class NATInstance(Instance):
    def __init__(self, **kwargs):
        kwargs['UserData'] = Base64(Join("", ["#!/bin/bash\n", "yum update -y && yum install -y yum-cron && chkconfig yum-cron on"]))
        # Make sure we have some tags no matter what
        if 'Tags' not in kwargs:
            kwargs['Tags'] = Tags(Name='NAT')
        # Make sure we have a name tag at least.
        has_no_name_tag = not list(tag for tag in kwargs['Tags'].tags if tag['Key'] == 'Name')
        if has_no_name_tag:
            kwargs['Tags'].tags.append({
                'Key' : 'Name',
                'Value': 'NAT'
            })



        nat_image = self.get_nat_image(kwargs['region'])

        super().__init__("NAT", *kwargs)

    def get_nat_image(self,region=None):
        ec2_conn = boto.ec2.connect_to_region(region)
        images = ec2_conn.get_all_images(
            owners=['amazon'],
            # AWS says we can filter by the ami name starting with 'amzn-ami-vpc-nat'
            # http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_NAT_Instance.html#NATInstance
            filters={'name' : 'amzn-ami-vpc-nat-hvm*'}
        )
        images.sort(key=attrgetter('creationDate'))
        return images.pop()