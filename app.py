from ec2 import Ec2
from kubernetes import Kubernetes
from os import environ
from re import sub
from time import sleep

def main(infra, kube, prefix):

    while True:

        nodes = kube.get_nodes()
        for node in nodes:
            vm = infra.get_vm_by_hostname(node.get_name())

            tags = vm.get_tags()
            labels = node.get_labels()

            # Remove from labels all the labels that start with the "prefix". Then,
            # add to "labels" every tag prepended with the "prefix"

            for label in labels.get_keys_by_prefix(prefix):
                labels.remove_label(label)

            for tag_key, tag_value in tags.iteritems():
                labels.add_label('%s/%s' % (prefix, sub('[:/\s]', '-', tag_key)), sub('[:/\s]', '-', tag_value[:63]))

            labels.commit()

        sleep(2)


if __name__ == '__main__':

    vpc_id = environ['VPC']
    region = environ['REGION']
    prefix = environ['LABEL_PREFIX']

    infra = Ec2(region, vpc_id)
    kube = Kubernetes()

    main(infra, kube, prefix)
