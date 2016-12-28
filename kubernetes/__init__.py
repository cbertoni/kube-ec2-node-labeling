import pykube

class KubernetesLabels():

    node_object = None

    def __init__(self, node_object):
        self.node_object = node_object

    def commit(self):
        try:
            print 'Ready to update the node labels...'
            self.node_object.update()
        except pykube.exceptions.HTTPError as e:
            print e
            print 'Seems we arrived here late. We will retry.'

    def add_label(self, key, value):
        self.node_object.obj['metadata']['labels'][key] = value

    def remove_label(self, key):
        self.node_object.obj['metadata']['labels'][key] = None

    def get_keys_by_prefix(self, prefix):
        return filter(lambda x: x.startswith(prefix),
            self.node_object.obj['metadata']['labels'].keys())



class KubernetesNode():

    node_object = None

    def __init__(self, node_object):
        self.node_object = node_object

    def get_name(self):
        return self.node_object.name

    def get_labels(self):
        return KubernetesLabels(self.node_object)


class Kubernetes():

    kube = None

    def __init__(self):
        self.kube = pykube.HTTPClient(pykube.KubeConfig.from_service_account(
            path='/var/run/secrets/kubernetes.io/serviceaccount'))

    def get_nodes(self):
        nodes = [KubernetesNode(node) for node in pykube.Node.objects(self.kube)]

        return nodes

