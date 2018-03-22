import unittest
import uuid

import ground.client as client


class TestClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = client.GroundClient()

    def test_node(self):
        """
        Tests most of the node access methods
        """
        source_key = uuid.uuid4().hex

        node = self.client.create_node(source_key, source_key)
        # test created node is valid
        self.assertTrue(
            node is not None,
            msg="create_node with source_key = {} returned None instead of a node"
            .format(source_key)
        )
        self.assertTrue(
            source_key == node.get_source_key(),
            msg="node created with source key {} has a differing source key: {}"
            .format(source_key, node.get_source_key())
        )

        retrieved_node = self.client.get_node(source_key)
        # test retrieved node_version is valid
        self.assertTrue(
            retrieved_node is not None,
            msg='valid call to get_node returned None'
        )
        self.assertTrue(
            retrieved_node == node,
            msg='valid call to get_node returned incorrect data'
        )

        node_version = self.client.create_node_version(node.get_id())
        # test created node_version is valid
        self.assertTrue(
            node_version is not None,
            msg='create_node_version with node_id={} returned None instead of a node version'
            .format(node.get_id())
        )
        self.assertTrue(
            node_version.get_node_id() == node.get_id(),
            msg="created node_version's node_id does not match id of node"
        )

        retrieved_nv = self.client.get_node_version(node_version.get_id())
        # test retrieved node_version is valid
        self.assertTrue(
            retrieved_nv is not None,
            msg='valid call to get_node_version returned None'
        )
        self.assertTrue(
            retrieved_nv == node_version,
            msg='valid call to get_node_version returned incorrect data'
        )

        latest = self.client.get_node_latest_versions(source_key)
        # test latest_version matches created node_version
        self.assertTrue(
            latest == [node_version.get_id()],
            msg="get_node_latest_version returns incorrect versions"
        )

        # TODO: uncomment when server side bug fixed
        # history = self.client.get_node_history(source_key)
        # expected_history = {
        #     '0': [node_version.get_id()]
        # }
        # self.assertTrue(
        #     history == expected_history,
        #     "call to get_node_history did not match expected value"
        # )

    def test_graph(self):
        """
        Tests most of the node access methods
        """
        source_key = uuid.uuid4().hex

        graph = self.client.create_graph(source_key, source_key)
        # test created graph is valid
        self.assertTrue(
            graph is not None,
            msg="create_graph with source_key = {} returned None instead of a graph"
            .format(source_key)
        )
        self.assertTrue(
            source_key == graph.get_source_key(),
            msg="graph created with source key {} has a differing source key: {}"
            .format(source_key, graph.get_source_key())
        )

        retrieved_graph = self.client.get_graph(source_key)
        # test retrieved graph_version is valid
        self.assertTrue(
            retrieved_graph is not None,
            msg='valid call to get_graph returned None'
        )
        self.assertTrue(
            retrieved_graph == graph,
            msg='valid call to get_graph returned incorrect data'
        )

        graph_version = self.client.create_graph_version(graph.get_id(), [])
        # test created graph_version is valid
        self.assertTrue(
            graph_version is not None,
            msg='create_graph_version with graph_id={} returned None instead of a graph version'
            .format(graph.get_id())
        )
        self.assertTrue(
            graph_version.get_graph_id() == graph.get_id(),
            msg="created graph_version's graph_id does not match id of graph"
        )

        retrieved_gv = self.client.get_graph_version(graph_version.get_id())
        # test retrieved graph_version is valid
        self.assertTrue(
            retrieved_gv is not None,
            msg='valid call to get_graph_version returned None'
        )
        self.assertTrue(
            retrieved_gv == graph_version,
            msg='valid call to get_graph_version returned incorrect data'
        )

        latest = self.client.get_graph_latest_versions(source_key)
        # test latest_version matches created graph_version
        self.assertTrue(
            latest == [graph_version.get_id()],
            msg="get_graph_latest_version returns incorrect versions"
        )

        # TODO: uncomment when server side bug fixed
        # history = self.client.get_graph_history(source_key)
        # expected_history = {
        #     '0': [graph_version.get_id()]
        # }
        # self.assertTrue(
        #     history == expected_history,
        #     "call to get_graph_history did not match expected value"
        # )

    def test_edge(self):
        """
        Tests most of the node access methods
        """
        # create nodes/nodeversions for edges
        node1_source_key = uuid.uuid4().hex
        node2_source_key = uuid.uuid4().hex
        node1 = self.client.create_node(node1_source_key, node1_source_key)
        node2 = self.client.create_node(node2_source_key, node2_source_key)
        nv1   = self.client.create_node_version(node1.get_id())
        nv2   = self.client.create_node_version(node2.get_id())

        source_key = uuid.uuid4().hex

        edge = self.client.create_edge(source_key, source_key, node1.get_id(), node2.get_id())
        # test created edge is valid
        self.assertTrue(
            edge is not None,
            msg="create_edge with source_key = {} returned None instead of a edge"
            .format(source_key)
        )
        self.assertTrue(
            source_key == edge.get_source_key(),
            msg="edge created with source key {} has a differing source key: {}"
            .format(source_key, edge.get_source_key())
        )

        retrieved_edge = self.client.get_edge(source_key)
        # test retrieved edge_version is valid
        self.assertTrue(
            retrieved_edge is not None,
            msg='valid call to get_edge returned None'
        )
        self.assertTrue(
            retrieved_edge == edge,
            msg='valid call to get_edge returned incorrect data'
        )

        edge_version = self.client.create_edge_version(edge.get_id(), nv1.get_id(), nv2.get_id())
        # test created edge_version is valid
        self.assertTrue(
            edge_version is not None,
            msg='create_edge_version with edge_id={} returned None instead of a edge version'
            .format(edge.get_id())
        )
        self.assertTrue(
            edge_version.get_edge_id() == edge.get_id(),
            msg="created edge_version's edge_id does not match id of edge"
        )

        retrieved_nv = self.client.get_edge_version(edge_version.get_id())
        # test retrieved edge_version is valid
        self.assertTrue(
            retrieved_nv is not None,
            msg='valid call to get_edge_version returned None'
        )
        self.assertTrue(
            retrieved_nv == edge_version,
            msg='valid call to get_edge_version returned incorrect data'
        )

        latest = self.client.get_edge_latest_versions(source_key)
        # test latest_version matches created edge_version
        self.assertTrue(
            latest == [edge_version.get_id()],
            msg="get_edge_latest_version returns incorrect versions"
        )

        # TODO: uncomment when server side bug fixed
        # history = self.client.get_edge_history(source_key)
        # expected_history = {
        #     '0': [edge_version.get_id()]
        # }
        # self.assertTrue(
        #     history == expected_history,
        #     "call to get_edge_history did not match expected value"
        # )

    def test_structure(self):
        """
        Tests most of the node access methods
        """
        source_key = uuid.uuid4().hex

        structure = self.client.create_structure(source_key, source_key)
        # test created structure is valid
        self.assertTrue(
            structure is not None,
            msg="create_structure with source_key = {} returned None instead of a structure"
            .format(source_key)
        )
        self.assertTrue(
            source_key == structure.get_source_key(),
            msg="structure created with source key {} has a differing source key: {}"
            .format(source_key, structure.get_source_key())
        )

        retrieved_structure = self.client.get_structure(source_key)
        # test retrieved structure_version is valid
        self.assertTrue(
            retrieved_structure is not None,
            msg='valid call to get_structure returned None'
        )
        self.assertTrue(
            retrieved_structure == structure,
            msg='valid call to get_structure returned incorrect data'
        )

        structure_version = self.client.create_structure_version(structure.get_id(), {})
        # test created structure_version is valid
        self.assertTrue(
            structure_version is not None,
            msg='create_structure_version with structure_id={} returned None instead of a structure version'
            .format(structure.get_id())
        )
        self.assertTrue(
            structure_version.get_structure_id() == structure.get_id(),
            msg="created structure_version's structure_id does not match id of structure"
        )

        retrieved_nv = self.client.get_structure_version(structure_version.get_id())
        # test retrieved structure_version is valid
        self.assertTrue(
            retrieved_nv is not None,
            msg='valid call to get_structure_version returned None'
        )
        self.assertTrue(
            retrieved_nv == structure_version,
            msg='valid call to get_structure_version returned incorrect data'
        )

        latest = self.client.get_structure_latest_versions(source_key)
        # test latest_version matches created structure_version
        self.assertTrue(
            latest == [structure_version.get_id()],
            msg="get_structure_latest_version returns incorrect versions"
        )

        # TODO: uncomment when server side bug fixed
        # history = self.client.get_structure_history(source_key)
        # expected_history = {
        #     '0': [structure_version.get_id()]
        # }
        # self.assertTrue(
        #     history == expected_history,
        #     "call to get_structure_history did not match expected value"
        # )

    def test_lineage_edge(self):
        """
        Tests most of the node access methods
        """
        # create rich versions aka node versions
        node1_source_key = uuid.uuid4().hex
        node2_source_key = uuid.uuid4().hex
        node1 = self.client.create_node(node1_source_key, node1_source_key)
        node2 = self.client.create_node(node2_source_key, node2_source_key)
        nv1 = self.client.create_node_version(node1.get_id())
        nv2 = self.client.create_node_version(node2.get_id())

        source_key = uuid.uuid4().hex

        lineage_edge = self.client.create_lineage_edge(source_key, source_key)
        # test created lineage_edge is valid
        self.assertTrue(
            lineage_edge is not None,
            msg="create_lineage_edge with source_key = {} returned None instead of a lineage_edge"
            .format(source_key)
        )
        self.assertTrue(
            source_key == lineage_edge.get_source_key(),
            msg="lineage_edge created with source key {} has a differing source key: {}"
            .format(source_key, lineage_edge.get_source_key())
        )

        retrieved_lineage_edge = self.client.get_lineage_edge(source_key)
        # test retrieved lineage_edge_version is valid
        self.assertTrue(
            retrieved_lineage_edge is not None,
            msg='valid call to get_lineage_edge returned None'
        )
        self.assertTrue(
            retrieved_lineage_edge == lineage_edge,
            msg='valid call to get_lineage_edge returned incorrect data'
        )

        lineage_edge_version = self.client.create_lineage_edge_version(
            lineage_edge.get_id(), nv1.get_id(), nv2.get_id()
        )
        # test created lineage_edge_version is valid
        self.assertTrue(
            lineage_edge_version is not None,
            msg='create_lineage_edge_version with lineage_edge_id={} returned None instead of a lineage_edge version'
            .format(lineage_edge.get_id())
        )
        self.assertTrue(
            lineage_edge_version.get_lineage_edge_id() == lineage_edge.get_id(),
            msg="created lineage_edge_version's lineage_edge_id does not match id of lineage_edge"
        )

        retrieved_nv = self.client.get_lineage_edge_version(lineage_edge_version.get_id())
        # test retrieved lineage_edge_version is valid
        self.assertTrue(
            retrieved_nv is not None,
            msg='valid call to get_lineage_edge_version returned None'
        )
        self.assertTrue(
            retrieved_nv == lineage_edge_version,
            msg='valid call to get_lineage_edge_version returned incorrect data'
        )

        latest = self.client.get_lineage_edge_latest_versions(source_key)
        # test latest_version matches created lineage_edge_version
        self.assertTrue(
            latest == [lineage_edge_version.get_id()],
            msg="get_lineage_edge_latest_version returns incorrect versions"
        )

        # TODO: uncomment when server side bug fixed
        # history = self.client.get_lineage_edge_history(source_key)
        # expected_history = {
        #     '0': [lineage_edge_version.get_id()]
        # }
        # self.assertTrue(
        #     history == expected_history,
        #     "call to get_lineage_edge_history did not match expected value"
        # )

    def test_lineage_graph(self):
        """
        Tests most of the node access methods
        """
        # create rich versions aka node versions
        node1_source_key = uuid.uuid4().hex
        node2_source_key = uuid.uuid4().hex
        node1 = self.client.create_node(node1_source_key, node1_source_key)
        node2 = self.client.create_node(node2_source_key, node2_source_key)
        nv1 = self.client.create_node_version(node1.get_id())
        nv2 = self.client.create_node_version(node2.get_id())

        source_key = uuid.uuid4().hex

        lineage_graph = self.client.create_lineage_graph(source_key, source_key)
        # test created lineage_graph is valid
        self.assertTrue(
            lineage_graph is not None,
            msg="create_lineage_graph with source_key = {} returned None instead of a lineage_graph"
            .format(source_key)
        )
        self.assertTrue(
            source_key == lineage_graph.get_source_key(),
            msg="lineage_graph created with source key {} has a differing source key: {}"
            .format(source_key, lineage_graph.get_source_key())
        )

        retrieved_lineage_graph = self.client.get_lineage_graph(source_key)
        # test retrieved lineage_graph_version is valid
        self.assertTrue(
            retrieved_lineage_graph is not None,
            msg='valid call to get_lineage_graph returned None'
        )
        self.assertTrue(
            retrieved_lineage_graph == lineage_graph,
            msg='valid call to get_lineage_graph returned incorrect data'
        )

        lineage_graph_version = self.client.create_lineage_graph_version(
            lineage_graph.get_id(), []
        )
        # test created lineage_graph_version is valid
        self.assertTrue(
            lineage_graph_version is not None,
            msg='create_lineage_graph_version with lineage_graph_id={} returned None instead of a lineage_graph version'
            .format(lineage_graph.get_id())
        )
        self.assertTrue(
            lineage_graph_version.get_lineage_graph_id() == lineage_graph.get_id(),
            msg="created lineage_graph_version's lineage_graph_id does not match id of lineage_graph"
        )

        retrieved_nv = self.client.get_lineage_graph_version(lineage_graph_version.get_id())
        # test retrieved lineage_graph_version is valid
        self.assertTrue(
            retrieved_nv is not None,
            msg='valid call to get_lineage_graph_version returned None'
        )
        self.assertTrue(
            retrieved_nv == lineage_graph_version,
            msg='valid call to get_lineage_graph_version returned incorrect data'
        )

        latest = self.client.get_lineage_graph_latest_versions(source_key)
        # test latest_version matches created lineage_graph_version
        self.assertTrue(
            latest == [lineage_graph_version.get_id()],
            msg="get_lineage_graph_latest_version returns incorrect versions"
        )

        # TODO: uncomment when server side bug fixed
        # history = self.client.get_lineage_graph_history(source_key)
        # expected_history = {
        #     '0': [lineage_graph_version.get_id()]
        # }
        # self.assertTrue(
        #     history == expected_history,
        #     "call to get_lineage_graph_history did not match expected value"
        # )


if __name__ == '__main__':
    unittest.main()
