from ..rich_version import RichVersion


class EdgeVersion(RichVersion):

    def __init__(self, json_payload):
        super(id, tags, structureVersionId, reference, referenceParameters)
        self._edge_id = edgeId
        self._from_node_version_start_id = json_payload['fromNodeVersionStartId']
        if json_payload['fromNodeVersionEndId'] <= 0:
            self._from_node_version_end_id = -1
        else:
            self._from_node_version_end_id = json_payload['fromNodeVersionEndId']
        self._to_node_version_start_id = json_payload['toNodeVersionStartId']
        if json_payload['toNodeVersionEndId'] <= 0:
            self._to_node_version_end_id = -1
        else:
            self._to_node_version_end_id = json_payload['toNodeVersionEndId']

    # def __init__(self, id, other):
    #     self(id, other, other)

    # def __init__(self, long id, RichVersion otherRichVersion, EdgeVersion other):
    #     super(id, otherRichVersion)
    #     self._edge_id = other.edgeId
    #     self._from_node_version_start_id = other.fromNodeVersionStartId
    #     self._from_node_version_end_id = other.fromNodeVersionEndId
    #     self._to_node_version_start_id = other.toNodeVersionStartId
    #     self._to_node_version_end_id = other.toNodeVersionEndId

    def get_edge_id(self):
        return self._edge_id

    def get_from_node_version_start_id(self):
        return self._from_node_version_start_id

    def get_from_node_version_end_id(self):
        return self._from_node_version_end_id

    def get_to_node_version_start_id(self):
        return self._to_node_version_start_id

    def get_to_node_version_end_id(self):
        return self._to_node_version_end_id

    def __eq__(self, other):
        if not isinstance(other, EdgeVersion):
            return False
        return (self._edge_id == otherEdgeVersion._edge_id
            and self._from_node_version_start_id == otherEdgeVersion._from_node_version_start_id
            and self._from_node_version_end_id == otherEdgeVersion._from_node_version_end_id
            and self._to_node_version_start_id == otherEdgeVersion._to_node_version_start_id
            and self._to_node_version_end_id == otherEdgeVersion._to_node_version_end_id
            and self.get_id() == otherEdgeVersion.get_id()
            and super(self, RichVersion) == super(other, RichVersion))
