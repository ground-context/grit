from ..version.version import Version


class RichVersion(Version):

    def __init__(self, json_payload):
        super(id)
        if 'tags' not in json_payload.keys():
            self._tags = {}
        else:
            self._tags = json_payload['tags']

        if 'structureVersionId' not in json_payload.keys() or json_payload['structureVersionId'] <= 0:
            self._structure_version_id = -1
        else:
            self._structure_version_id = json_payload['structureVersionId']

        if 'reference' not in json_payload.keys() or json_payload['reference'] == "null":
            self._reference = None
        else:
            self._reference = json_payload['reference']

        if 'referenceParameters' not in json_payload.keys():
            self._parameters = {}
        else:
            self._parameters = json_payload['referenceParameters']

    # def __init__(self, id, other):
    #     super(id)
    #     self._tags = other.tags
    #     self._structure_version_id = other.structureVersionId
    #     self._reference = other.reference
    #     self._parameters = other.parameters

    def get_tags(self):
        return self._tags

    def get_structure_version_id(self):
        return self._structure_version_id

    def get_reference(self):
        return self._reference

    def get_parameters(self):
        return self._parameters

    # NOTE: for get_tags() and _parameters, even if lists contain same elements but different ordering, they are still not equal
    def __eq__(self, other):
        if not isinstance(other, RichVersion):
            return False
        return (self.get_id() == other.get_id()
            and self._tags == other._tags
            and self._structure_version_id == other._structure_version_id
            and self._reference == other._reference
            and self._parameters == other._parameters)
