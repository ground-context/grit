#!/usr/bin/env python

import csv
import json
import os
import sys

from typing import Dict, Tuple, List

class chinto(object):
    def __init__(self, target):
        self.original_dir = os.getcwd()
        self.target = target

    def __enter__(self):
        os.chdir(self.target)

    def __exit__(self, type, value, traceback):
        os.chdir(self.original_dir)

class Header(object):

    def __init__(self, tableName, schema, current_page_num=0, page_size=1024):
        assert(type(schema) == list)
        self.tableName = tableName
        self.schema = schema
        self.current_page_number = current_page_num
        self.page_size = page_size

    """
    Gets the current page path
    """
    def get_cpage(self):
        return 'page_' + str(self.current_page_number) + '.csv'

    def to_dict(self):
        return {
            'tableName': self.tableName,
            'schema': self.schema,
            'current_page': self.current_page_number,
            'page_size': self.page_size
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def flush(self, inContext=True):
        if inContext:
            with open('header.json', 'w') as f:
                json.dump(self.to_dict(), f)
        else:
            with chinto(target_dir(self.tableName)):
                with open('header.json', 'w') as f:
                    json.dump(self.to_dict(), f)

    def touch_next_page(self, inContext=True):
        self.current_page_number += 1  # ALERT: Dirty Bit is Set
        new_page_path = self.get_cpage()
        if inContext:
            open(new_page_path, 'a').close()
        else:
            with chinto(target_dir(self.tableName)):
                open(new_page_path, 'a').close()
        self.flush(inContext)         # Dirty bit cleared
        return self.get_cpage()

    @staticmethod
    def load(targetDir=None):
        if targetDir:
            with chinto(targetDir):
                with open('header.json', 'r') as f:
                    d = json.load(f)
        else:
            with open('header.json', 'r') as f:
                d = json.load(f)
        return Header(d['tableName'], d['schema'], int(d['current_page']), int(d['page_size']))


__DB_PATH__ = os.path.expanduser('~') + '/grit.d'

# Notes:
## in item_tag || rich_version_tag, type should be type Data_Type. Setting to string for now
__TABLE_SCHEMAS__ : Dict[str, list] = {'edge' : [('item_id', 'int'), ('source_key', 'string'), ('from_node_id', 'int'), ('to_node_id', 'int')],
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

# Header Cache. Bounded. In worst case, we can afford all header pages in memory.
__hc__ : Dict[str, Header] = {}

def __init__():
    if not os.path.exists(__DB_PATH__):
        os.mkdir(__DB_PATH__)
        for r in __TABLE_SCHEMAS__:
            os.mkdir(target_dir(r))
            with chinto(target_dir(r)):
                h = Header(r, __TABLE_SCHEMAS__[r])
                h.touch_next_page()

"""
Caching the header cuts the I/Os by up to a half. No reads.
However, unless we want the user to be responsible for "closing" grit
We have to force buffer to disk immediately after every dirty.
"""
def writeRecord(record, tableName):
    assert(type(record) == list)
    assert(tableName in __TABLE_SCHEMAS__)

    __cache_header__(tableName)

    # Some validation
    assert(len(record) == len(__TABLE_SCHEMAS__[tableName]))

    current_page = __hc__[tableName].get_cpage()

    with chinto(target_dir(tableName)):
        # This expression is overly-pessimistic, worth investigating
        if int(os.stat(current_page).st_size) + sys.getsizeof(','.join(record)+'\n') > __hc__[tableName].page_size:
            current_page = __hc__[tableName].touch_next_page()
        with open(current_page, 'a') as f:
            csvwriter = csv.writer(f, delimiter=',')
            csvwriter.writerow(record)



def target_dir(tableName):
    return __DB_PATH__ + '/' + tableName

def __cache_header__(tableName):
    if tableName not in __hc__:
        # cache miss, load from disk
        with chinto(target_dir(tableName)):
            __hc__[tableName] = Header.load()