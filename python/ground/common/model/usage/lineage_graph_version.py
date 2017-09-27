from ..version.rich_version import RichVersion


class LineageGraphVersion(RichVersion):

    def __init__(self, json_payload):
        super().__init__(json_payload)
        self._lineage_graph_id = json_payload.get('lineageGraphId', 0)
        self._lineage_edge_version_ids = json_payload.get('lineageEdgeVersionIds', [])

    @classmethod
    def from_lineage_graph_version(cls, _id, other_lineage_graph_version):
        return LineageGraphVersion.from_lineage_graph_version_and_rich_version(
            _id, other_lineage_graph_version, other_lineage_graph_version
        )

    @classmethod
    def from_lineage_graph_version_and_rich_version(
                cls, _id, other_rich_version, other_lineage_graph_version):
        return cls({
            'id': _id,
            'tags': other.get_tags(),
            'structureVersionId': other_rich_version.get_structure_version_id(),
            'reference': other_rich_version.get_reference(),
            'referenceParameters': other_rich_version.get_parameters(),
            'lineageGraphId': other_lineage_graph_version.get_lineage_graph_id(),
            'lineageEdgeVersionIds', other_lineage_graph_version.get_lineage_edge_version_ids(),
        })

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
