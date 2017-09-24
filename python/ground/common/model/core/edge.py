from ..version.item import Item


class Edge(Item):

    def __init__(self, json_payload):
        super(id, tags)
        self._name = json_payload['name']
        self._from_node_id = json_payload['fromNodeId']
        self._to_node_id = json_payload['toNodeId']
        self._source_key = json_payload['sourceKey']

    # def __init__(self, id, other):
    #     super(id, other.getTags())
    #     self._name = other.get_name()
    #     self._from_node_id = other.get_from_node_id()
    #     self._to_node_id = other.get_to_node_id()
    #     self._source_key = other.get_source_key()

    def get_name(self):
        return self._name

    def get_from_node_id(self):
        return self._from_node_id

    def get_to_node_id(self):
        return self._to_node_id

    def get_source_key(self):
        return self._source_key

    # NOTE: for get_tags(), even if lists contain same elements but different ordering, they are still not equal
    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return (self._name == other._name
            and self._source_key == other._source_key
            and self.get_id() == other.get_id()
            and self._from_node_id == other._from_node_id
            and self._to_node_id == other._to_node_id
            and self.get_tags() == other.get_tags())
