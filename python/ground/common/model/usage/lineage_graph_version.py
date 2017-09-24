from ..version.rich_version import RichVersion


class LineageGraphVersion(RichVersion):

    def __init__(self, json_payload):
        super(self, RichVersion).__init__(json_payload['id'], json_payload['tags'], json_payload['structureVersionId'], json_payload['reference'], json_payload['referenceParameters'])
        self._lineage_graph_id = json_payload['lineageGraphId']
        if 'lineageEdgeVersionIds' not in json_payload.keys():
            self._lineage_edge_version_ids = []
        else:
            self._lineage_edge_version_ids = json_payload['lineageEdgeVersionIds']

    # def __init__(self, id, other):
    #     self(id, other, other)

    # def __init__(self, id, otherRichVersion, other):
    #     super(self, RichVersion).__init__(id, other)
    #     self._lineage_graph_id = other.lineageGraphId
    #     self._lineage_edge_version_ids = other.lineageEdgeVersionIds

    def get_lineage_graph_id(self):
        return self._lineage_graph_id

    def get_lineage_edge_version_ids(self):
        return self._lineage_edge_version_ids

    # NOTE: for _lineage_edge_version_ids, even if lists contain same elements but different ordering, they are still not equal
    def __eq__(self, other):
        if not isinstance(other, LineageGraphVersion):
            return False
        return (self._lineage_graph_id == otherLineageGraphVersion._lineage_graph_id
            and self._lineage_edge_version_ids == otherLineageGraphVersion._lineage_edge_version_ids
            and super(self, RichVersion) == super(other, RichVersion))
