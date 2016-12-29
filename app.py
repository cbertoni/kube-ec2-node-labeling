from ec2 import Ec2
from kubernetes import Kubernetes
from labeler.node_labeler import NodeLabeler
from os import environ
from time import sleep


def main(labeler):
    
    while True:
        labeler.label_nodes()
        sleep(2)


if __name__ == '__main__':

    vpc_id = environ['VPC']
    region = environ['REGION']
    prefix = environ['LABEL_PREFIX']

    infra = Ec2(region, vpc_id)
    kube = Kubernetes()
    labeler = NodeLabeler(infra, kube, prefix)

    main(labeler)
