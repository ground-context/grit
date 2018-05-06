import unittest
import uuid
import time
import argparse

import ground.grit as grit
import ground.common.model as model

from memory_profiler import profile

VERBOSE = False


class TestClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = grit.GroundClient('git')

    # @profile
    def test_node_create(self):
        source_key = uuid.uuid4().hex
        start = time.time()
        node = self.client.createNode(source_key, source_key)

        self.assertTrue(
            node is not None,
            msg="createNode with source_key = {} returned None instead of a node"
            .format(source_key)
        )
        self.assertTrue(
            type(node) == model.core.node.Node,
            msg="createNode returned node of type '{}' rather than 'Node'"
            .format(type(node))
        )
        self.assertTrue(
            source_key == node.get_source_key(),
            msg="node created with source key {} has a differing source key: {}"
            .format(source_key, node.get_source_key())
        )

        # now try to create the same node again
        with self.assertRaises(FileExistsError):
            self.client.createNode(source_key, source_key)

        elapsed = time.time() - start
        if VERBOSE:
            print('Time elapsed is: ' + str(elapsed) + " seconds")
        return node

    # @profile
    def test_node_get(self):
        node = self.test_node_create()

        # I can try to get node that exists, or node that not exists

        # Get node that exists
        start = time.time()
        got_node = self.client.getNode(node.get_source_key())
        self.assertTrue(
            got_node is not None,
            msg='valid call to getNode returned None'
        )
        self.assertTrue(
            type(got_node) == model.core.node.Node,
            msg="getNode returned node that is of type '{}' rather than 'Node'"
            .format(type(node))
        )
        self.assertTrue(
            got_node == node,
            msg='valid call to getNode returned incorrect data'
        )

        # Get node that not exists
        with self.assertRaises(FileNotFoundError):
            self.client.getNode(uuid.uuid4().hex)
        elapsed = time.time() - start
        if VERBOSE:
            print('Time elapsed is: ' + str(elapsed) + " seconds")

    # @profile
    def test_node_version_create(self):
        node = self.test_node_create()

        # I can try to create a nv for a node that exists,
        #   or nv for node that not exists

        # Create a node_version for a node that exists
        start = time.time()
        node_version = self.client.createNodeVersion(int(node.get_id()))
        self.assertTrue(
            node_version is not None,
            msg='createNodeVersion with node_id={} returned None instead of a node version'
            .format(node.get_id())
        )
        self.assertTrue(
            type(node_version) == model.core.node_version.NodeVersion,
            msg="createNodeVersion returned nodeVersion of type '{}' rather than 'NodeVersion'"
            .format(type(node_version))
        )
        self.assertTrue(
            node_version.get_node_id() == node.get_id(),
            msg="created node_version's node_id does not match id of node"
        )

        # Create a node_version for a node that not exists
        with self.assertRaises(KeyError):
            self.client.createNodeVersion(int(uuid.uuid4().int))

        # Now as above, but passing in a string rather than an int

        # Create a node_version for a node that exists
        node_version = self.client.createNodeVersion(str(node.get_id()))
        self.assertTrue(
            node_version is not None,
            msg='createNodeVersion with node_id={} returned None instead of a node version'
            .format(node.get_id())
        )
        self.assertTrue(
            type(node_version) == model.core.node_version.NodeVersion,
            msg="createNodeVersion returned nodeVersion of type '{}' rather than 'NodeVersion'"
            .format(type(node_version))
        )
        self.assertTrue(
            node_version.get_node_id() == node.get_id(),
            msg="created node_version's node_id does not match id of node"
        )

        # Create a node_version for a node that not exists
        with self.assertRaises(KeyError):
            self.client.createNodeVersion(str(uuid.uuid4().int))

        # Total: created two distinct node versions for the same node.
        elapsed = time.time() - start
        if VERBOSE:
            print('Time elapsed is: ' + str(elapsed) + " seconds")
        return node_version

    # @profile
    def test_node_version_get_chain(self):
        node = self.test_node_create()

        nv1 = self.client.createNodeVersion(node.get_id())
        nv2 = self.client.createNodeVersion(node.get_id(), parentIds=[nv1.get_id()])
        nv3 = self.client.createNodeVersion(node.get_id(), parentIds=[nv2.get_id()])

        start = time.time()

        node_version = self.client.getNodeVersion(nv2.get_id())

        self.assertTrue(
            node_version is not None,
            msg='getNodeVersion with node_id={} returned None instead of a node version'
            .format(node.get_id())
        )
        self.assertTrue(
            type(node_version) == model.core.node_version.NodeVersion,
            msg="getNodeVersion returned nodeVersion of type '{}' rather than 'NodeVersion'"
            .format(type(node_version))
        )
        self.assertTrue(
            node_version.get_node_id() == node.get_id(),
            msg="getNodeVersion's node_id does not match id of node"
        )
        self.assertTrue(
            node_version == nv2,
            msg="Stored and retrieved node versions mismatch"
        )
        elapsed = time.time() - start
        if VERBOSE:
            print('Time elapsed is: ' + str(elapsed) + " seconds")

        return node, nv1, nv2, nv3

    # @profile
    def test_node_version_get_fan(self):
        node = self.test_node_create()

        nv1 = self.client.createNodeVersion(node.get_id())
        nv2 = self.client.createNodeVersion(node.get_id())
        nv3 = self.client.createNodeVersion(node.get_id())

        start = time.time()

        node_version = self.client.getNodeVersion(nv2.get_id())

        self.assertTrue(
            node_version is not None,
            msg='getNodeVersion with node_id={} returned None instead of a node version'
            .format(node.get_id())
        )
        self.assertTrue(
            type(node_version) == model.core.node_version.NodeVersion,
            msg="getNodeVersion returned nodeVersion of type '{}' rather than 'NodeVersion'"
            .format(type(node_version))
        )
        self.assertTrue(
            node_version.get_node_id() == node.get_id(),
            msg="getNodeVersion's node_id does not match id of node"
        )
        self.assertTrue(
            node_version == nv2,
            msg="Stored and retrieved node versions mismatch"
        )
        elapsed = time.time() - start
        if VERBOSE:
            print('Time elapsed is: ' + str(elapsed) + " seconds")

        return node, nv1, nv2, nv3

    # @profile
    def test_node_version_get_fan_out_in(self):
        node = self.test_node_create()

        nv1 = self.client.createNodeVersion(node.get_id())
        nv2 = self.client.createNodeVersion(node.get_id())
        nv3 = self.client.createNodeVersion(node.get_id())

        nv4 = self.client.createNodeVersion(node.get_id(), parentIds=[nv1.get_id(), nv2.get_id(), nv3.get_id()])
        start = time.time()

        node_version = self.client.getNodeVersion(nv2.get_id())

        self.assertTrue(
            node_version is not None,
            msg='getNodeVersion with node_id={} returned None instead of a node version'
            .format(node.get_id())
        )
        self.assertTrue(
            type(node_version) == model.core.node_version.NodeVersion,
            msg="getNodeVersion returned nodeVersion of type '{}' rather than 'NodeVersion'"
            .format(type(node_version))
        )
        self.assertTrue(
            node_version.get_node_id() == node.get_id(),
            msg="getNodeVersion's node_id does not match id of node"
        )
        self.assertTrue(
            node_version == nv2,
            msg="Stored and retrieved node versions mismatch"
        )

        node_version = self.client.getNodeVersion(nv4.get_id())

        self.assertTrue(
            node_version is not None,
            msg='getNodeVersion with node_id={} returned None instead of a node version'
            .format(node.get_id())
        )
        self.assertTrue(
            type(node_version) == model.core.node_version.NodeVersion,
            msg="getNodeVersion returned nodeVersion of type '{}' rather than 'NodeVersion'"
            .format(type(node_version))
        )
        self.assertTrue(
            node_version.get_node_id() == node.get_id(),
            msg="getNodeVersion's node_id does not match id of node"
        )
        self.assertTrue(
            node_version == nv4,
            msg="Stored and retrieved node versions mismatch"
        )
        elapsed = time.time() - start
        if VERBOSE:
            print('Time elapsed is: ' + str(elapsed) + " seconds")

    # @profile
    def test_node_version_get_dag(self):
        node = self.test_node_create()

        nv1 = self.client.createNodeVersion(node.get_id())
        nv2 = self.client.createNodeVersion(node.get_id(), parentIds=[nv1.get_id()])
        nv3 = self.client.createNodeVersion(node.get_id(), parentIds=[nv1.get_id()])

        nv4 = self.client.createNodeVersion(node.get_id(), parentIds=[nv2.get_id(), nv3.get_id()])
        nv5 = self.client.createNodeVersion(node.get_id(), parentIds=[nv4.get_id()])
        nv6 = self.client.createNodeVersion(node.get_id(), parentIds=[nv4.get_id()])

        start = time.time()

        node_version = self.client.getNodeVersion(nv2.get_id())

        self.assertTrue(
            node_version is not None,
            msg='getNodeVersion with node_id={} returned None instead of a node version'
            .format(node.get_id())
        )
        self.assertTrue(
            type(node_version) == model.core.node_version.NodeVersion,
            msg="getNodeVersion returned nodeVersion of type '{}' rather than 'NodeVersion'"
            .format(type(node_version))
        )
        self.assertTrue(
            node_version.get_node_id() == node.get_id(),
            msg="getNodeVersion's node_id does not match id of node"
        )
        self.assertTrue(
            node_version == nv2,
            msg="Stored and retrieved node versions mismatch"
        )

        node_version = self.client.getNodeVersion(nv1.get_id())

        self.assertTrue(
            node_version is not None,
            msg='getNodeVersion with node_id={} returned None instead of a node version'
            .format(node.get_id())
        )
        self.assertTrue(
            type(node_version) == model.core.node_version.NodeVersion,
            msg="getNodeVersion returned nodeVersion of type '{}' rather than 'NodeVersion'"
            .format(type(node_version))
        )
        self.assertTrue(
            node_version.get_node_id() == node.get_id(),
            msg="getNodeVersion's node_id does not match id of node"
        )
        self.assertTrue(
            node_version == nv1,
            msg="Stored and retrieved node versions mismatch"
        )

        node_version = self.client.getNodeVersion(nv4.get_id())

        self.assertTrue(
            node_version is not None,
            msg='getNodeVersion with node_id={} returned None instead of a node version'
            .format(node.get_id())
        )
        self.assertTrue(
            type(node_version) == model.core.node_version.NodeVersion,
            msg="getNodeVersion returned nodeVersion of type '{}' rather than 'NodeVersion'"
            .format(type(node_version))
        )
        self.assertTrue(
            node_version.get_node_id() == node.get_id(),
            msg="getNodeVersion's node_id does not match id of node"
        )
        self.assertTrue(
            node_version == nv4,
            msg="Stored and retrieved node versions mismatch"
        )

        node_version = self.client.getNodeVersion(nv5.get_id())

        self.assertTrue(
            node_version is not None,
            msg='getNodeVersion with node_id={} returned None instead of a node version'
            .format(node.get_id())
        )
        self.assertTrue(
            type(node_version) == model.core.node_version.NodeVersion,
            msg="getNodeVersion returned nodeVersion of type '{}' rather than 'NodeVersion'"
            .format(type(node_version))
        )
        self.assertTrue(
            node_version.get_node_id() == node.get_id(),
            msg="getNodeVersion's node_id does not match id of node"
        )
        self.assertTrue(
            node_version == nv5,
            msg="Stored and retrieved node versions mismatch"
        )

        node_version = self.client.getNodeVersion(nv6.get_id())

        self.assertTrue(
            node_version is not None,
            msg='getNodeVersion with node_id={} returned None instead of a node version'
            .format(node.get_id())
        )
        self.assertTrue(
            type(node_version) == model.core.node_version.NodeVersion,
            msg="getNodeVersion returned nodeVersion of type '{}' rather than 'NodeVersion'"
            .format(type(node_version))
        )
        self.assertTrue(
            node_version.get_node_id() == node.get_id(),
            msg="getNodeVersion's node_id does not match id of node"
        )
        self.assertTrue(
            node_version == nv6,
            msg="Stored and retrieved node versions mismatch"
        )
        elapsed = time.time() - start
        if VERBOSE:
            print('Time elapsed is: ' + str(elapsed) + " seconds")

    # @profile
    def test_node_version_latest_get(self):
        node = self.test_node_create()

        nv1 = self.client.createNodeVersion(node.get_id())
        nv2 = self.client.createNodeVersion(node.get_id(), parentIds=[nv1.get_id()])
        nv3 = self.client.createNodeVersion(node.get_id(), parentIds=[nv1.get_id()])

        nv4 = self.client.createNodeVersion(node.get_id(), parentIds=[nv2.get_id(), nv3.get_id()])
        nv5 = self.client.createNodeVersion(node.get_id(), parentIds=[nv4.get_id()])
        nv6 = self.client.createNodeVersion(node.get_id(), parentIds=[nv4.get_id()])

        start = time.time()
        node_versions = self.client.getNodeLatestVersions(node.get_source_key())

        for node_version in node_versions:
            self.assertTrue(
                node_version is not None,
                msg='getNodeLatestVersions with node_id={} returned None instead of a node version'
                .format(node.get_id())
            )
            self.assertTrue(
                type(node_version) == model.core.node_version.NodeVersion,
                msg="getNodeLatestVersions returned nodeVersion of type '{}' rather than 'NodeVersion'"
                .format(type(node_version))
            )
            self.assertTrue(
                node_version.get_node_id() == node.get_id(),
                msg="getNodeLatestVersions node_id does not match id of node"
            )
            self.assertTrue(
                node_version == nv5 or node_version == nv6,
                msg="Stored and retrieved node versions mismatch"
            )
        self.assertTrue(
            len(node_versions) == 2,
            msg='getNodeLatestVersions returned {} node versions but there are 2 latest.'
            .format(len(node_versions))
        )
        self.assertTrue(
            node_versions[0] != node_versions[1],
            msg='getNodeLatestVersions returned two node versions that are equal but should be different'
        )
        elapsed = time.time() - start
        if VERBOSE:
            print('Time elapsed is: ' + str(elapsed) + " seconds")

    # @profile
    def test_node_get_history(self):
        # dag
        node = self.test_node_create()

        nv1 = self.client.createNodeVersion(node.get_id())
        nv2 = self.client.createNodeVersion(node.get_id(), parentIds=[nv1.get_id()])
        nv3 = self.client.createNodeVersion(node.get_id(), parentIds=[nv1.get_id()])

        nv4 = self.client.createNodeVersion(node.get_id(), parentIds=[nv2.get_id(), nv3.get_id()])
        nv5 = self.client.createNodeVersion(node.get_id(), parentIds=[nv4.get_id()])
        nv6 = self.client.createNodeVersion(node.get_id(), parentIds=[nv4.get_id()])

        start = time.time()
        dag = self.client.getNodeHistory(node.get_source_key())

        self.assertTrue(
            dag[nv1.get_id()] == {nv2.get_id(), nv3.get_id()},
            msg="Invalid children"
        )
        self.assertTrue(
            dag[nv2.get_id()] == {nv4.get_id(), },
            msg="Invalid children"
        )
        self.assertTrue(
            dag[nv3.get_id()] == {nv4.get_id(), },
            msg="Invalid children"
        )
        self.assertTrue(
            dag[nv4.get_id()] == {nv5.get_id(), nv6.get_id()},
            msg="Invalid children"
        )
        self.assertTrue(
            dag[nv5.get_id()] == set([]),
            msg="Invalid children"
        )
        self.assertTrue(
            dag[nv6.get_id()] == set([]),
            msg="Invalid children"
        )
        self.assertTrue(
            len(dag) == 6,
            msg="Expected 6 elements but found {}".format(len(dag))
        )

        elapsed = time.time() - start
        if VERBOSE:
            print('Time elapsed in dag is: ' + str(elapsed) + " seconds")

        # fan out in
        node = self.test_node_create()

        nv1 = self.client.createNodeVersion(node.get_id())
        nv2 = self.client.createNodeVersion(node.get_id())
        nv3 = self.client.createNodeVersion(node.get_id())

        nv4 = self.client.createNodeVersion(node.get_id(), parentIds=[nv1.get_id(), nv2.get_id(), nv3.get_id()])

        start = time.time()

        dag = self.client.getNodeHistory(node.get_source_key())

        self.assertTrue(
            dag[nv1.get_id()] == {nv4.get_id(), },
            msg="Invalid children"
        )
        self.assertTrue(
            dag[nv2.get_id()] == {nv4.get_id(), },
            msg="Invalid children"
        )
        self.assertTrue(
            dag[nv3.get_id()] == {nv4.get_id(), },
            msg="Invalid children"
        )
        self.assertTrue(
            dag[nv4.get_id()] == set([]),
            msg="Invalid children"
        )
        self.assertTrue(
            len(dag) == 4,
            msg="Expected 4 elements but found {}".format(len(dag))
        )
        elapsed = time.time() - start
        if VERBOSE:
            print('Time elapsed in fan out in is: ' + str(elapsed) + " seconds")

        # chain
        node = self.test_node_create()

        nv1 = self.client.createNodeVersion(node.get_id())
        nv2 = self.client.createNodeVersion(node.get_id(), parentIds=[nv1.get_id()])
        nv3 = self.client.createNodeVersion(node.get_id(), parentIds=[nv2.get_id()])

        start = time.time()

        dag = self.client.getNodeHistory(node.get_source_key())

        self.assertTrue(
            dag[nv1.get_id()] == {nv2.get_id(), },
            msg="Invalid children"
        )
        self.assertTrue(
            dag[nv2.get_id()] == {nv3.get_id(), },
            msg="Invalid children"
        )
        self.assertTrue(
            dag[nv3.get_id()] == set([]),
            msg="Invalid children"
        )
        self.assertTrue(
            len(dag) == 3,
            msg="Expected 3 elements but found {}".format(len(dag))
        )
        elapsed = time.time() - start
        if VERBOSE:
            print('Time elapsed in chain is: ' + str(elapsed) + " seconds")

    # @profile
    def test_edge_create(self):
        # There are two alternatives:
        # Create an edge between two existing nodes
        # Create one edge between at least one non-existent node

        # Create an edge between two existing nodes
        node1 = self.test_node_create()
        node2 = self.test_node_create()

        source_key = uuid.uuid4().hex
        start = time.time()
        edge = self.client.createEdge(source_key, node1.get_id(), node2.get_id())

        self.assertTrue(
            edge is not None,
            msg="create_edge with source_key = {} returned None instead of a edge"
            .format(source_key)
        )
        self.assertTrue(
            type(edge) == model.core.edge.Edge,
            msg="createEdge returned edge of type '{}' rather than 'Edge'"
            .format(type(edge))
        )
        self.assertTrue(
            source_key == edge.get_source_key(),
            msg="edge created with source key {} has a differing source key: {}"
            .format(source_key, edge.get_source_key())
        )

        # Create an edge between at least one non-existent node
        with self.assertRaises(KeyError):
            self.client.createEdge(uuid.uuid4().hex, node1.get_id(), uuid.uuid4().int)

        # Create an edge with the same source key
        with self.assertRaises(FileExistsError):
            self.client.createEdge(source_key, node2.get_id(), node1.get_id())

        elapsed = time.time() - start
        if VERBOSE:
            print('Time elapsed is: ' + str(elapsed) + " seconds")

        return edge

    # @profile
    def test_edge_get(self):
        edge = self.test_edge_create()
        start = time.time()

        # I can try to get edge that exists or edge that not exists

        # Get edge that exists
        got_edge = self.client.getEdge(edge.get_source_key())
        self.assertTrue(
            got_edge is not None,
            msg='valid call to getEdge returned None'
        )
        self.assertTrue(
            type(got_edge) == model.core.edge.Edge,
            msg="getEdge returned edge that is of type '{}' rather than 'Edge'"
            .format(type(edge))
        )
        self.assertTrue(
            got_edge == edge,
            msg='valid call to getEdge returned incorrect data'
        )

        # Get edge that not exists
        with self.assertRaises(FileNotFoundError):
            self.client.getEdge(uuid.uuid4().hex)

        elapsed = time.time() - start
        if VERBOSE:
            print('Time elapsed is: ' + str(elapsed) + " seconds")

    # @profile
    def test_edge_version_create(self):
        edge = self.test_edge_create()
        from_node_id = edge.get_from_node_id()
        to_node_id = edge.get_to_node_id()

        # I can try to create a ev for an edge that exists,
        #   or ev for an edge that not exists

        # Create an edge_version for an edge that exists
        from_node_version = self.client.createNodeVersion(from_node_id)
        to_node_version = self.client.createNodeVersion(to_node_id)
        start = time.time()
        edge_version = self.client.createEdgeVersion(edge.get_id(), to_node_version.get_id(),
                                                     from_node_version.get_id())
        self.assertTrue(
            edge_version is not None,
            msg='createEdgeVersion with edge_id={} returned None instead of a node version'
            .format(edge.get_id())
        )
        self.assertTrue(
            type(edge_version) == model.core.edge_version.EdgeVersion,
            msg="createEdgeVersion returned edgeVersion of type '{}' rather than 'EdgeVersion'"
            .format(type(edge_version))
        )
        self.assertTrue(
            edge_version.get_edge_id() == edge.get_id(),
            msg="created edge_version's edge_id does not match id of edge"
        )

        # create an edge_version for an edge that does not exist
        with self.assertRaises(KeyError):
            self.client.createNodeVersion(uuid.uuid4().int, to_node_version.get_id(),
                                          from_node_version.get_id())

        elapsed = time.time() - start
        if VERBOSE:
            print('Time elapsed is: ' + str(elapsed) + " seconds")

        return edge_version

    # @profile
    def test_edge_version_get(self):
        edge = self.test_edge_create()
        from_node_id = edge.get_from_node_id()
        to_node_id = edge.get_to_node_id()

        # Create an edge version for an edge that exists
        from_node_version = self.client.createNodeVersion(from_node_id)
        to_node_version = self.client.createNodeVersion(to_node_id)
        edge_version = self.client.createEdgeVersion(edge.get_id(), to_node_version.get_id(),
                                                     from_node_version.get_id())

        start = time.time()
        got_edge_version = self.client.getEdgeVersion(edge_version.get_id())
        self.assertTrue(
            got_edge_version is not None,
            msg='valid call to getEdgeVersion returned None'
        )
        self.assertTrue(
            type(got_edge_version) == model.core.edge_version.EdgeVersion,
            msg="getEdgeVersion returned edge version that is of type '{}' rather than 'EdgeVersion'"
            .format(type(edge))
        )
        self.assertTrue(
            got_edge_version == edge_version,
            msg='valid call to getEdgeVersion returned incorrect data'
        )

        elapsed = time.time() - start
        if VERBOSE:
            print('Time elapsed is: ' + str(elapsed) + " seconds")

    # @profile
    def test_edge_version_latest_get(self):
        n1 = self.test_node_create()
        n2 = self.test_node_create()

        sk1 = uuid.uuid4().hex
        sk2 = uuid.uuid4().hex

        edge = self.client.createEdge(sk1, n1.get_id(), n2.get_id())
        ev1 = self.client.createEdgeVersion(edge.get_id(), n1.get_id(), n2.get_id())
        ev2 = self.client.createEdgeVersion(edge.get_id(), n1.get_id(), n2.get_id(), parentIds=[ev1.get_id(), ])
        ev3 = self.client.createEdgeVersion(edge.get_id(), n1.get_id(), n2.get_id(), parentIds=[ev2.get_id(), ])
        ev4 = self.client.createEdgeVersion(edge.get_id(), n1.get_id(), n2.get_id(), parentIds=[ev3.get_id(), ])
        ev5 = self.client.createEdgeVersion(edge.get_id(), n1.get_id(), n2.get_id(), parentIds=[ev3.get_id(), ])

        start = time.time()
        edge_versions = self.client.getEdgeLatestVersions(edge.get_source_key())

        for edge_version in edge_versions:
            self.assertTrue(
                edge_version is not None,
                msg='getEdgeLatestVersions with edge_id={} returned None instead of a edge version'
                .format(edge.get_id())
            )
            self.assertTrue(
                type(edge_version) == model.core.edge_version.EdgeVersion,
                msg="getEdgeLatestVersions returned edgeVersion of type '{}' rather than 'EdgeVersion'"
                .format(type(edge_version))
            )
            self.assertTrue(
                edge_version.get_edge_id() == edge.get_id(),
                msg="getEdgeLatestVersions edge_id does not match id of edge"
            )
            self.assertTrue(
                edge_version == ev4 or edge_version == ev5,
                msg="Stored and retrieved edge versions mismatch"
            )
        self.assertTrue(
            len(edge_versions) == 2,
            msg='getEdgeLatestVersions returned {} edge versions but there are 2 latest.'
            .format(len(edge_versions))
        )
        self.assertTrue(
            edge_versions[0] != edge_versions[1],
            msg='getEdgeLatestVersions returned two edge versions that are equal but should be different'
        )

        elapsed = time.time() - start
        if VERBOSE:
            print('Time elapsed is: ' + str(elapsed) + " seconds")

    # @profile
    def test_edge_get_history(self):
        pass

    # @profile
    def test_lineage_edge_version_get(self):
        pass

    # @profile
    def test_lineage_edge_version_latest_get(self):
        pass

    # @profile
    def test_lineage_edge_get_history(self):
        pass

    # @profile
    def test_lineage_edge_create(self):
        source_key = uuid.uuid4().hex
        start = time.time()
        node = self.client.createLineageEdge(source_key, source_key)

        self.assertTrue(
            node is not None,
            msg="createLineageEdge with source_key = {} returned None instead of a lineage edge"
            .format(source_key)
        )
        self.assertTrue(
            type(node) == model.usage.lineage_edge.LineageEdge,
            msg="createLineageEdge returned node of type '{}' rather than 'LineageEdge'"
            .format(type(node))
        )
        self.assertTrue(
            source_key == node.get_source_key(),
            msg="lineage edge created with source key {} has a differing source key: {}"
            .format(source_key, node.get_source_key())
        )

        # now try to create the same node again
        with self.assertRaises(FileExistsError):
            self.client.createLineageEdge(source_key, source_key)

        elapsed = time.time() - start
        if VERBOSE:
            print('Time elapsed is: ' + str(elapsed) + " seconds")

        return node

    # @profile
    def test_lineage_edge_get(self):
        node = self.test_lineage_edge_create()

        # I can try to get node that exists, or node that not exists

        # Get node that exists
        start = time.time()
        got_node = self.client.getLineageEdge(node.get_source_key())
        self.assertTrue(
            got_node is not None,
            msg='valid call to getLineageEdge returned None'
        )
        self.assertTrue(
            type(got_node) == model.usage.lineage_edge.LineageEdge,
            msg="getLineageEdge returned node that is of type '{}' rather than 'LineageEdge'"
            .format(type(node))
        )
        self.assertTrue(
            got_node == node,
            msg='valid call to getLineageEdge returned incorrect data'
        )

        # Get node that not exists
        with self.assertRaises(FileNotFoundError):
            self.client.getLineageEdge(uuid.uuid4().hex)

        elapsed = time.time() - start
        if VERBOSE:
            print('Time elapsed is: ' + str(elapsed) + " seconds")

    # @profile
    def test_lineage_edge_version_create(self):
        lineage_edge = self.test_lineage_edge_create()
        nv1 = self.test_node_version_create()
        nv2 = self.test_node_version_create()

        # I can try to create a ev for an edge that exists,
        #   or ev for an edge that not exists

        # Create an edge_version for an edge that exists
        start = time.time()
        edge_version = self.client.createLineageEdgeVersion(lineage_edge.get_id(), nv2.get_id(), nv1.get_id())
        self.assertTrue(
            edge_version is not None,
            msg='createLineageEdgeVersion with edge_id={} returned None instead of a lineage edge version'
            .format(lineage_edge.get_id())
        )
        self.assertTrue(
            type(edge_version) == model.usage.lineage_edge_version.LineageEdgeVersion,
            msg="createLineageEdgeVersion returned edgeVersion of type '{}' rather than 'LineageEdgeVersion'"
            .format(type(edge_version))
        )
        self.assertTrue(
            edge_version.get_lineage_edge_id() == lineage_edge.get_id(),
            msg="created edge_version's edge_id does not match id of lineage edge"
        )

        # create an edge_version for an edge that does not exist
        with self.assertRaises(KeyError):
            self.client.createNodeVersion(uuid.uuid4().int, nv2.get_id(),
                                          nv1.get_id())

        elapsed = time.time() - start
        if VERBOSE:
            print('Time elapsed is: ' + str(elapsed) + " seconds")

        return edge_version


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true', default=False)
    args = parser.parse_args()
    VERBOSE = args.verbose
    unittest.main()