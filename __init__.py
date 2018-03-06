#!/usr/bin/env python3

import os

db_path = os.path.expanduser('~') + '/grit.d'
if not os.path.exists(db_path):
    relations = ['edge',
                 'edge_version',
                 'graph',
                 'graph_version',
                 'graph_version_edge',
                 'item',
                 'item_tag',
                 'lineage_edge',
                 'lineage_edge_version',
                 'lineage_graph',
                 'lineage_graph_version',
                 'lineage_graph_version_edge',
                 'node',
                 'node_version',
                 'principal',
                 'rich_version',
                 'rich_version_external_parameter',
                 'rich_version_tag',
                 'structure',
                 'structure_version',
                 'structure_version_attribute',
                 'version',
                 'version_history_dag',
                 'version_successor']

    os.mkdir(db_path)

    for r in relations:
        os.mkdir(db_path + '/' + r)

