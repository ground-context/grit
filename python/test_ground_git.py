import unittest
# noinspection PyUnresolvedReferences
import ground_git
# noinspection PyUnresolvedReferences
import ground.common.model as model
import json

class GroundTest(unittest.TestCase):
    def test_git_create(self):
        git = ground_git.GitImplementation()
        git.init()
        tag = model.version.tag.Tag({'id': 0, 'key': 'testKey', 'value': 'testValue'})
        nodeId = git.createNode('testSourceKey', 'testName', {'testTag': tag})
        nodeJson = {}
        with open(git.path + str(nodeId) + '.json', 'r') as f:
            nodeJson = json.loads(f.read())
        node= model.core.node.Node(nodeJson)
        compareNodeJson = {'id': node.get_item_id(), 'sourceKey': 'testSourceKey',
                       'name': 'testName', 'tags': {'testTag': tag}}
        # noinspection PyUnresolvedReferences
        compareNode = model.core.node.Node(compareNodeJson)
        self.assertEqual(node, compareNode)
        compareNodeGet = model.core.node.Node(git.getNode('testSourceKey'))
        self.assertEqual(node, compareNodeGet)

        edgeId = git.createEdge('testSourceKey', 'testFromNodeId', 'testToNodeId', 'testName', {'testTag': tag})
        edgeJson = {}
        with open(git.path + str(edgeId) + '.json', 'r') as f:
            edgeJson = json.loads(f.read())
        edge = model.core.edge.Edge(edgeJson)
        compareEdgeJson = {'id': edge.get_id(), 'sourceKey': 'testSourceKey', 'fromNodeId': 'testFromNodeId',
                       'toNodeId': 'testToNodeId', 'name': 'testName', 'tags': {'testTag': tag}}
        # noinspection PyUnresolvedReferences
        compareEdge = model.core.edge.Edge(compareEdgeJson)
        self.assertEqual(edge, compareEdge)
        compareEdgeGet = model.core.edge.Edge(git.getEdge('testSourceKey'))
        self.assertEqual(edge, compareEdgeGet)

        graphId = git.createGraph('testSourceKey', 'testName', {'testTag': tag})
        graphJson = {}
        with open(git.path + str(graphId) + '.json', 'r') as f:
            graphJson = json.loads(f.read())
        graph = model.core.graph.Graph(graphJson)
        compareGraphJson = {'id': graph.get_item_id(), 'sourceKey': 'testSourceKey',
                       'name': 'testName', 'tags': {'testTag': tag}}
        # noinspection PyUnresolvedReferences
        compareGraph = model.core.graph.Graph(compareGraphJson)
        self.assertEqual(graph, compareGraph)
        compareGraphGet = model.core.graph.Graph(git.getGraph('testSourceKey'))
        self.assertEqual(graph, compareGraphGet)

        structureId = git.createStructure('testSourceKey', 'testName', {'testTag': tag})
        structureJson = {}
        with open(git.path + str(structureId) + '.json', 'r') as f:
            structureJson = json.loads(f.read())
        structure = model.core.structure.Structure(structureJson)
        compareStructureJson = {'id': structure.get_item_id(), 'sourceKey': 'testSourceKey',
                       'name': 'testName', 'tags': {'testTag': tag}}
        # noinspection PyUnresolvedReferences
        compareStructure = model.core.structure.Structure(compareStructureJson)
        self.assertEqual(structure, compareStructure)
        compareStructureGet = model.core.structure.Structure(git.getStructure('testSourceKey'))
        self.assertEqual(structure, compareStructureGet)

        lineageEdgeId = git.createLineageEdge('testSourceKey', 'testName', {'testTag': tag})
        lineageEdgeJson = {}
        with open(git.path + str(lineageEdgeId) + '.json', 'r') as f:
            lineageEdgeJson = json.loads(f.read())
        lineageEdge = model.usage.lineage_edge.LineageEdge(lineageEdgeJson)
        compareLineageEdgeJson = {'id': lineageEdge.get_id(), 'sourceKey': 'testSourceKey',
                       'name': 'testName', 'tags': {'testTag': tag}}
        # noinspection PyUnresolvedReferences
        compareLineageEdge = model.usage.lineage_edge.LineageEdge(compareLineageEdgeJson)
        self.assertEqual(lineageEdge, compareLineageEdge)
        compareLineageEdgeGet = model.usage.lineage_edge.LineageEdge(git.getLineageEdge('testSourceKey'))
        self.assertEqual(lineageEdge, compareLineageEdgeGet)

        lineageGraphId = git.createLineageGraph('testSourceKey', 'testName', {'testTag': tag})
        lineageGraphJson = {}
        with open(git.path + str(lineageGraphId) + '.json', 'r') as f:
            lineageGraphJson = json.loads(f.read())
        lineageGraph = model.usage.lineage_graph.LineageGraph(lineageGraphJson)
        compareLineageGraphJson = {'id': lineageGraph.get_id(), 'sourceKey': 'testSourceKey',
                       'name': 'testName', 'tags': {'testTag': tag}}
        # noinspection PyUnresolvedReferences
        compareLineageGraph = model.usage.lineage_graph.LineageGraph(compareLineageGraphJson)
        self.assertEqual(lineageGraph, compareLineageGraph)
        compareLineageGraphGet = model.usage.lineage_graph.LineageGraph(git.getLineageGraph('testSourceKey'))
        self.assertEqual(lineageGraph, compareLineageGraphGet)



        params = {"testReference": 9}
        nodeVersionId = git.createNodeVersion(nodeId, "testReference", params, {"testTag": tag}, 1, [2, 3])
        nodeVersionJson = {}
        with open(git.path + str(nodeVersionId) + '.json', 'r') as f:
            nodeVersionJson = json.loads(f.read())
        nodeVersion = model.core.node_version.NodeVersion(nodeVersionJson)
        compareNodeVersionJson = {'id': nodeVersionId, 'nodeId': nodeId, "reference": "testReference",
                       "referenceParameters": params, "tags": {"testTag": tag}, "structureVersionId": 1,
                       "parentIds": [2, 3]}
        compareNodeVersion = model.core.node_version.NodeVersion(compareNodeVersionJson)
        self.assertEqual(nodeVersion, compareNodeVersion)
        edgeVersionId = git.createEdgeVersion(edgeId, 4, 5, 6, 7, "testReference", params,
                                              {"testTag": tag}, 1, [2, 3])
        edgeVersionJson = {}
        with open(git.path + str(edgeVersionId) + '.json', 'r') as f:
            edgeVersionJson = json.loads(f.read())
        edgeVersion = model.core.edge_version.EdgeVersion(edgeVersionJson)
        compareEdgeVersionJson = {'id': edgeVersionId, 'edgeId': edgeId, "toNodeVersionStartId": 4,
                                  "fromNodeVersionStartId": 5,
                       "toNodeVersionEndId": 6, "fromNodeVersionEndId": 7, "reference": "testReference",
                       "referenceParameters": params, "tags": {"testTag": tag}, "structureVersionId": 1,
                       "parentIds": [2, 3]}
        compareEdgeVersion = model.core.edge_version.EdgeVersion(compareEdgeVersionJson)
        self.assertEqual(edgeVersion, compareEdgeVersion)
        graphVersionId = git.createGraphVersion(graphId, [4, 5, 6], "testReference",
                                                params, {"testTag": tag}, 1, [2, 3])
        graphVersionJson = {}
        with open(git.path + str(graphVersionId) + '.json', 'r') as f:
            graphVersionJson = json.loads(f.read())
        graphVersion = model.core.graph_version.GraphVersion(graphVersionJson)
        compareGraphVersionJson = {'id': graphVersionId, 'graphId': graphId, "edgeVersionIds": [4, 5, 6],
                       "reference": "testReference", "referenceParameters": params, "tags": {"testTag": tag},
                       "structureVersionId": 1, "parentIds": [2, 3]}
        compareGraphVersion = model.core.graph_version.GraphVersion(compareGraphVersionJson)
        self.assertEqual(graphVersion, compareGraphVersion)
        structureVersionId = git.createStructureVersion(structureId, {'testKey': 'testValue'}, [2, 3])
        structureVersionJson = {}
        with open(git.path + str(structureVersionId) + '.json', 'r') as f:
            structureVersionJson = json.loads(f.read())
        structureVersion = model.core.structure_version.StructureVersion(structureVersionJson)
        compareStructureVersionJson = {'id': structureVersionId, 'structureId': structureId,
                                       "attributes": {'testKey': 'testValue'},
                       "parentIds": [2, 3]}
        compareStructureVersion = model.core.structure_version.StructureVersion(compareStructureVersionJson)
        self.assertEqual(structureVersion, compareStructureVersion)
        lineageEdgeVersionId = git.createLineageEdgeVersion(lineageEdgeId, 4, 5, "testReference", params,
                                                            {"testTag": tag}, 1, [2, 3])
        lineageEdgeVersionJson = {}
        with open(git.path + str(lineageEdgeVersionId) + '.json', 'r') as f:
            lineageEdgeVersionJson = json.loads(f.read())
        lineageEdgeVersion = model.usage.lineage_edge_version.LineageEdgeVersion(lineageEdgeVersionJson)
        compareLineageEdgeVersionJson = {'id': lineageEdgeVersionId, 'lineageEdgeId': lineageEdgeId,
                                         "toRichVersionId": 4,
                       "fromRichVersionId": 5,
                       "reference": "testReference", "referenceParameters": params, "tags": {"testTag": tag},
                       "structureVersionId": 1, "parentIds": [2, 3]}
        compareLineageEdgeVersion = model.usage.lineage_edge_version.LineageEdgeVersion(compareLineageEdgeVersionJson)
        self.assertEqual(lineageEdgeVersion, compareLineageEdgeVersion)
        lineageGraphVersionId = git.createLineageGraphVersion(lineageGraphId, [4, 5], "testReference", params,
                                                              {"testTag": tag}, 1, [2, 3])
        lineageGraphVersionJson = {}
        with open(git.path + str(lineageGraphVersionId) + '.json', 'r') as f:
            lineageGraphVersionJson = json.loads(f.read())
        lineageGraphVersion = model.usage.lineage_graph_version.LineageGraphVersion(lineageGraphVersionJson)
        compareLineageGraphVersionJson = {'id': lineageGraphVersionId, 'lineageGraphId': lineageGraphId,
                       "lineageEdgeVersionIds": [4, 5],
                       "reference": "testReference", "referenceParameters": params, "tags": {"testTag": tag},
                       "structureVersionId": 1, "parentIds": [2, 3]}
        compareLGV = model.usage.lineage_graph_version.LineageGraphVersion(compareLineageGraphVersionJson)
        self.assertEqual(lineageGraphVersion, compareLGV)

    @unittest.skip
    def test_git_create_edge(self):
        git = ground_git.GitImplementation()
        git.init()
        tag = model.version.tag.Tag({'id': 0, 'key': 'testKey', 'value': 'testValue'})
        edgeId = git.createEdge('testSourceKey', 'testFromNodeId', 'testToNodeId', 'testName', {'testTag': tag})
        edge = git.edges[edgeId]
        compareJson = {'id': edge.get_id(), 'sourceKey': 'testSourceKey', 'fromNodeId': 'testFromNodeId',
                       'toNodeId': 'testToNodeId', 'name': 'testName', 'tags': {'testTag': tag}}
        # noinspection PyUnresolvedReferences
        compareEdge = model.core.edge.Edge(compareJson)
        self.assertEqual(edge, compareEdge)

    @unittest.skip
    def test_git_create_graph(self):
        git = ground_git.GitImplementation()
        git.init()
        tag = model.version.tag.Tag({'id': 0, 'key': 'testKey', 'value': 'testValue'})
        graphId = git.createGraph('testSourceKey', 'testName', {'testTag': tag})
        graph = git.graphs[graphId]
        compareJson = {'id': graph.get_item_id(), 'sourceKey': 'testSourceKey',
                       'name': 'testName', 'tags': {'testTag': tag}}
        # noinspection PyUnresolvedReferences
        compareGraph = model.core.graph.Graph(compareJson)
        self.assertEqual(graph, compareGraph)

    @unittest.skip
    def test_git_create_structure(self):
        git = ground_git.GitImplementation()
        git.init()
        tag = model.version.tag.Tag({'id': 0, 'key': 'testKey', 'value': 'testValue'})
        structureId = git.createStructure('testSourceKey', 'testName', {'testTag': tag})
        structure = git.structures[structureId]
        compareJson = {'id': structure.get_item_id(), 'sourceKey': 'testSourceKey',
                       'name': 'testName', 'tags': {'testTag': tag}}
        # noinspection PyUnresolvedReferences
        compareStructure = model.core.structure.Structure(compareJson)
        self.assertEqual(structure, compareStructure)

    @unittest.skip
    def test_git_create_lineage_edge(self):
        git = ground_git.GitImplementation()
        git.init()
        tag = model.version.tag.Tag({'id': 0, 'key': 'testKey', 'value': 'testValue'})
        lineageEdgeId = git.createLineageEdge('testSourceKey', 'testName', {'testTag': tag})
        lineageEdge = git.lineageEdges[lineageEdgeId]
        compareJson = {'id': lineageEdge.get_id(), 'sourceKey': 'testSourceKey',
                       'name': 'testName', 'tags': {'testTag': tag}}
        # noinspection PyUnresolvedReferences
        compareLineageEdge = model.usage.lineage_edge.LineageEdge(compareJson)
        self.assertEqual(lineageEdge, compareLineageEdge)

    @unittest.skip
    def test_git_create_lineage_graph(self):
        git = ground_git.GitImplementation()
        git.init()
        tag = model.version.tag.Tag({'id': 0, 'key': 'testKey', 'value': 'testValue'})
        lineageGraphId = git.createLineageGraph('testSourceKey', 'testName', {'testTag': tag})
        lineageGraph = git.lineageGraphs[lineageGraphId]
        compareJson = {'id': lineageGraph.get_id(), 'sourceKey': 'testSourceKey',
                       'name': 'testName', 'tags': {'testTag': tag}}
        # noinspection PyUnresolvedReferences
        compareLineageGraph = model.usage.lineage_graph.LineageGraph(compareJson)
        self.assertEqual(lineageGraph, compareLineageGraph)

    @unittest.skip
    def test_git_get_node(self):
        git = ground_git.GitImplementation()
        nodeId = git.createNode('testSourceKey', 'testName', {'testKey': 'testValue'})
        node = git.getNode('testSourceKey')
        self.assertIsNotNone(node.get_source_key(), "node attribute 'sourceKey' is None")
        self.assertEqual(node.get_source_key(), 'testSourceKey', "node attribute 'sourceKey', "
                                                          "Expected: testSourceKey, Actual: " + str(node.get_source_key()))
        self.assertIsNotNone(node.get_name(), "node attribute 'name' is None")
        self.assertEqual(node.get_name(), 'testName', "node attribute 'name', Expected: testName, "
                                                "Actual: " + str(node.get_name()))
        self.assertIsNotNone(node.tags, "node attribute 'tags' is None")
        self.assertEqual(node.tags, {'testKey': 'testValue'},
                         "node attribute 'sourceKey', Expected: "
                         "" + str({'testKey': 'testValue'}) + ", Actual: " + str(node.tags))
        node_json = node.to_json()
        self.assertEqual(node_json, '{"nodeId": 0, "class": "Node", "sourceKey": "testSourceKey", '
                                    '"name": "testName", "tags": {"testKey": "testValue"}}')

    @unittest.skip
    def test_git_get_edge(self):
        git = ground_git.GitImplementation()
        edgeId = git.createEdge('testSourceKey', 0, 1, 'testName', {'testKey': 'testValue'})
        edge = git.getEdge('testSourceKey')
        self.assertIsNotNone(edge.get_source_key(), "edge attribute 'sourceKey' is None")
        self.assertEqual(edge.get_source_key(), 'testSourceKey', "edge attribute 'sourceKey', "
                                                          "Expected: testSourceKey, Actual: " + str(edge.get_source_key()))
        self.assertIsNotNone(edge.get_from_node_id(), "edge attribute 'fromNodeId' is None")
        self.assertEqual(edge.get_from_node_id(), 0, "edge attribute 'fromNodeId', Expected: 0, "
                                             "Actual: " + str(edge.get_from_node_id()))
        self.assertIsNotNone(edge.get_to_node_id(), "edge attribute 'toNodeId' is None")
        self.assertEqual(edge.get_to_node_id(), 1, "edge attribute 'toNodeId', Expected: 1, "
                                           "Actual: " + str(edge.get_to_node_id()))
        self.assertIsNotNone(edge.get_name(), "edge attribute 'name' is None")
        self.assertEqual(edge.get_name(), 'testName', "edge attribute 'name', Expected: testName, "
                                                "Actual: " + str(edge.get_name()))
        self.assertIsNotNone(edge.tags, "edge attribute 'tags' is None")
        self.assertEqual(edge.tags, {'testKey': 'testValue'},
                         "edge attribute 'sourceKey', Expected: "
                         "" + str({'testKey': 'testValue'}) + ", Actual: " + str(edge.tags))
        edge_json = edge.to_json()
        self.assertEqual(edge_json, '{"fromNodeId": 0, "name": "testName", "edgeId": 0, '
                                    '"tags": {"testKey": "testValue"}, "class": "Edge", '
                                    '"toNodeId": 1, "sourceKey": "testSourceKey"}')

    @unittest.skip
    def test_git_get_graph(self):
        git = ground_git.GitImplementation()
        graphId = git.createGraph('testSourceKey', 'testName', {'testKey': 'testValue'})
        graph = git.getGraph('testSourceKey')
        self.assertIsNotNone(graph.get_source_key(), "graph attribute 'sourceKey' is None")
        self.assertEqual(graph.get_source_key(), 'testSourceKey', "graph attribute 'sourceKey', "
                                                           "Expected: testSourceKey, Actual: " + str(graph.get_source_key()))
        self.assertIsNotNone(graph.get_name(), "graph attribute 'name' is None")
        self.assertEqual(graph.get_name(), 'testName', "graph attribute 'name', Expected: testName, "
                                                 "Actual: " + str(graph.get_name()))
        self.assertIsNotNone(graph.tags, "graph attribute 'tags' is None")
        self.assertEqual(graph.tags, {'testKey': 'testValue'},
                         "graph attribute 'sourceKey', Expected: "
                         "" + str({'testKey': 'testValue'}) + ", Actual: " + str(graph.tags))
        self.assertEqual(graph.nodes, {})
        self.assertEqual(graph.nodeVersions, {})
        self.assertEqual(graph.edges, {})
        self.assertEqual(graph.edgeVersions, {})
        self.assertEqual(graph.graphs, {})
        self.assertEqual(graph.graphVersions, {})
        self.assertEqual(graph.structures, {})
        self.assertEqual(graph.structureVersions, {})
        self.assertEqual(graph.lineageEdges, {})
        self.assertEqual(graph.lineageEdgeVersions, {})
        self.assertEqual(graph.lineageGraphs, {})
        self.assertEqual(graph.lineageGraphVersions, {})
        self.assertEqual(graph.ids, set([]))
        for i in range(100):
            testId = graph.gen_id()
            self.assertIn(testId, graph.ids)
            self.assertNotIn(len(graph.ids), graph.ids)
        graph_json = graph.to_json()
        self.assertEqual(graph_json, '{"class": "Graph", "graphId": 0, "sourceKey": "testSourceKey", '
                                     '"name": "testName", "tags": {"testKey": "testValue"}}')

    @unittest.skip
    def test_git_get_structure(self):
        git = ground_git.GitImplementation()
        structureId = git.createStructure('testSourceKey', 'testName', {'testKey': 'testValue'})
        structure = git.getStructure('testSourceKey')
        self.assertIsNotNone(structure.get_source_key(), "structure attribute 'sourceKey' is None")
        self.assertEqual(structure.get_source_key(), 'testSourceKey', "structure attribute 'sourceKey', "
                                                               "Expected: testSourceKey, "
                                                               "Actual: " + str(structure.get_source_key()))
        self.assertIsNotNone(structure.get_name(), "structure attribute 'name' is None")
        self.assertEqual(structure.get_name(), 'testName', "structure attribute 'name', Expected: testName, "
                                                     "Actual: " + str(structure.get_name()))
        self.assertIsNotNone(structure.tags, "structure attribute 'tags' is None")
        self.assertEqual(structure.tags, {'testKey': 'testValue'},
                         "structure attribute 'sourceKey', Expected: "
                         "" + str({'testKey': 'testValue'}) + ", Actual: " + str(structure.tags))
        structure_json = structure.to_json()
        self.assertEqual(structure_json, '{"class": "Structure", "structureId": 0, "sourceKey": "testSourceKey", '
                                         '"name": "testName", "tags": {"testKey": "testValue"}}')

    @unittest.skip
    def test_git_get_lineage_edge(self):
        git = ground_git.GitImplementation()
        lineageEdgeId = git.createLineageEdge('testSourceKey', 'testName', {'testKey': 'testValue'})
        lineage_edge = git.getLineageEdge('testSourceKey')
        self.assertIsNotNone(lineage_edge.get_source_key(), "lineage_edge attribute 'sourceKey' is None")
        self.assertEqual(lineage_edge.get_source_key(), 'testSourceKey', "lineage_edge attribute 'sourceKey', "
                                                                  "Expected: testSourceKey, "
                                                                  "Actual: " + str(lineage_edge.get_source_key()))
        self.assertIsNotNone(lineage_edge.get_name(), "lineage_edge attribute 'name' is None")
        self.assertEqual(lineage_edge.get_name(), 'testName', "lineage_edge attribute 'name', Expected: testName, "
                                                        "Actual: " + str(lineage_edge.get_name()))
        self.assertIsNotNone(lineage_edge.tags, "lineage_edge attribute 'tags' is None")
        self.assertEqual(lineage_edge.tags, {'testKey': 'testValue'},
                         "lineage_edge attribute 'sourceKey', Expected: "
                         "" + str({'testKey': 'testValue'}) + ", Actual: " + str(lineage_edge.tags))
        lineage_edge_json = lineage_edge.to_json()
        self.assertEqual(lineage_edge_json, '{"class": "LineageEdge", "tags": {"testKey": "testValue"}, '
                                            '"sourceKey": "testSourceKey", "lineageEdgeId": 0, "name": "testName"}')

    @unittest.skip
    def test_git_get_lineage_graph(self):
        git = ground_git.GitImplementation()
        lineageGraphId = git.createLineageGraph('testSourceKey', 'testName', {'testKey': 'testValue'})
        lineage_graph = git.getLineageGraph('testSourceKey')
        self.assertIsNotNone(lineage_graph.get_source_key(), "lineage_graph attribute 'sourceKey' is None")
        self.assertEqual(lineage_graph.get_source_key(), 'testSourceKey', "lineage_graph attribute 'sourceKey', "
                                                                   "Expected: testSourceKey, "
                                                                   "Actual: " + str(lineage_graph.get_source_key()))
        self.assertIsNotNone(lineage_graph.get_name(), "lineage_graph attribute 'name' is None")
        self.assertEqual(lineage_graph.get_name(), 'testName', "lineage_graph attribute 'name', Expected: testName, "
                                                         "Actual: " + str(lineage_graph.get_name()))
        self.assertIsNotNone(lineage_graph.tags, "lineage_graph attribute 'tags' is None")
        self.assertEqual(lineage_graph.tags, {'testKey': 'testValue'},
                         "lineage_graph attribute 'sourceKey', Expected: "
                         "" + str({'testKey': 'testValue'}) + ", Actual: " + str(lineage_graph.tags))
        lineage_graph_json = lineage_graph.to_json()
        self.assertEqual(lineage_graph_json, '{"lineageGraphId": 0, "class": "LineageGraph", '
                                             '"tags": {"testKey": "testValue"}, '
                                             '"sourceKey": "testSourceKey", "name": "testName"}')

    @unittest.skip
    def test_git_create_node_version(self):
        git = ground_git.GitImplementation()
        git.init()
        tag = model.version.tag.Tag({'id': 0, 'key': 'testKey', 'value': 'testValue'})
        params = {"testReference": 9}
        nodeId = git.createNode('testSourceKey', 'testName', {'testTag': tag})
        nodeVersionId = git.createNodeVersion(nodeId, "testReference", params, {"testTag": tag}, 1, [2, 3])
        nodeVersion = git.nodeVersions[nodeVersionId]
        compareJson = {'id': nodeVersionId, 'nodeId': nodeId, "reference": "testReference",
                       "referenceParameters": params, "tags": {"testTag": tag}, "structureVersionId": 1,
                       "parentIds": [2, 3]}
        compareNodeVersion = model.core.node_version.NodeVersion(compareJson)
        self.assertEqual(nodeVersion, compareNodeVersion)

    @unittest.skip
    def test_git_create_edge_version(self):
        git = ground_git.GitImplementation()
        git.init()
        tag = model.version.tag.Tag({'id': 0, 'key': 'testKey', 'value': 'testValue'})
        params ={"testReference" : 9}
        edgeId = git.createEdge('testSourceKey', 'testFromNodeId', 'testToNodeId', 'testName', {'testTag': tag})
        edgeVersionId = git.createEdgeVersion(edgeId, 4, 5, 6, 7, "testReference", params,
                                              {"testTag": tag}, 1, [2, 3])
        edgeVersion = git.edgeVersions[edgeVersionId]
        compareJson = {'id': edgeVersionId, 'edgeId': edgeId, "toNodeVersionStartId": 4, "fromNodeVersionStartId": 5,
                       "toNodeVersionEndId": 6, "fromNodeVersionEndId": 7, "reference": "testReference",
                       "referenceParameters": params, "tags": {"testTag": tag}, "structureVersionId": 1,
                       "parentIds": [2, 3]}
        compareEdgeVersion = model.core.edge_version.EdgeVersion(compareJson)
        self.assertEqual(edgeVersion, compareEdgeVersion)

    @unittest.skip
    def test_git_create_graph_version(self):
        git = ground_git.GitImplementation()
        git.init()
        tag = model.version.tag.Tag({'id': 0, 'key': 'testKey', 'value': 'testValue'})
        params = {"testReference": 9}
        graphId = git.createGraph('testSourceKey', 'testName', {'testTag': tag})
        graphVersionId = git.createGraphVersion(graphId, [4, 5, 6], "testReference",
                                                params, {"testTag": tag}, 1, [2, 3])
        graphVersion = git.graphVersions[graphVersionId]
        compareJson = {'id': graphVersionId, 'graphId': graphId, "edgeVersionIds": [4, 5, 6],
                       "reference": "testReference", "referenceParameters": params, "tags": {"testTag": tag},
                       "structureVersionId": 1, "parentIds": [2, 3]}
        compareGraphVersion = model.core.graph_version.GraphVersion(compareJson)
        self.assertEqual(graphVersion, compareGraphVersion)

    @unittest.skip
    def test_git_create_structure_version(self):
        git = ground_git.GitImplementation()
        git.init()
        tag = model.version.tag.Tag({'id': 0, 'key': 'testKey', 'value': 'testValue'})
        structureId = git.createStructure('testSourceKey', 'testName', {'testTag': tag})
        structureVersionId = git.createStructureVersion(structureId, {'testKey': 'testValue'}, [2, 3])
        structureVersion = git.structureVersions[structureVersionId]
        compareJson = {'id': structureVersionId, 'structureId': structureId, "attributes": {'testKey': 'testValue'},
                       "parentIds": [2, 3]}
        compareStructureVersion = model.core.structure_version.StructureVersion(compareJson)
        self.assertEqual(structureVersion, compareStructureVersion)

    @unittest.skip
    def test_git_create_lineage_edge_version(self):
        git = ground_git.GitImplementation()
        git.init()
        tag = model.version.tag.Tag({'id': 0, 'key': 'testKey', 'value': 'testValue'})
        params = {"testReference": 9}
        lineageEdgeId = git.createLineageEdge('testSourceKey', 'testName', {'testTag': tag})
        lineageEdgeVersionId = git.createLineageEdgeVersion(lineageEdgeId, 4, 5, "testReference", params,
                                              {"testTag": tag}, 1, [2, 3])
        lineageEdgeVersion = git.lineageEdgeVersions[lineageEdgeVersionId]
        compareJson = {'id': lineageEdgeVersionId, 'lineageEdgeId': lineageEdgeId, "toRichVersionId": 4,
                       "fromRichVersionId": 5,
                       "reference": "testReference", "referenceParameters": params, "tags": {"testTag": tag},
                       "structureVersionId": 1, "parentIds": [2, 3]}
        compareLineageEdgeVersion = model.usage.lineage_edge_version.LineageEdgeVersion(compareJson)
        self.assertEqual(lineageEdgeVersion, compareLineageEdgeVersion)

    @unittest.skip
    def test_git_create_lineage_graph_version(self):
        git = ground_git.GitImplementation()
        git.init()
        tag = model.version.tag.Tag({'id': 0, 'key': 'testKey', 'value': 'testValue'})
        params = {"testReference": 9}
        lineageGraphId = git.createLineageGraph('testSourceKey', 'testName', {'testTag': tag})
        lineageGraphVersionId = git.createLineageGraphVersion(lineageGraphId, [4, 5], "testReference", params,
                                                            {"testTag": tag}, 1, [2, 3])
        lineageGraphVersion = git.lineageGraphVersions[lineageGraphVersionId]
        compareJson = {'id': lineageGraphVersionId, 'lineageGraphId': lineageGraphId,
                       "lineageEdgeVersionIds": [4, 5],
                       "reference": "testReference", "referenceParameters": params, "tags": {"testTag": tag},
                       "structureVersionId": 1, "parentIds": [2, 3]}
        compareLineageGraphVersion = model.usage.lineage_graph_version.LineageGraphVersion(compareJson)
        self.assertEqual(lineageGraphVersion, compareLineageGraphVersion)

    @unittest.skip
    def test_git_get_node_version(self):
        git = ground_git.GitImplementation()
        nodeId = git.createNode('testSourceKey', 'testName', {'testKey': 'testValue'})
        nodeVersionId = git.createNodeVersion(nodeId, "testReference", "testReferenceParameters",
                                              {'testKey': 'testValue'}, 1, [2, 3])
        node_version = git.getNodeVersion(nodeVersionId)
        self.assertIsNotNone(node_version.get_source_key(), "node_version attribute 'sourceKey' is None")
        self.assertEqual(node_version.get_source_key(), 'testSourceKey', "node_version attribute 'sourceKey', "
                                                                  "Expected: testSourceKey, "
                                                                  "Actual: " + str(node_version.get_source_key()))
        self.assertIsNotNone(node_version.nodeId, "node_version attribute 'nodeId' is None")
        self.assertEqual(node_version.nodeId, 0, "node_version attribute 'nodeId', "
                                                 "Expected: 0, Actual: " + str(node_version.nodeId))
        self.assertIsNotNone(node_version.reference, "node_version attribute 'reference' is None")
        self.assertEqual(node_version.reference, "testReference", "node_version attribute 'reference', "
                                                                  "Expected: testReference, "
                                                                  "Actual: " + str(node_version.reference))
        self.assertIsNotNone(node_version.referenceParameters, "node_version attribute 'referenceParameters' is None")
        self.assertEqual(node_version.referenceParameters, "testReferenceParameters", "node_version attribute "
                                                                                      "'referenceParameters', "
                                                                                      "Expected: testReferenceParameters, "
                                                                                      "Actual: " + str(
            node_version.referenceParameters))
        self.assertIsNotNone(node_version.tags, "node_version attribute 'tags' is None")
        self.assertEqual(node_version.tags,
                         {'testKey': 'testValue'},
                         "node_version attribute 'tags', "
                         "Expected: " + str({'testKey': 'testValue'}) + ", Actual: " + str(node_version.tags))
        self.assertIsNotNone(node_version.structureVersionId, "node_version attribute 'structureVersionId' is None")
        self.assertEqual(node_version.structureVersionId, 1, "node_version attribute 'structureVersionId', "
                                                             "Expected: 1, "
                                                             "Actual: " + str(node_version.structureVersionId))
        self.assertIsNotNone(node_version.parentIds, "node_version attribute 'parentIds' is None")
        self.assertEqual(node_version.parentIds, [2, 3], "node_version attribute 'parentIds', "
                                                         "Expected: [2, 3], "
                                                         "Actual: " + str(node_version.parentIds))
        node_version_json = node_version.to_json()
        self.assertEqual(node_version_json, '{"nodeVersionId": 1, "reference": "testReference", '
                                            '"tags": {"testKey": "testValue"}, '
                                            '"referenceParameters": "testReferenceParameters", "class": "NodeVersion", '
                                            '"parentIds": [2, 3], "structureVersionId": 1, '
                                            '"sourceKey": "testSourceKey", "nodeId": 0}')

    @unittest.skip
    def test_git_get_edge_version(self):
        git = ground_git.GitImplementation()
        edgeId = git.createEdge('testSourceKey', 0, 10, 'testName', {'testKey': 'testValue'})
        edgeVersionId = git.createEdgeVersion(edgeId, 4, 5, 6, 7, "testReference", "testReferenceParameters",
                                              {'testKey': 'testValue'}, 1, [2, 3])
        edge_version = git.getEdgeVersion(edgeVersionId)
        self.assertIsNotNone(edge_version.get_source_key(), "edge_version attribute 'sourceKey' is None")
        self.assertEqual(edge_version.get_source_key(), 'testSourceKey', "edge_version attribute 'sourceKey', "
                                                                  "Expected: testSourceKey, "
                                                                  "Actual: " + str(edge_version.get_source_key()))
        self.assertIsNotNone(edge_version.get_from_node_id(), "edge_version attribute 'fromNodeId' is None")
        self.assertEqual(edge_version.get_from_node_id(), 0, "edge_version attribute 'fromNodeId', "
                                                     "Expected: 0, Actual: " + str(edge_version.get_from_node_id()))
        self.assertIsNotNone(edge_version.get_to_node_id(), "edge_version attribute 'toNodeId' is None")
        self.assertEqual(edge_version.get_to_node_id(), 10, "edge_version attribute 'toNodeId', "
                                                    "Expected: 10, Actual: " + str(edge_version.get_to_node_id()))
        self.assertIsNotNone(edge_version.edgeId, "edge_version attribute 'edgeId' is None")
        self.assertEqual(edge_version.edgeId, 0, "edge_version attribute 'edgeId', "
                                                 "Expected: 0, Actual: " + str(edge_version.edgeId))
        self.assertIsNotNone(edge_version.toNodeVersionStartId, "edge_version attribute 'toNodeVersionStartId' is None")
        self.assertEqual(edge_version.toNodeVersionStartId, 4, "edge_version attribute 'toNodeVersionStartId', "
                                                               "Expected: 4, Actual: " + str(
            edge_version.toNodeVersionStartId))
        self.assertIsNotNone(edge_version.fromNodeVersionStartId, "edge_version attribute 'fromNodeVersionStartId' "
                                                                  "is None")
        self.assertEqual(edge_version.fromNodeVersionStartId, 5, "edge_version attribute 'fromNodeVersionStartId', "
                                                                 "Expected: 5, Actual: " + str(
            edge_version.fromNodeVersionStartId))
        self.assertIsNotNone(edge_version.toNodeVersionEndId, "edge_version attribute 'toNodeVersionEndId' is None")
        self.assertEqual(edge_version.toNodeVersionEndId, 6, "edge_version attribute 'toNodeVersionEndId', "
                                                             "Expected: 6, Actual: " + str(
            edge_version.toNodeVersionEndId))
        self.assertIsNotNone(edge_version.fromNodeVersionEndId, "edge_version attribute 'fromNodeVersionEndId' is None")
        self.assertEqual(edge_version.fromNodeVersionEndId, 7, "edge_version attribute 'fromNodeVersionEndId', "
                                                               "Expected: 7, Actual: " + str(
            edge_version.fromNodeVersionEndId))
        self.assertIsNotNone(edge_version.reference, "edge_version attribute 'reference' is None")
        self.assertEqual(edge_version.reference, "testReference", "edge_version attribute 'reference', "
                                                                  "Expected: testReference, "
                                                                  "Actual: " + str(edge_version.reference))
        self.assertIsNotNone(edge_version.referenceParameters, "edge_version attribute 'referenceParameters' is None")
        self.assertEqual(edge_version.referenceParameters, "testReferenceParameters", "edge_version attribute "
                                                                                      "'referenceParameters', "
                                                                                      "Expected: testReferenceParameters, "
                                                                                      "Actual: " + str(
            edge_version.referenceParameters))
        self.assertIsNotNone(edge_version.tags, "edge_version attribute 'tags' is None")
        self.assertEqual(edge_version.tags,
                         {'testKey': 'testValue'},
                         "edge_version attribute 'tags', "
                         "Expected: " + str({'testKey': 'testValue'}) + ", Actual: " + str(edge_version.tags))
        self.assertIsNotNone(edge_version.structureVersionId, "edge_version attribute 'structureVersionId' is None")
        self.assertEqual(edge_version.structureVersionId, 1, "edge_version attribute 'structureVersionId', "
                                                             "Expected: 1, "
                                                             "Actual: " + str(edge_version.structureVersionId))
        self.assertIsNotNone(edge_version.parentIds, "edge_version attribute 'parentIds' is None")
        self.assertEqual(edge_version.parentIds, [2, 3], "edge_version attribute 'parentIds', "
                                                         "Expected: [2, 3], "
                                                         "Actual: " + str(edge_version.parentIds))
        edge_version_json = edge_version.to_json()
        self.assertEqual(edge_version_json, '{"toNodeVersionStartId": 4, "toNodeVersionEndId": 6, '
                                            '"reference": "testReference", "tags": {"testKey": "testValue"}, '
                                            '"edgeVersionId": 1, "referenceParameters": "testReferenceParameters", '
                                            '"class": "EdgeVersion", "fromNodeId": 0, "edgeId": 0, '
                                            '"parentIds": [2, 3], "structureVersionId": 1, '
                                            '"fromNodeVersionStartId": 5, "toNodeId": 10, '
                                            '"fromNodeVersionEndId": 7, "sourceKey": "testSourceKey"}')

    @unittest.skip
    def test_git_get_graph_version(self):
        git = ground_git.GitImplementation()
        graphId = git.createGraph('testSourceKey', 'testName', {'testKey': 'testValue'})
        graphVersionId = git.createGraphVersion(graphId, [4, 5, 6], "testReference", "testReferenceParameters",
                                                {'testKey': 'testValue'}, 1, [2, 3])
        graph_version = git.getGraphVersion(graphVersionId)
        self.assertIsNotNone(graph_version.get_source_key(), "graph_version attribute 'sourceKey' is None")
        self.assertEqual(graph_version.get_source_key(), 'testSourceKey', "graph_version attribute 'sourceKey', "
                                                                   "Expected: testSourceKey, "
                                                                   "Actual: " + str(graph_version.get_source_key()))
        self.assertIsNotNone(graph_version.graphId, "graph_version attribute 'graphId' is None")
        self.assertEqual(graph_version.graphId, 0, "graph_version attribute 'graphId', "
                                                   "Expected: 0, Actual: " + str(graph_version.graphId))
        self.assertIsNotNone(graph_version.edgeVersionIds, "graph_version attribute 'edgeVersionIds' is None")
        self.assertEqual(graph_version.edgeVersionIds, [4, 5, 6], "graph_version attribute 'edgeVersionIds', "
                                                                  "Expected: [4, 5, 6], "
                                                                  "Actual: " + str(graph_version.edgeVersionIds))
        self.assertIsNotNone(graph_version.reference, "graph_version attribute 'reference' is None")
        self.assertEqual(graph_version.reference, "testReference", "graph_version attribute 'reference', "
                                                                   "Expected: testReference, "
                                                                   "Actual: " + str(graph_version.reference))
        self.assertIsNotNone(graph_version.referenceParameters, "graph_version attribute 'referenceParameters' is None")
        self.assertEqual(graph_version.referenceParameters, "testReferenceParameters", "graph_version attribute "
                                                                                       "'referenceParameters', "
                                                                                       "Expected: testReferenceParameters, "
                                                                                       "Actual: " + str(
            graph_version.referenceParameters))
        self.assertIsNotNone(graph_version.tags, "graph_version attribute 'tags' is None")
        self.assertEqual(graph_version.tags,
                         {'testKey': 'testValue'},
                         "graph_version attribute 'tags', "
                         "Expected: " + str({'testKey': 'testValue'}) + ", Actual: " + str(graph_version.tags))
        self.assertIsNotNone(graph_version.structureVersionId, "graph_version attribute 'structureVersionId' is None")
        self.assertEqual(graph_version.structureVersionId, 1, "graph_version attribute 'structureVersionId', "
                                                              "Expected: 1, "
                                                              "Actual: " + str(graph_version.structureVersionId))
        self.assertIsNotNone(graph_version.parentIds, "graph_version attribute 'parentIds' is None")
        self.assertEqual(graph_version.parentIds, [2, 3], "graph_version attribute 'parentIds', "
                                                          "Expected: [2, 3], "
                                                          "Actual: " + str(graph_version.parentIds))
        graph_version_json = graph_version.to_json()
        self.assertEqual(graph_version_json, '{"parentIds": [2, 3], "graphId": 0, "reference": "testReference", '
                                             '"edgeVersionIds": [4, 5, 6], '
                                             '"referenceParameters": "testReferenceParameters", '
                                             '"graphVersionId": 1, "tags": {"testKey": "testValue"}, '
                                             '"structureVersionId": 1, "sourceKey": "testSourceKey", '
                                             '"class": "GraphVersion"}')

    @unittest.skip
    def test_git_get_structure_version(self):
        git = ground_git.GitImplementation()
        structureId = git.createStructure('testSourceKey', 'testName', {'testKey': 'testValue'})
        structureVersionId = git.createStructureVersion(structureId, {'testKey': 'testValue'}, [2, 3])
        structure_version = git.getStructureVersion(structureVersionId)
        self.assertIsNotNone(structure_version.get_source_key(), "structure_version attribute 'sourceKey' is None")
        self.assertEqual(structure_version.get_source_key(), 'testSourceKey', "structure_version attribute 'sourceKey', "
                                                                       "Expected: testSourceKey, "
                                                                       "Actual: " + str(structure_version.get_source_key()))
        self.assertIsNotNone(structure_version.structureId, "structure_version attribute 'structureId' is None")
        self.assertEqual(structure_version.structureId, 0, "structure_version attribute 'structureId', "
                                                           "Expected: 0, Actual: " + str(structure_version.structureId))
        self.assertIsNotNone(structure_version.attributes, "structure_version attribute 'attributes' is None")
        self.assertEqual(structure_version.attributes, {'testKey': 'testValue'}, "structure_version "
                                                                                 "attribute 'attributes', "
                                                                                 "Expected: , " + str(
            {'testKey': 'testValue'}) +
                         ", Actual: " + str(structure_version.attributes))
        self.assertIsNotNone(structure_version.parentIds, "structure_version attribute 'parentIds' is None")
        self.assertEqual(structure_version.parentIds, [2, 3], "structure_version attribute 'parentIds', "
                                                              "Expected: [2, 3], "
                                                              "Actual: " + str(structure_version.parentIds))
        structure_version_json = structure_version.to_json()
        self.assertEqual(structure_version_json, '{"parentIds": [2, 3], "structureId": 0, "structureVersionId": 1, '
                                                 '"sourceKey": "testSourceKey", '
                                                 '"attributes": {"testKey": "testValue"}, '
                                                 '"class": "StructureVersion"}')

    @unittest.skip
    def test_git_get_lineage_edge_version(self):
        git = ground_git.GitImplementation()
        lineageEdgeId = git.createLineageEdge('testSourceKey', 'testName', {'testKey': 'testValue'})
        lineageEdgeVersionId = git.createLineageEdgeVersion(lineageEdgeId, 5, 4, "testReference",
                                                            "testReferenceParameters",
                                                            {'testKey': 'testValue'}, 1, [2, 3])
        lineage_edge_version = git.getLineageEdgeVersion(lineageEdgeVersionId)
        self.assertIsNotNone(lineage_edge_version.get_source_key(), "lineage_edge_version attribute 'sourceKey' is None")
        self.assertEqual(lineage_edge_version.get_source_key(), 'testSourceKey', "lineage_edge_version attribute 'sourceKey', "
                                                                          "Expected: testSourceKey, "
                                                                          "Actual: " + str(
            lineage_edge_version.get_source_key()))
        self.assertIsNotNone(lineage_edge_version.lineageEdgeId, "lineage_edge_version attribute "
                                                                 "'lineageEdgeId' is None")
        self.assertEqual(lineage_edge_version.lineageEdgeId, 0, "lineage_edge_version attribute 'lineageEdgeId', "
                                                                "Expected: 0, Actual: " + str(
            lineage_edge_version.lineageEdgeId))
        self.assertIsNotNone(lineage_edge_version.fromRichVersionId, "lineage_edge_version attribute "
                                                                     "'fromRichVersionId' is None")
        self.assertEqual(lineage_edge_version.fromRichVersionId, 4,
                         "lineage_edge_version attribute 'fromRichVersionId', "
                         "Expected: 4, Actual: " + str(lineage_edge_version.fromRichVersionId))
        self.assertIsNotNone(lineage_edge_version.toRichVersionId, "lineage_edge_version attribute "
                                                                   "'toRichVersionId' is None")
        self.assertEqual(lineage_edge_version.toRichVersionId, 5, "lineage_edge_version attribute 'toRichVersionId', "
                                                                  "Expected: 5, Actual: " + str(
            lineage_edge_version.toRichVersionId))
        self.assertIsNotNone(lineage_edge_version.reference, "lineage_edge_version attribute 'reference' is None")
        self.assertEqual(lineage_edge_version.reference, "testReference", "lineage_edge_version attribute 'reference', "
                                                                          "Expected: testReference, "
                                                                          "Actual: " + str(
            lineage_edge_version.reference))
        self.assertIsNotNone(lineage_edge_version.referenceParameters, "lineage_edge_version attribute "
                                                                       "'referenceParameters' is None")
        self.assertEqual(lineage_edge_version.referenceParameters, "testReferenceParameters",
                         "lineage_edge_version "
                         "attribute "
                         "'referenceParameters', "
                         "Expected: testReferenceParameters, "
                         "Actual: " + str(lineage_edge_version.referenceParameters))
        self.assertIsNotNone(lineage_edge_version.tags, "lineage_edge_version attribute 'tags' is None")
        self.assertEqual(lineage_edge_version.tags,
                         {'testKey': 'testValue'},
                         "lineage_edge_version attribute 'tags', "
                         "Expected: " + str({'testKey': 'testValue'}) + ", Actual: " + str(lineage_edge_version.tags))
        self.assertIsNotNone(lineage_edge_version.structureVersionId,
                             "lineage_edge_version attribute 'structureVersionId' is None")
        self.assertEqual(lineage_edge_version.structureVersionId, 1,
                         "lineage_edge_version attribute 'structureVersionId', "
                         "Expected: 1, "
                         "Actual: " + str(lineage_edge_version.structureVersionId))
        self.assertIsNotNone(lineage_edge_version.parentIds, "lineage_edge_version attribute 'parentIds' is None")
        self.assertEqual(lineage_edge_version.parentIds, [2, 3], "lineage_edge_version attribute 'parentIds', "
                                                                 "Expected: [2, 3], "
                                                                 "Actual: " + str(lineage_edge_version.parentIds))
        lineage_edge_version_json = lineage_edge_version.to_json()
        self.assertEqual(lineage_edge_version_json, '{"reference": "testReference", "tags": {"testKey": "testValue"}, '
                                                    '"lineageEdgeVersionId": 1, '
                                                    '"referenceParameters": "testReferenceParameters", '
                                                    '"fromRichVersionId": 4, "class": "LineageEdgeVersion", '
                                                    '"parentIds": [2, 3], "structureVersionId": 1, '
                                                    '"toRichVersionId": 5, "lineageEdgeId": 0, '
                                                    '"sourceKey": "testSourceKey"}')

    @unittest.skip
    def test_git_get_lineage_graph_version(self):
        git = ground_git.GitImplementation()
        lineageGraphId = git.createLineageGraph('testSourceKey', 'testName', {'testKey': 'testValue'})
        lineageGraphVersionId = git.createLineageGraphVersion(lineageGraphId, [5, 4], "testReference",
                                                              "testReferenceParameters",
                                                              {'testKey': 'testValue'}, 1, [2, 3])
        lineage_graph_version = git.getLineageGraphVersion(lineageGraphVersionId)
        self.assertIsNotNone(lineage_graph_version.get_source_key(), "lineage_graph_version attribute 'sourceKey' is None")
        self.assertEqual(lineage_graph_version.get_source_key(), 'testSourceKey',
                         "lineage_graph_version attribute 'sourceKey', "
                         "Expected: testSourceKey, "
                         "Actual: " + str(
                             lineage_graph_version.get_source_key()))
        self.assertIsNotNone(lineage_graph_version.lineageGraphId, "lineage_graph_version attribute "
                                                                   "'lineageGraphId' is None")
        self.assertEqual(lineage_graph_version.lineageGraphId, 0, "lineage_graph_version attribute 'lineageGraphId', "
                                                                  "Expected: 0, Actual: " + str(
            lineage_graph_version.lineageGraphId))
        self.assertIsNotNone(lineage_graph_version.lineageEdgeVersionIds, "lineage_graph_version attribute "
                                                                          "'lineageEdgeVersionIds' is None")
        self.assertEqual(lineage_graph_version.lineageEdgeVersionIds, [5, 4],
                         "lineage_graph_version attribute 'lineageEdgeVersionIds', "
                         "Expected: [5, 4], Actual: " + str(lineage_graph_version.lineageEdgeVersionIds))
        self.assertIsNotNone(lineage_graph_version.reference, "lineage_graph_version attribute 'reference' is None")
        self.assertEqual(lineage_graph_version.reference, "testReference",
                         "lineage_graph_version attribute 'reference', "
                         "Expected: testReference, "
                         "Actual: " + str(
                             lineage_graph_version.reference))
        self.assertIsNotNone(lineage_graph_version.referenceParameters, "lineage_graph_version attribute "
                                                                        "'referenceParameters' is None")
        self.assertEqual(lineage_graph_version.referenceParameters, "testReferenceParameters",
                         "lineage_graph_version "
                         "attribute "
                         "'referenceParameters', "
                         "Expected: testReferenceParameters, "
                         "Actual: " + str(lineage_graph_version.referenceParameters))
        self.assertIsNotNone(lineage_graph_version.tags, "lineage_graph_version attribute 'tags' is None")
        self.assertEqual(lineage_graph_version.tags,
                         {'testKey': 'testValue'},
                         "lineage_graph_version attribute 'tags', "
                         "Expected: " + str({'testKey': 'testValue'}) + ", Actual: " + str(lineage_graph_version.tags))
        self.assertIsNotNone(lineage_graph_version.structureVersionId,
                             "lineage_graph_version attribute 'structureVersionId' is None")
        self.assertEqual(lineage_graph_version.structureVersionId, 1,
                         "lineage_graph_version attribute 'structureVersionId', "
                         "Expected: 1, "
                         "Actual: " + str(lineage_graph_version.structureVersionId))
        self.assertIsNotNone(lineage_graph_version.parentIds, "lineage_graph_version attribute 'parentIds' is None")
        self.assertEqual(lineage_graph_version.parentIds, [2, 3], "lineage_graph_version attribute 'parentIds', "
                                                                  "Expected: [2, 3], "
                                                                  "Actual: " + str(lineage_graph_version.parentIds))
        lineage_graph_version_json = lineage_graph_version.to_json()
        self.assertEqual(lineage_graph_version_json, '{"lineageGraphId": 0, "lineageGraphVersionId": 1, '
                                                     '"parentIds": [2, 3], "reference": "testReference", '
                                                     '"tags": {"testKey": "testValue"}, '
                                                     '"referenceParameters": "testReferenceParameters", '
                                                     '"lineageEdgeVersionIds": [5, 4], '
                                                     '"structureVersionId": 1, "sourceKey": "testSourceKey", '
                                                     '"class": "LineageGraphVersion"}')

    @unittest.skip
    def test_git_get_node_latest_version(self):
        git = ground_git.GitImplementation()
        nodeId = git.createNode('testSourceKey')
        nodeVersionIdOne = git.createNodeVersion(nodeId, "testReference", "testReferenceParameters",
                                                 {'testKeyOne': 'testValueOne'}, 1)
        nodeVersionIdTwo = git.createNodeVersion(nodeId, "testReference", "testReferenceParameters",
                                                 {'testKeyTwo': 'testValueTwo'}, 1, [nodeVersionIdOne])
        nodeVersionIdThree = git.createNodeVersion(nodeId, "testReference", "testReferenceParameters",
                                                   {'testKeyThree': 'testValueThree'}, 1,
                                                   [nodeVersionIdOne, nodeVersionIdTwo])
        nodeVersionIdFour = git.createNodeVersion(nodeId, "testReference", "testReferenceParameters",
                                                  {'testKeyFour': 'testValueFour'}, 1, [nodeVersionIdTwo])
        nodeVersionIdFive = git.createNodeVersion(nodeId, "testReference", "testReferenceParameters",
                                                  {'testKeyFive': 'testValueFive'}, 1, [nodeVersionIdThree])
        nodeVersionIdSix = git.createNodeVersion(nodeId, "testReference", "testReferenceParameters",
                                                 {'testKeySix': 'testValueSix'}, 1,
                                                 [nodeVersionIdTwo, nodeVersionIdThree])
        nodeLastestIds = [nv.nodeVersionId for nv in git.getNodeLatestVersions('testSourceKey')]
        self.assertNotIn(nodeId, nodeLastestIds)
        self.assertNotIn(nodeVersionIdOne, nodeLastestIds)
        self.assertNotIn(nodeVersionIdTwo, nodeLastestIds)
        self.assertNotIn(nodeVersionIdThree, nodeLastestIds)
        self.assertIn(nodeVersionIdFour, nodeLastestIds)
        self.assertIn(nodeVersionIdFive, nodeLastestIds)
        self.assertIn(nodeVersionIdSix, nodeLastestIds)

    def test_git_get_edge_latest_version(self):
        git = ground_git.GitImplementation()
        git.init()
        tag = model.version.tag.Tag({'id': 0, 'key': 'testKey', 'value': 'testValue'})
        edgeId = git.createEdge('test_git_get_edge_latest_version', 0, 10)
        edgeVersionIdOne = git.createEdgeVersion(edgeId, 4, 5, 6, 7, "testReference", "testReferenceParameters",
                                                 {'testTag': tag}, 1)
        edgeVersionIdTwo = git.createEdgeVersion(edgeId, 4, 5, 6, 7, "testReference", "testReferenceParameters",
                                                 {'testTag': tag}, 1, [edgeVersionIdOne])
        edgeVersionIdThree = git.createEdgeVersion(edgeId, 4, 5, 6, 7, "testReference", "testReferenceParameters",
                                                   {'testTag': tag}, 1, [edgeVersionIdOne, edgeVersionIdTwo])
        edgeVersionIdFour = git.createEdgeVersion(edgeId, 4, 5, 6, 7, "testReference", "testReferenceParameters",
                                                  {'testTag': tag}, 1, [edgeVersionIdTwo])
        edgeVersionIdFive = git.createEdgeVersion(edgeId, 4, 5, 6, 7, "testReference", "testReferenceParameters",
                                                  {'testTag': tag}, 1, [edgeVersionIdThree])
        edgeVersionIdSix = git.createEdgeVersion(edgeId, 4, 5, 6, 7, "testReference", "testReferenceParameters",
                                                 {'testTag': tag}, 1, [edgeVersionIdTwo, edgeVersionIdThree])
        edgeLastestIds = [nv['id'] for nv in git.getEdgeLatestVersions('test_git_get_edge_latest_version')]
        self.assertNotIn(edgeId, edgeLastestIds)
        self.assertNotIn(edgeVersionIdOne, edgeLastestIds)
        self.assertNotIn(edgeVersionIdTwo, edgeLastestIds)
        self.assertNotIn(edgeVersionIdThree, edgeLastestIds)
        self.assertIn(edgeVersionIdFour, edgeLastestIds)
        self.assertIn(edgeVersionIdFive, edgeLastestIds)
        self.assertIn(edgeVersionIdSix, edgeLastestIds)

    @unittest.skip
    def test_git_get_graph_latest_version(self):
        git = ground_git.GitImplementation()
        graphId = git.createGraph('testSourceKey')
        graphVersionIdOne = git.createGraphVersion(graphId, [4, 5, 6], "testReference", "testReferenceParameters",
                                                   {'testKey': 'testValue'}, 1)
        graphVersionIdTwo = git.createGraphVersion(graphId, [4, 5, 6], "testReference", "testReferenceParameters",
                                                   {'testKey': 'testValue'}, 1, [graphVersionIdOne])
        graphVersionIdThree = git.createGraphVersion(graphId, [4, 5, 6], "testReference", "testReferenceParameters",
                                                     {'testKey': 'testValue'}, 1,
                                                     [graphVersionIdOne, graphVersionIdTwo])
        graphVersionIdFour = git.createGraphVersion(graphId, [4, 5, 6], "testReference", "testReferenceParameters",
                                                    {'testKey': 'testValue'}, 1, [graphVersionIdTwo])
        graphVersionIdFive = git.createGraphVersion(graphId, [4, 5, 6], "testReference", "testReferenceParameters",
                                                    {'testKey': 'testValue'}, 1, [graphVersionIdThree])
        graphVersionIdSix = git.createGraphVersion(graphId, [4, 5, 6], "testReference", "testReferenceParameters",
                                                   {'testKey': 'testValue'}, 1,
                                                   [graphVersionIdTwo, graphVersionIdThree])
        graphLastestIds = [nv.graphVersionId for nv in git.getGraphLatestVersions('testSourceKey')]
        self.assertNotIn(0, graphLastestIds)
        self.assertNotIn(1, graphLastestIds)
        self.assertNotIn(2, graphLastestIds)
        self.assertNotIn(3, graphLastestIds)
        self.assertIn(4, graphLastestIds)
        self.assertIn(5, graphLastestIds)
        self.assertIn(6, graphLastestIds)

    @unittest.skip
    def test_git_get_structure_latest_version(self):
        git = ground_git.GitImplementation()
        structureId = git.createStructure('testSourceKey')
        structureVersionIdOne = git.createStructureVersion(structureId, {'testKey': 'testValue'})
        structureVersionIdTwo = git.createStructureVersion(structureId, {'testKey': 'testValue'},
                                                           [structureVersionIdOne])
        structureVersionIdThree = git.createStructureVersion(structureId, {'testKey': 'testValue'},
                                                             [structureVersionIdOne, structureVersionIdTwo])
        structureVersionIdFour = git.createStructureVersion(structureId, {'testKey': 'testValue'},
                                                            [structureVersionIdTwo])
        structureVersionIdFive = git.createStructureVersion(structureId, {'testKey': 'testValue'},
                                                            [structureVersionIdThree])
        structureVersionIdSix = git.createStructureVersion(structureId, {'testKey': 'testValue'},
                                                           [structureVersionIdTwo, structureVersionIdThree])
        structureLastestIds = [nv.structureVersionId for nv in git.getStructureLatestVersions('testSourceKey')]
        self.assertNotIn(0, structureLastestIds)
        self.assertNotIn(1, structureLastestIds)
        self.assertNotIn(2, structureLastestIds)
        self.assertNotIn(3, structureLastestIds)
        self.assertIn(4, structureLastestIds)
        self.assertIn(5, structureLastestIds)
        self.assertIn(6, structureLastestIds)

    @unittest.skip
    def test_git_get_lineage_edge_latest_version(self):
        git = ground_git.GitImplementation()
        lineageEdgeId = git.createLineageEdge('testSourceKey')
        lineageEdgeVersionIdOne = git.createLineageEdgeVersion(lineageEdgeId, 5, 4, "testReference",
                                                               "testReferenceParameters",
                                                               {'testKey': 'testValue'}, 1)
        lineageEdgeVersionIdTwo = git.createLineageEdgeVersion(lineageEdgeId, 5, 4, "testReference",
                                                               "testReferenceParameters",
                                                               {'testKey': 'testValue'}, 1,
                                                               [lineageEdgeVersionIdOne])
        lineageEdgeVersionIdThree = git.createLineageEdgeVersion(lineageEdgeId, 5, 4, "testReference",
                                                                 "testReferenceParameters",
                                                                 {'testKey': 'testValue'}, 1,
                                                                 [lineageEdgeVersionIdOne, lineageEdgeVersionIdTwo])
        lineageEdgeVersionIdFour = git.createLineageEdgeVersion(lineageEdgeId, 5, 4, "testReference",
                                                                "testReferenceParameters",
                                                                {'testKey': 'testValue'}, 1,
                                                                [lineageEdgeVersionIdTwo])
        lineageEdgeVersionIdFive = git.createLineageEdgeVersion(lineageEdgeId, 5, 4, "testReference",
                                                                "testReferenceParameters",
                                                                {'testKey': 'testValue'}, 1,
                                                                [lineageEdgeVersionIdThree])
        lineageEdgeVersionIdSix = git.createLineageEdgeVersion(lineageEdgeId, 5, 4, "testReference",
                                                               "testReferenceParameters",
                                                               {'testKey': 'testValue'}, 1,
                                                               [lineageEdgeVersionIdTwo, lineageEdgeVersionIdThree])
        lineageEdgeLastestIds = [nv.lineageEdgeVersionId for nv in git.getLineageEdgeLatestVersions('testSourceKey')]
        self.assertNotIn(0, lineageEdgeLastestIds)
        self.assertNotIn(1, lineageEdgeLastestIds)
        self.assertNotIn(2, lineageEdgeLastestIds)
        self.assertNotIn(3, lineageEdgeLastestIds)
        self.assertIn(4, lineageEdgeLastestIds)
        self.assertIn(5, lineageEdgeLastestIds)
        self.assertIn(6, lineageEdgeLastestIds)

    @unittest.skip
    def test_git_get_lineage_graph_latest_version(self):
        git = ground_git.GitImplementation()
        lineageGraphId = git.createLineageGraph('testSourceKey')
        lineageGraphVersionIdOne = git.createLineageGraphVersion(lineageGraphId, [5, 4], "testReference",
                                                                 "testReferenceParameters",
                                                                 {'testKey': 'testValue'}, 1)
        lineageGraphVersionIdTwo = git.createLineageGraphVersion(lineageGraphId, [5, 4], "testReference",
                                                                 "testReferenceParameters",
                                                                 {'testKey': 'testValue'}, 1,
                                                                 [lineageGraphVersionIdOne])
        lineageGraphVersionIdThree = git.createLineageGraphVersion(lineageGraphId, [5, 4], "testReference",
                                                                   "testReferenceParameters",
                                                                   {'testKey': 'testValue'}, 1,
                                                                   [lineageGraphVersionIdOne, lineageGraphVersionIdTwo])
        lineageGraphVersionIdFour = git.createLineageGraphVersion(lineageGraphId, [5, 4], "testReference",
                                                                  "testReferenceParameters",
                                                                  {'testKey': 'testValue'}, 1,
                                                                  [lineageGraphVersionIdTwo])
        lineageGraphVersionIdFive = git.createLineageGraphVersion(lineageGraphId, [5, 4], "testReference",
                                                                  "testReferenceParameters",
                                                                  {'testKey': 'testValue'}, 1,
                                                                  [lineageGraphVersionIdThree])
        lineageGraphVersionIdSix = git.createLineageGraphVersion(lineageGraphId, [5, 4], "testReference",
                                                                 "testReferenceParameters",
                                                                 {'testKey': 'testValue'}, 1,
                                                                 [lineageGraphVersionIdTwo, lineageGraphVersionIdThree])
        lineageGraphLastestIds = [nv.lineageGraphVersionId for nv in git.getLineageGraphLatestVersions('testSourceKey')]
        self.assertNotIn(0, lineageGraphLastestIds)
        self.assertNotIn(1, lineageGraphLastestIds)
        self.assertNotIn(2, lineageGraphLastestIds)
        self.assertNotIn(3, lineageGraphLastestIds)
        self.assertIn(4, lineageGraphLastestIds)
        self.assertIn(5, lineageGraphLastestIds)
        self.assertIn(6, lineageGraphLastestIds)

    @unittest.skip
    def test_git_get_node_history(self):
        git = ground_git.GitImplementation()
        nodeId = git.createNode('testSourceKey')
        nodeVersionIdOne = git.createNodeVersion(nodeId, "testReference", "testReferenceParameters",
                                                 {'testKeyOne': 'testValueOne'}, 1)
        nodeVersionIdTwo = git.createNodeVersion(nodeId, "testReference", "testReferenceParameters",
                                                 {'testKeyTwo': 'testValueTwo'}, 1, [nodeVersionIdOne])
        nodeVersionIdThree = git.createNodeVersion(nodeId, "testReference", "testReferenceParameters",
                                                   {'testKeyThree': 'testValueThree'}, 1,
                                                   [nodeVersionIdOne, nodeVersionIdTwo])
        nodeVersionIdFour = git.createNodeVersion(nodeId, "testReference", "testReferenceParameters",
                                                  {'testKeyFour': 'testValueFour'}, 1, [nodeVersionIdTwo])
        nodeVersionIdFive = git.createNodeVersion(nodeId, "testReference", "testReferenceParameters",
                                                  {'testKeyFive': 'testValueFive'}, 1, [nodeVersionIdThree])
        nodeVersionIdSix = git.createNodeVersion(nodeId, "testReference", "testReferenceParameters",
                                                 {'testKeySix': 'testValueSix'}, 1,
                                                 [nodeVersionIdThree])
        self.assertEqual(git.getNodeHistory('testSourceKey'), {'0': 1, '1': 3, '3': 6, '2': 4})


    def test_git_get_edge_history(self):
        git = ground_git.GitImplementation()
        git.init()
        tag = model.version.tag.Tag({'id': 0, 'key': 'testKey', 'value': 'testValue'})
        edgeId = git.createEdge('test_git_get_edge_history', 0, 10)
        edgeVersionIdOne = git.createEdgeVersion(edgeId, 4, 5, 6, 7, "testReference", "testReferenceParameters",
                                                 {'testTag': tag}, 1)
        edgeVersionIdTwo = git.createEdgeVersion(edgeId, 4, 5, 6, 7, "testReference", "testReferenceParameters",
                                                 {'testTag': tag}, 1, [edgeVersionIdOne])
        edgeVersionIdThree = git.createEdgeVersion(edgeId, 4, 5, 6, 7, "testReference", "testReferenceParameters",
                                                   {'testTag': tag}, 1, [edgeVersionIdOne, edgeVersionIdTwo])
        edgeVersionIdFour = git.createEdgeVersion(edgeId, 4, 5, 6, 7, "testReference", "testReferenceParameters",
                                                  {'testTag': tag}, 1, [edgeVersionIdTwo])
        edgeVersionIdFive = git.createEdgeVersion(edgeId, 4, 5, 6, 7, "testReference", "testReferenceParameters",
                                                  {'testTag': tag}, 1, [edgeVersionIdThree])
        edgeVersionIdSix = git.createEdgeVersion(edgeId, 4, 5, 6, 7, "testReference", "testReferenceParameters",
                                                 {'testTag': tag}, 1, [edgeVersionIdThree])
        self.assertEqual(git.getEdgeHistory('test_git_get_edge_history'),
                         {str(edgeId): edgeVersionIdOne, str(edgeVersionIdOne): edgeVersionIdThree,
                          str(edgeVersionIdThree): edgeVersionIdSix, str(edgeVersionIdTwo): edgeVersionIdFour})

    @unittest.skip
    def test_git_get_graph_history(self):
        git = ground_git.GitImplementation()
        graphId = git.createGraph('testSourceKey')
        graphVersionIdOne = git.createGraphVersion(graphId, [4, 5, 6], "testReference", "testReferenceParameters",
                                                   {'testKey': 'testValue'}, 1)
        graphVersionIdTwo = git.createGraphVersion(graphId, [4, 5, 6], "testReference", "testReferenceParameters",
                                                   {'testKey': 'testValue'}, 1, [graphVersionIdOne])
        graphVersionIdThree = git.createGraphVersion(graphId, [4, 5, 6], "testReference", "testReferenceParameters",
                                                     {'testKey': 'testValue'}, 1,
                                                     [graphVersionIdOne, graphVersionIdTwo])
        graphVersionIdFour = git.createGraphVersion(graphId, [4, 5, 6], "testReference", "testReferenceParameters",
                                                    {'testKey': 'testValue'}, 1, [graphVersionIdTwo])
        graphVersionIdFive = git.createGraphVersion(graphId, [4, 5, 6], "testReference", "testReferenceParameters",
                                                    {'testKey': 'testValue'}, 1, [graphVersionIdThree])
        graphVersionIdSix = git.createGraphVersion(graphId, [4, 5, 6], "testReference", "testReferenceParameters",
                                                   {'testKey': 'testValue'}, 1,
                                                   [graphVersionIdThree])
        self.assertEqual(git.getGraphHistory('testSourceKey'), {'0': 1, '1': 3, '3': 6, '2': 4})

    @unittest.skip
    def test_git_get_structure_history(self):
        git = ground_git.GitImplementation()
        structureId = git.createStructure('testSourceKey')
        structureVersionIdOne = git.createStructureVersion(structureId, {'testKey': 'testValue'})
        structureVersionIdTwo = git.createStructureVersion(structureId, {'testKey': 'testValue'},
                                                           [structureVersionIdOne])
        structureVersionIdThree = git.createStructureVersion(structureId, {'testKey': 'testValue'},
                                                             [structureVersionIdOne, structureVersionIdTwo])
        structureVersionIdFour = git.createStructureVersion(structureId, {'testKey': 'testValue'},
                                                            [structureVersionIdTwo])
        structureVersionIdFive = git.createStructureVersion(structureId, {'testKey': 'testValue'},
                                                            [structureVersionIdThree])
        structureVersionIdSix = git.createStructureVersion(structureId, {'testKey': 'testValue'},
                                                           [structureVersionIdThree])
        self.assertEqual(git.getStructureHistory('testSourceKey'), {'0': 1, '1': 3, '3': 6, '2': 4})

    @unittest.skip
    def test_git_get_lineage_edge_history(self):
        git = ground_git.GitImplementation()
        lineageEdgeId = git.createLineageEdge('testSourceKey')
        lineageEdgeVersionIdOne = git.createLineageEdgeVersion(lineageEdgeId, 5, 4, "testReference",
                                                               "testReferenceParameters",
                                                               {'testKey': 'testValue'}, 1)
        lineageEdgeVersionIdTwo = git.createLineageEdgeVersion(lineageEdgeId, 5, 4, "testReference",
                                                               "testReferenceParameters",
                                                               {'testKey': 'testValue'}, 1,
                                                               [lineageEdgeVersionIdOne])
        lineageEdgeVersionIdThree = git.createLineageEdgeVersion(lineageEdgeId, 5, 4, "testReference",
                                                                 "testReferenceParameters",
                                                                 {'testKey': 'testValue'}, 1,
                                                                 [lineageEdgeVersionIdOne, lineageEdgeVersionIdTwo])
        lineageEdgeVersionIdFour = git.createLineageEdgeVersion(lineageEdgeId, 5, 4, "testReference",
                                                                "testReferenceParameters",
                                                                {'testKey': 'testValue'}, 1,
                                                                [lineageEdgeVersionIdTwo])
        lineageEdgeVersionIdFive = git.createLineageEdgeVersion(lineageEdgeId, 5, 4, "testReference",
                                                                "testReferenceParameters",
                                                                {'testKey': 'testValue'}, 1,
                                                                [lineageEdgeVersionIdThree])
        lineageEdgeVersionIdSix = git.createLineageEdgeVersion(lineageEdgeId, 5, 4, "testReference",
                                                               "testReferenceParameters",
                                                               {'testKey': 'testValue'}, 1,
                                                               [lineageEdgeVersionIdThree])
        self.assertEqual(git.getLineageEdgeHistory('testSourceKey'), {'0': 1, '1': 3, '3': 6, '2': 4})

    @unittest.skip
    def test_git_get_lineage_graph_history(self):
        git = ground_git.GitImplementation()
        lineageGraphId = git.createLineageGraph('testSourceKey')
        lineageGraphVersionIdOne = git.createLineageGraphVersion(lineageGraphId, [5, 4], "testReference",
                                                                 "testReferenceParameters",
                                                                 {'testKey': 'testValue'}, 1)
        lineageGraphVersionIdTwo = git.createLineageGraphVersion(lineageGraphId, [5, 4], "testReference",
                                                                 "testReferenceParameters",
                                                                 {'testKey': 'testValue'}, 1,
                                                                 [lineageGraphVersionIdOne])
        lineageGraphVersionIdThree = git.createLineageGraphVersion(lineageGraphId, [5, 4], "testReference",
                                                                   "testReferenceParameters",
                                                                   {'testKey': 'testValue'}, 1,
                                                                   [lineageGraphVersionIdOne, lineageGraphVersionIdTwo])
        lineageGraphVersionIdFour = git.createLineageGraphVersion(lineageGraphId, [5, 4], "testReference",
                                                                  "testReferenceParameters",
                                                                  {'testKey': 'testValue'}, 1,
                                                                  [lineageGraphVersionIdTwo])
        lineageGraphVersionIdFive = git.createLineageGraphVersion(lineageGraphId, [5, 4], "testReference",
                                                                  "testReferenceParameters",
                                                                  {'testKey': 'testValue'}, 1,
                                                                  [lineageGraphVersionIdThree])
        lineageGraphVersionIdSix = git.createLineageGraphVersion(lineageGraphId, [5, 4], "testReference",
                                                                 "testReferenceParameters",
                                                                 {'testKey': 'testValue'}, 1,
                                                                 [lineageGraphVersionIdThree])
        self.assertEqual(git.getLineageGraphHistory('testSourceKey'), {'0': 1, '1': 3, '3': 6, '2': 4})


    def test_git_get_node_version_adjacent_history(self):
        git = ground_git.GitImplementation()
        git.init()
        tag = model.version.tag.Tag({'id': 0, 'key': 'testKey', 'value': 'testValue'})
        nodeId = git.createNode('testSourceKey')
        nodeVersionIdOne = git.createNodeVersion(nodeId, "testReference", "testReferenceParameters",
                                                 {'testTag': tag}, 1)
        nodeVersionIdTwo = git.createNodeVersion(nodeId, "testReference", "testReferenceParameters",
                                                 {'testTag': tag}, 1, [nodeVersionIdOne])
        nodeVersionIdThree = git.createNodeVersion(nodeId, "testReference", "testReferenceParameters",
                                                   {'testTag': tag}, 1,
                                                   [nodeVersionIdOne, nodeVersionIdTwo])
        nodeVersionIdFour = git.createNodeVersion(nodeId, "testReference", "testReferenceParameters",
                                                  {'testTag': tag}, 1, [nodeVersionIdTwo])
        nodeVersionIdFive = git.createNodeVersion(nodeId, "testReference", "testReferenceParameters",
                                                  {'testTag': tag}, 1, [nodeVersionIdThree])
        nodeVersionIdSix = git.createNodeVersion(nodeId, "testReference", "testReferenceParameters",
                                                 {'testTag': tag}, 1,
                                                 [nodeVersionIdThree])
        lineageEdgeId = git.createLineageEdge('testSourceKey')
        lineageEdgeVersionIdOne = git.createLineageEdgeVersion(lineageEdgeId, nodeVersionIdFive,
                                                               nodeVersionIdThree, "testReference",
                                                               "testReferenceParameters",
                                                               {'testTag': tag}, 1)
        lineageEdgeVersionIdTwo = git.createLineageEdgeVersion(lineageEdgeId, nodeVersionIdThree,
                                                               nodeVersionIdTwo, "testReference",
                                                               "testReferenceParameters",
                                                               {'testTag': tag}, 1,
                                                               [lineageEdgeVersionIdOne])
        lineageEdgeVersionIdThree = git.createLineageEdgeVersion(lineageEdgeId, nodeVersionIdFour,
                                                                 nodeVersionIdOne, "testReference",
                                                                 "testReferenceParameters",
                                                                 {'testTag': tag}, 1,
                                                                 [lineageEdgeVersionIdOne, lineageEdgeVersionIdTwo])
        lineageEdgeVersionIdFour = git.createLineageEdgeVersion(lineageEdgeId, nodeVersionIdFive,
                                                                nodeVersionIdTwo , "testReference",
                                                                "testReferenceParameters",
                                                                {'testTag': tag}, 1,
                                                                [lineageEdgeVersionIdTwo])
        lineageEdgeVersionIdFive = git.createLineageEdgeVersion(lineageEdgeId, nodeVersionIdSix,
                                                                nodeVersionIdFour, "testReference",
                                                                "testReferenceParameters",
                                                                {'testTag': tag}, 1,
                                                                [lineageEdgeVersionIdThree])
        lineageEdgeVersionIdSix = git.createLineageEdgeVersion(lineageEdgeId, nodeVersionIdSix,
                                                               nodeVersionIdOne, "testReference",
                                                               "testReferenceParameters",
                                                               {'testTag': tag}, 1,
                                                               [lineageEdgeVersionIdThree])
        adjIdsOne = [adj['id'] for adj in git.getNodeVersionAdjacentLineage(nodeVersionIdOne)]
        self.assertEqual(2, len(adjIdsOne))
        self.assertIn(lineageEdgeVersionIdThree, adjIdsOne)
        self.assertIn(lineageEdgeVersionIdSix, adjIdsOne)
        adjIdsTwo = [adj['id'] for adj in git.getNodeVersionAdjacentLineage(nodeVersionIdTwo)]
        self.assertEqual(2, len(adjIdsTwo))
        self.assertIn(lineageEdgeVersionIdTwo, adjIdsTwo)
        self.assertIn(lineageEdgeVersionIdFour, adjIdsTwo)
        adjIdsThree = [adj['id'] for adj in git.getNodeVersionAdjacentLineage(nodeVersionIdThree)]
        self.assertEqual(2, len(adjIdsThree))
        self.assertIn(lineageEdgeVersionIdOne, adjIdsThree)
        self.assertIn(lineageEdgeVersionIdTwo, adjIdsThree)
        adjIdsFour = [adj['id'] for adj in git.getNodeVersionAdjacentLineage(nodeVersionIdFour)]
        self.assertEqual(2, len(adjIdsFour))
        self.assertIn(lineageEdgeVersionIdThree, adjIdsFour)
        self.assertIn(lineageEdgeVersionIdFive, adjIdsFour)
        adjIdsFive = [adj['id'] for adj in git.getNodeVersionAdjacentLineage(nodeVersionIdFive)]
        self.assertEqual(2, len(adjIdsFive))
        self.assertIn(lineageEdgeVersionIdOne, adjIdsFive)
        self.assertIn(lineageEdgeVersionIdFour, adjIdsFive)
        adjIdsSix = [adj['id'] for adj in git.getNodeVersionAdjacentLineage(nodeVersionIdSix)]
        self.assertEqual(2, len(adjIdsSix))
        self.assertIn(lineageEdgeVersionIdFive, adjIdsSix)
        self.assertIn(lineageEdgeVersionIdSix, adjIdsSix)


if __name__ == '__main__':
    unittest.main()
