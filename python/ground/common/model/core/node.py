from ..version.item import Item


class Node(Item):

    def __init__(self, json_payload):
        super().__init__(json_payload)

        self._name = json_payload['name']
        self._source_key = json_payload['sourceKey']

    @classmethod
    def from_node(cls, node_id, other_node):
        json = {
            'id': node_id,
            'tags': other_node.get_tags(),
            'name': other_node.get_name(),
            'sourceKey': other_node.get_source_key(),
        }
        node = cls(json)
        return node

    def get_item_id(self):
        return self.get_id()

    def get_name(self):
        return self._name

    def get_source_key(self):
        return self._source_key

    def __eq__(self, other):
        return (
            isinstance(other, Node) and
            self._name == other._name and
            self._source_key == other._source_key and
            self._id == other._id and
            self._tags == other._tags
        )
