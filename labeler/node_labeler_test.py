from unittest import TestCase
from mock import MagicMock
from mock import call
from node_labeler import NodeLabeler

class ApplicationTest(TestCase):
    def test_running_labeling_without_nodes(self):
        # Prepare data
        prefix = "test"
        infra = MagicMock()
        kube = MagicMock()
        kube.get_nodes = MagicMock(return_value=[])
        # Call labeler
        labeler = NodeLabeler(infra, kube, prefix)
        labeler.label_nodes()
        # Assert calls
        assert kube.get_nodes.called
        assert not infra.get_vm_by_hostname.called

    def test_running_labeling_with_nodes(self):
        # Prepare data
        prefix = "test"
        infra = MagicMock()
        kube = MagicMock()
        node = MagicMock()
        vm = MagicMock()
        tags = MagicMock()
        labels = MagicMock()
        node.get_name = MagicMock(return_value="node_name")
        kube.get_nodes = MagicMock(return_value=[node])
        infra.get_vm_by_hostname = MagicMock(return_value=vm)
        vm.get_tags = MagicMock(return_value={"key1":"value1", "key2":"value2"})
        node.get_labels = MagicMock(return_value=labels)
        labels.get_keys_by_prefix = MagicMock(return_value=["test_tag1", "test_tag4"])
        # Call labeler
        labeler = NodeLabeler(infra, kube, prefix)
        labeler.label_nodes()
        # Assert calls
        labels.remove_label.assert_has_calls([call("test_tag1"), call("test_tag4")], any_order=True)
        labels.add_label.assert_has_calls([call("test/key1", "value1"), call("test/key2", "value2")],  any_order=True)
        assert labels.commit.called