import copy
from typing import Dict

class Tag:

    def __init__(self, json_payload):
        self._id  = json_payload.get('id')
        self._key = json_payload.get('key')
        self._val = json_payload.get('value')

    def get_id(self):
        return self._id

    def get_key(self):
        return self._key

    def get_value(self):
        return self._val

    def to_json(self):
        d = {}
        d["id"] = self._id
        d["key"] = self._key
        if isinstance(self._val, Tag):
            d["value"] = self._val.to_json()
        elif isinstance(self._val, Dict):
            t = copy.deepcopy(self._val)
            for k in t:
                t[k] = t[k].to_json()
            d["value"] = t
        else:
            d['value'] = self._val

        return d

    def __eq__(self, other):
        return (
            isinstance(other, Tag)
            and self._id == other._id
            and self._key == other._key
            and self._val == other._val
        )
