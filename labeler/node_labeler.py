from re import sub

class NodeLabeler():


    infra = None
    kube = None
    prefix = None


    def __init__(self, infra, kube, prefix):
        self.infra = infra
        self.kube = kube
        self.prefix = prefix


    def label_nodes(self):
        nodes = self.kube.get_nodes()
        for node in nodes:
            vm = self.infra.get_vm_by_hostname(node.get_name())

            tags = vm.get_tags()
            labels = node.get_labels()

            # Remove from labels all the labels that start with the "prefix". Then,
            # add to "labels" every tag prepended with the "prefix"

            for label in labels.get_keys_by_prefix(self.prefix):
                labels.remove_label(label)

            for tag_key, tag_value in tags.iteritems():
                labels.add_label('%s/%s' % (self.prefix, sub('[:/\s]', '-', tag_key)),
                                 sub('[:/\s]', '-', tag_value[:63]))

            labels.commit()