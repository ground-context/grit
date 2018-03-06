#!/usr/bin/env python

import csv
import json
import os

__DB_PATH__ = os.path.expanduser('~') + '/grit.d'

# Notes:
## in item_tag || rich_version_tag, type should be type Data_Type. Setting to string for now
__TABLE_SCHEMAS__ = {'edge' : [('item_id', 'int'), ('source_key', 'string'), ('from_node_id', 'int'), ('to_node_id', 'int')],
                     'edge_version': [('id', 'int'), ('edge_id', 'int'), ('from_node_version_start_id', 'int'), ('from_node_version_end_id', 'int'), ('to_node_version_start_id', 'int'), ('to_node_version_end_id', 'int')],
                     'graph': [('item_id', 'int'), ('source_key', 'string'), ('name', 'string')],
                     'graph_version': [('id', 'int'), ('graph_id', 'int')],
                     'graph_version_edge': [('graph_version_id', 'int'), ('edge_version_id', 'int')],
                     'item': [('id', 'int')],
                     'item_tag': [('item_id', 'int'), ('key', 'string'), ('value', 'string'), ('type', 'string')],
                     'lineage_edge': [('item_id', 'int'), ('source_key', 'string'), ('name', 'string')],
                     'lineage_edge_version': [('id', 'int'), ('lineage_edge_id', 'int'), ('from_rich_version_id', 'int'), ('to_rich_version_id', 'int'), ('principal_id', 'int')],
                     'lineage_graph': [('item_id', 'int'), ('source_key', 'string'), ('name', 'string')],
                     'lineage_graph_version': [('id', 'int'), ('lineage_graph_id', 'int')],
                     'lineage_graph_version_edge': [('lineage_graph_version_id', 'int'), ('lineage_edge_version_id', 'int')],
                     'node': [('item_id', 'int'), ('source_key', 'string'), ('name', 'string')],
                     'node_version': [('id', 'int'), ('node_id', 'int')],
                     'principal': [('node_id', 'int'), ('source_key', 'string'), ('name', 'string')],
                     'rich_version': [('id', 'int'), ('structure_version_id', 'int'), ('reference', 'string')],
                     'rich_version_external_parameter': [('rich_version_id', 'int'), ('key', 'string'), ('value', 'string')],
                     'rich_version_tag': [('rich_version_id', 'int'), ('key', 'string'), ('value', 'string'), ('type', 'string')],
                     'structure': [('item_id', 'int'), ('source_key', 'string'), ('name', 'string')],
                     'structure_version': [('id', 'int'), ('structure_id', 'int')],
                     'structure_version_attribute': [('structure_version_id', 'int'), ('key', 'string'), ('type', 'string')],
                     'version': [('id', 'int')],
                     'version_history_dag': [('item_id', 'int'), ('version_successor_id', 'int')],
                     'version_successor': [('id', 'int'), ('from_version_id', 'int'), ('to_version_id', 'int')]}

def __init__():
    if not os.path.exists(__DB_PATH__):
        os.mkdir(__DB_PATH__)
        for r in __TABLE_SCHEMAS__:
            os.mkdir(target_dir(r))
            with chinto(target_dir(r)):
                open('page_1.csv', 'a').close()
                h = Header(__TABLE_SCHEMAS__[r])
                h.flush()

class chinto(object):
    def __init__(self, target):
        self.original_dir = os.getcwd()
        self.target = target

    def __enter__(self):
        os.chdir(self.target)

    def __exit__(self, type, value, traceback):
        os.chdir(self.original_dir)

class Header(object):

    def __init__(self, schema, current_page=1, page_size=1024):
        assert(type(schema) == list)
        self.schema = schema
        self.current_page = current_page
        self.page_size = page_size

    def to_dict(self):
        return {
            'schema': self.schema,
            'current_page': self.current_page,
            'page_size': self.page_size
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def flush(self, targetDir=None):
        if targetDir:
            with chinto(targetDir):
                with open('header.json', 'w') as f:
                    json.dump(self.to_dict(), f)
        else:
            with open('header.json', 'w') as f:
                json.dump(self.to_dict(), f)

    @staticmethod
    def load(targetDir=None):
        if targetDir:
            with chinto(targetDir):
                with open('header.json', 'r') as f:
                    d = json.load(f)
        else:
            with open('header.json', 'r') as f:
                d = json.load(f)
        return Header(d['schema'], d['current_page'], d['page_size'])



def writeRecord(record, tableName):
    assert(type(record) == list)
    assert(tableName in __TABLE_SCHEMAS__)

    with chinto(target_dir(tableName)):
        pass

def target_dir(tableName):
    return __DB_PATH__ + '/' + tableName
