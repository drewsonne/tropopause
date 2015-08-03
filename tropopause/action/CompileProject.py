from tropopause import BaseAction
from troposphere.ec2 import VPC, RouteTable, Route, InternetGateway, VPCGatewayAttachment, SubnetRouteTableAssociation, \
    Subnet
from troposphere import Template, Ref
from tropopause.action.CompileNatInstance import CompileNatInstance

__author__ = 'drews'

# Builds a troposphere object based on a project object
# Keep the compilation work seperate from the data object.
class CompileProject(BaseAction):
    def __init__(self, project, template):
        self.project = project
        self.cfn_template = template
        self.cfn_vpc = None

    def compile(self):
        self.cfn_template.add_description(self.project.description)
        self.cfn_vpc = self.cfn_template.add_resource(VPC(
            self.project.title,
            CidrBlock=self.project.cidr_block+'/'+str(self.project.cidr_range)
        ))
        self.compute_network_structure()
        self.compute_compute_groups(self.project.compute_groups)
        return self

    def compute_compute_groups(self, compute_groups):
        for compute_group in compute_groups:
            self.generate_compute_group(compute_group)

    def generate_compute_group(self, compute_group):
        pass
        # 1 - Create a Launch Configuration
        # 2 - Create an Autoscaling Group
        #

    def compute_network_structure(self):
        public_subnet = False
        private_subnet = False
        for compute_group in self.project.compute_groups:
            if compute_group.is_private:
                private_subnet = True
            else:
                public_subnet = True

        if public_subnet or private_subnet:
            public_subnet = self.generate_public_subnet()
        if private_subnet:
            private_subnet = self.generate_private_subnet()

        self.generate_routing_table(
            private_subnet=private_subnet,
            public_subnet=public_subnet
        )

    def create_route_table(self, name):
        return self.cfn_template.add_resource(RouteTable(
            name+"RouteTable",
            VpcId=Ref(self.cfn_vpc)
        ))

    def generate_private_subnet(self):
        vpc_ref = Ref(self.cfn_vpc)

        private_route_table = self.create_route_table(name='PrivateSubnet')
        private_route = self.cfn_template.add_resource(Route(
            'PrivateSubnetRoute',
            DependsOn=[private_route_table]
        ))

        private_subnet = self.cfn_template.add_resource(Subnet(
            'PrivateSubnet',
            VpcId=vpc_ref,
            CidrBlock=self.generate_subnet_cidr()
        ))

        self.bind_table_to_subnet(
            name='PrivateSubnet',
            table=private_route_table,
            subnet=private_subnet
        )

        CompileNatInstance(self.project, self.cfn_template).compile(
            route_table_name=Ref(private_route_table)
        )

    def generate_public_subnet(self):
        vpc_ref = Ref(self.cfn_vpc)

        igw = self.cfn_template.add_resource(InternetGateway(
            'PublicSubnetInternetGateway'
        ))
        self.bind_igw_to_vpc(name='PublicSubnet',igw=igw)

        public_route_table = self.create_route_table(name='PublicSubnet')
        public_route = self.cfn_template.add_resource(Route(
            'PublicSubnetPublicRoute',
            DependsOn=igw.title,
            RouteTableId=Ref(public_route_table),
            DestinationCidrBlock="0.0.0.0/0",
            GatewayId=Ref(igw)
        ))

        public_subnet = self.cfn_template.add_resource(Subnet(
            'PublicSubnet',
            VpcId=vpc_ref,
            CidrBlock=self.generate_subnet_cidr()
        ))
        self.bind_table_to_subnet(
            name='PublicSubnet',
            table=public_route_table,
            subnet=public_subnet
        )

        return public_subnet

    def generate_subnet_cidr(self):
        range_diff = 32-int(self.project.cidr_range)
        subnet_offset = int(range_diff/2)
        range_mask = subnet_offset+int(self.project.cidr_range)
        return self.project.cidr_block+'/'+str(range_mask)

    def generate_routing_table(self, private_subnet, public_subnet):
        pass

    def bind_igw_to_vpc(self, name, igw):
        return self.cfn_template.add_resource(VPCGatewayAttachment(
            name+"GatewayToInternet",
            VpcId=Ref(self.cfn_vpc),
            InternetGatewayId=Ref(igw)
        ))

    def bind_table_to_subnet(self, name, table, subnet):
        return self.cfn_template.add_resource(SubnetRouteTableAssociation(
            name+"RouteTableAssociation",
            SubnetId=Ref(subnet),
            RouteTableId=Ref(table)
        ))