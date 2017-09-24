from ..version.rich_version import RichVersion


class LineageEdgeVersion(RichVersion):
    
    def __init__(self, json_payload):
        super(id, tags, json_payload['structureVersionId'], json_payload['reference'], json_payload['referenceParameters']);
        self._lineage_edge_id = json_payload['lineageEdgeId'];
        self._from_id = json_payload['fromId'];
        self._to_id = json_payload['toId'];

    def __init__(self, id, other):
        self(id, other, other);

    def __init__(self, id, otherRichVersion, other):
        super(self, RichVersion).__init__(id, otherRichVersion);
        self._lineage_edge_id = other.lineageEdgeId;
        self._from_id = other.fromId;
        self._to_id = other.toId;

    def getLineageEdgeId(self):
        return self._lineage_edge_id;

    def getFromId(self):
        return self._from_id;

    def getToId(self):
        return self._to_id;

    def __eq__(self, other):
        if not isinstance(other, LineageEdgeVersion):
            return False;
        return (self._lineage_edge_id == other._lineage_edge_id
            and self._from_id == other._from_id
            and self._to_id == other._to_id
            and self.get_id() == other.get_id()
            and super(self, RichVersion) == super(other, RichVersion))
