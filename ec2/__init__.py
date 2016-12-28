from boto.ec2 import connect_to_region


class Ec2VM():

    instance_object = None

    def __init__(self, instance):
        self.instance_object = instance

    def get_tags(self):
        return self.instance_object.tags


class Ec2():

    vpc_id = None
    ec2_conn = None

    def __init__(self, region,  vpc_id):
        self.vpc_id = vpc_id
        self.ec2_conn = connect_to_region(region)

    def get_vm_by_hostname(self, hostname):
        reservations = self.ec2_conn.get_all_instances(
            filters={
                'network-interface.private-dns-name': '%s.ec2.internal' % hostname,
                'vpc-id': self.vpc_id
            }
        )

        return Ec2VM(reservations[0].instances[0])

