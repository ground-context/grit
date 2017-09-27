from ..version.version import Version


class RichVersion(Version):

    def __init__(self, json_payload):
        super().__init__(json_payload['id'])

        self._tags = json_payload.get('tags', {}) or {}

        svid = json_payload.get('structureVersionId')
        if svid is None or svid <= 0:
            self._structure_version_id = -1
        else:
            self._structure_version_id = svid

        reference = json_payload.get('reference')
        if reference is None or reference == "null":
            self._reference = reference
        else:
            self._reference = reference

        self._parameters = json_payload.get('referenceParameters', {}) or {}


    @classmethod
    def from_rich_version(cls, _id, other_rich_version):
        return cls({
            'id': _id,
            'tags': other.get_tags(),
            'structureVersionId': other_rich_version.get_structure_version_id(),
            'reference': other_rich_version.get_reference(),
            'referenceParameters': other_rich_version.get_parameters(),
        })

    def get_tags(self):
        return self._tags

    def get_structure_version_id(self):
        return self._structure_version_id

    def get_reference(self):
        return self._reference

    def get_parameters(self):
        return self._parameters

    # NOTE: for get_tags() and _parameters, even if lists contain same elements
    # but different ordering, they are still not equal
    def __eq__(self, other):
        if not isinstance(other, RichVersion):
            return False
        return (self.get_id() == other.get_id()
            and self._tags == other._tags
            and self._structure_version_id == other._structure_version_id
            and self._reference == other._reference
            and self._parameters == other._parameters)
