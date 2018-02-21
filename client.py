

class GroundClient:

    '''
    Skeleton from https://github.com/ground-context/client
    '''

    def __init__(self, hostname="localhost", port=9000):
        pass

    '''
    EDGE METHODS
    '''

    def create_edge(self, source_key, name, from_node_id, to_node_id, tags=None):
        pass

    def create_edge_version(self,
                            edge_id,
                            from_node_version_start_id,
                            to_node_version_start_id,
                            from_node_version_end_id=-1,
                            to_node_version_end_id=-1,
                            reference=None,
                            reference_parameters=None,
                            tags=None,
                            structure_version_id=-1,
                            parent_ids=None):

        pass

    def get_edge(self, source_key):
        pass

    def get_edge_latest_versions(self, source_key):
        pass

    def get_edge_history(self, source_key):
        pass

    def get_edge_version(self, id):
        pass

    '''
    GRAPH METHODS
    '''

    def create_graph(self, source_key, name, tags=None):
        pass

    def create_graph_version(self,
                             graph_id,
                             edge_version_ids,
                             reference=None,
                             reference_parameters=None,
                             tags=None,
                             structure_version_id=-1,
                             parent_ids=None):

        pass

    def get_graph(self, source_key):
        pass

    def get_graph_latest_versions(self, source_key):
        pass

    def get_graph_history(self, source_key):
        pass

    def get_graph_version(self, id):
        pass

    '''
    NODE METHODS
    '''

    def create_node(self, source_key, name, tags=None):
        pass

    def create_node_version(self,
                            node_id,
                            reference=None,
                            reference_parameters=None,
                            tags=None,
                            structure_version_id=-1,
                            parent_ids=None):

        pass

    def get_node(self, source_key):
        pass

    def get_node_latest_versions(self, source_key):
        pass

    def get_node_history(self, source_key):
        pass

    def get_node_version(self, id):
        pass

    def get_node_version_adjacent_lineage(self, id):
        pass

    '''
    STRUCTURE METHODS
    '''

    def create_structure(self, source_key, name, tags=None):
        pass

    def create_structure_version(self,
                                 structure_id,
                                 attributes,
                                 parent_ids=None):

        pass

    def get_structure(self, source_key):
        pass

    def get_structure_latest_versions(self, source_key):
        pass

    def get_structure_history(self, source_key):
        pass

    def get_structure_version(self, id):
        pass

    '''
    LINEAGE EDGE METHODS
    '''

    def create_lineage_edge(self, source_key, name, tags=None):
        pass

    def create_lineage_edge_version(self,
                                    edge_id,
                                    to_rich_version_id,
                                    from_rich_version_id,
                                    reference=None,
                                    reference_parameters=None,
                                    tags=None,
                                    structure_version_id=-1,
                                    parent_ids=None):

        pass

    def get_lineage_edge(self, source_key):
        pass

    def get_lineage_edge_latest_versions(self, source_key):
        pass

    def get_lineage_edge_history(self, source_key):
        pass

    def get_lineage_edge_version(self, id):
        pass

    '''
    LINEAGE GRAPH METHODS
    '''

    def create_lineage_graph(self, source_key, name, tags=None):
        pass

    def create_lineage_graph_version(self,
                                     lineage_graph_id,
                                     lineage_edge_version_ids,
                                     reference=None,
                                     reference_parameters=None,
                                     tags=None,
                                     structure_version_id=-1,
                                     parent_ids=None):

        pass

    def get_lineage_graph(self, source_key):
        pass

    def get_lineage_graph_latest_versions(self, source_key):
        pass

    def get_lineage_graph_history(self, source_key):
        pass

    def get_lineage_graph_version(self, id):
        pass