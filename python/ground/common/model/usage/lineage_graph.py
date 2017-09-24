from ..version.item import Item


class LineageGraph(Item):

    def __init__(self, json_payload):
        super(self, Item).__init__(json_payload['id'], json_payload['tags'])
        self._name = json_payload['name']
        self._source_key = json_payload['sourceKey']

    # def __init__(self, id, other):
    #     super(id, other.get_tags())
    #     self._name = other.name
    #     self._source_key = other.sourceKey

    def get_name(self):
        return self._name

    def get_source_key(self):
        return self._source_key

    # NOTE: for get_tags(), even if lists contain same elements but different ordering, they are still not equal
    def __eq__(self, other):
        if not isinstance(other, LineageGraph):
            return False
        return (self._name == other._name
            and self.get_id() == other.get_id()
            and self._source_key == other._source_key
            and self.get_tags() == other.get_tags())
