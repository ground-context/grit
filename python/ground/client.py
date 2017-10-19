import requests

import ground.common.model as model


class GroundClient:

    def __init__(self, hostname="localhost", port=9000):
        self.url = "http://" + hostname + ":" + str(port)

    '''
    HELPER METHODS
    '''

    def _makeGetRequest(self, endpoint, return_json=True):
        request = requests.get(self.url + endpoint)

        if return_json:
            try:
                if request.status_code >= 400:
                    return None
                return request.json()
            except ValueError:
                raise RuntimeError("Unexpected error: Could not decode JSON response from server. Response was " + str(request.status_code) + ".")
        else:
            pass

    def _makePostRequest(self, endpoint, body, return_json=True):
        request = requests.post(self.url + endpoint, json=body)

        if return_json:
            try:
                if request.status_code >= 400:
                    return None
                return request.json()
            except ValueError:
                raise RuntimeError("Unexpected error: Could not decode JSON response from server. Response was " + str(request.status_code) + ".")
        else:
            pass

    def _getRichVersionJson(self, reference, reference_parameters, tags, structure_version_id, parent_ids):
        body = {}

        if reference:
            body["reference"] = reference

        if reference_parameters:
            body["referenceParameters"] = reference_parameters

        if tags:
            body["tags"] = tags

        if structure_version_id > 0:
            body["structureVersionId"] = structure_version_id

        if parent_ids:
            body["parentIds"] = parent_ids

        return body

    def _createItem(self, item_type, source_key, name, tags):
        endpoint = "/" + item_type
        body = {"sourceKey": source_key, "name": name}

        if tags:
            body["tags"] = tags

        return self._makePostRequest(endpoint, body)

    def _getItem(self, item_type, source_key):
        return self._makeGetRequest("/" + item_type + "/" + source_key)

    def _getItemLatestVersions(self, item_type, source_key):
        return self._makeGetRequest("/" + item_type + "/" + source_key + "/latest")

    def _getItemHistory(self, item_type, source_key):
        return self._makeGetRequest("/" + item_type + "/" + source_key + "/history")

    def _getVersion(self, item_type, id):
        return self._makeGetRequest("/versions/" + item_type + "/" + str(id))

    '''
    EDGE METHODS
    '''

    def createEdge(self, source_key, name, from_node_id, to_node_id, tags={}):
        endpoint = "/edges"
        body = {"sourceKey": source_key, "name": name, "fromNodeId": from_node_id, "toNodeId": to_node_id}

        if tags:
            body["tags"] = tags

        response = self._makePostRequest(endpoint, body)
        if response is None:
            return None
        else:
            return model.core.edge.Edge(response)

    def createEdgeVersion(self,
            edge_id,
            to_node_version_start_id,
            from_node_version_start_id,
            to_node_version_end_id=-1,
            from_node_version_end_id=-1,
            reference=None,
            reference_parameters={},
            tags={},
            structure_version_id=-1,
            parent_ids=[]):

        endpoint = "/versions/edges"
        body = self._getRichVersionJson(reference, reference_parameters, tags, structure_version_id, parent_ids)

        body["edgeId"] = edge_id
        body["toNodeVersionStartId"] = to_node_version_start_id
        body["fromNodeVersionStartId"] = from_node_version_start_id

        if to_node_version_end_id > 0:
            body["toNodeVersionEndId"] = to_node_version_end_id

        if from_node_version_end_id > 0:
            body["fromNodeVersionEndId"] = from_node_version_end_id

        response = self._makePostRequest(endpoint, body)
        if response is None:
            return None
        else:
            return model.core.edge_version.EdgeVersion(response)

    def getEdge(self, source_key):
        response = self._getItem("edges", source_key)
        if response is not None:
            return model.core.edge.Edge(response)

    def getEdgeLatestVersions(self, source_key):
        return self._getItemLatestVersions("edges", source_key)

    def getEdgeHistory(self, source_key):
        return self._getItemHistory("edges", source_key)

    def getEdgeVersion(self, id):
        response = self._getVersion("edges", id)
        if response is not None:
            return model.core.edge_version.EdgeVersion(response)

    '''
    GRAPH METHODS
    '''

    def createGraph(self, source_key, name, tags={}):
        response = self._createItem("graphs", source_key, name, tags)
        if response is not None:
            return model.core.graph.Graph(response)

    def createGraphVersion(self,
            graph_id,
            edge_version_ids,
            reference=None,
            reference_parameters={},
            tags={},
            structure_version_id=-1,
            parent_ids=[]):

        endpoint = "/versions/graphs"
        body = self._getRichVersionJson(reference, reference_parameters, tags, structure_version_id, parent_ids)

        body["graphId"] = graph_id
        body["edgeVersionIds"] = edge_version_ids

        response = self._makePostRequest(endpoint, body)
        if response is not None:
            return model.core.graph_version.GraphVersion(response)

    def getGraph(self, source_key):
        response = self._getItem("graphs", source_key)
        if response is not None:
            return model.core.graph.Graph()

    def getGraphLatestVersions(self, source_key):
        return self._getItemLatestVersions("graphs", source_key)

    def getGraphHistory(self, source_key):
        return self._getItemHistory("graphs", source_key)

    def getGraphVersion(self, id):
        response = self._getVersion("graphs", id)
        if response is not None:
            return model.core.graph_version.GraphVersion(response)

    '''
    NODE METHODS
    '''

    def createNode(self, source_key, name, tags={}):
        response = self._createItem("nodes", source_key, name, tags)
        if response is not None:
            return model.core.node.Node(response)

    def createNodeVersion(self,
            node_id,
            reference=None,
            reference_parameters={},
            tags={},
            structure_version_id=-1,
            parent_ids=[]):

        endpoint = "/versions/nodes"
        body = self._getRichVersionJson(reference, reference_parameters, tags, structure_version_id, parent_ids)

        body["nodeId"] = node_id

        response = self._makePostRequest(endpoint, body)
        if response is not None:
            return model.core.node_version.NodeVersion(response)

    def getNode(self, source_key):
        return model.core.node.Node(self._getItem("nodes", source_key))

    def getNodeLatestVersions(self, source_key):
        return model.core.node_version.NodeVersion(self._getItemLatestVersions("nodes", source_key))

    def getNodeHistory(self, source_key):
        return self._getItemHistory("nodes", source_key)

    def getNodeVersion(self, id):
        response = self._getVersion("nodes", id)
        if response is not None:
            return model.core.node.Node(response)

    def getNodeVersionAdjacentLineage(self, id):
        return self._makeGetRequest("/versions/nodes/adjacent/lineage/" + str(id))

    '''
    STRUCTURE METHODS
    '''

    def createStructure(self, source_key, name, tags={}):
        response = self._createItem("structures", source_key, name, tags)
        if response is not None:
            return model.core.structure.Structure(response)

    def createStructureVersion(self,
            structure_id,
            attributes,
            parent_ids=[]):

        endpoint = "/versions/structures"

        body = {"structureId": structure_id, "attributes": attributes}

        response = self._makePostRequest(endpoint, body)
        if response is not None:
            return model.core.structure_version.StructureVersion(response)

    def getStructure(self, source_key):
        response = self._getItem("structures", source_key)
        if response is not None:
            return model.core.structure.Structure(response)

    def getStructureLatestVersions(self, source_key):
        return self._getItemLatestVersions("structures", source_key)

    def getStructureHistory(self, source_key):
        return self._getItemHistory("structures", source_key)

    def getStructureVersion(self, id):
        response = self._getVersion("structures", id)
        if response is not None:
            return model.core.structure_version.StructureVersion(response)

    '''
    LINEAGE EDGE METHODS
    '''

    def createLineageEdge(self, source_key, name, tags={}):
        response = self._createItem("lineage_edges", source_key, name, tags)
        if response is not None:
            return model.usage.lineage_edge.LineageEdge(response)

    def createLineageEdgeVersion(self,
            edge_id,
            to_rich_version_id,
            from_rich_version_id,
            reference=None,
            reference_parameters={},
            tags={},
            structure_version_id=-1,
            parent_ids=[]):

        endpoint = "/versions/lineage_edges"
        body = self._getRichVersionJson(reference, reference_parameters, tags, structure_version_id, parent_ids)

        body["lineageEdgeId"] = edge_id
        body["toRichVersionId"] = to_rich_version_id
        body["fromRichVersionId"] = from_rich_version_id

        response = self._makePostRequest(endpoint, body)
        if response is not None:
            return model.usage.lineage_edge_version.LineageEdgeVersion(response)

    def getLineageEdge(self, source_key):
        response = self._getItem("lineage_edges", source_key)
        if response is not None:
            return model.usage.lineage_edge.LineageEdge(response)

    def getLineageEdgeLatestVersions(self, source_key):
        return self._getItemLatestVersions("lineage_edges", source_key)

    def getLineageEdgeHistory(self, source_key):
        return self._getItemHistory("lineage_edges", source_key)

    def getLineageEdgeVersion(self, id):
        response = self._getVersion("lineage_edges", id)
        if response is not None:
            return model.usage.lineage_edge_version.LineageEdgeVersion(response)

    '''
    LINEAGE GRAPH METHODS
    '''

    def createLineageGraph(self, source_key, name, tags={}):
        response = self._createItem("lineage_graphs", source_key, name, tags)
        if response is not None:
            return model.usage.lineage_graph.LineageGraph(response)

    def createLineageGraphVersion(self,
            lineage_graph_id,
            lineage_edge_version_ids,
            reference=None,
            reference_parameters={},
            tags={},
            structure_version_id=-1,
            parent_ids=[]):

        endpoint = "/versions/lineage_graphs"
        body = self._getRichVersionJson(reference, reference_parameters, tags, structure_version_id, parent_ids)

        body["lineageGraphId"] = lineage_graph_id
        body["lineageEdgeVersionIds"] = lineage_edge_version_ids

        response = self._makePostRequest(endpoint, body)
        if response is not None:
            return model.usage.lineage_graph_version.LineageGraphVersion(response)

    def getLineageGraph(self, source_key):
        response = self._getItem("lineage_graphs", source_key)
        if response is not None:
            return model.usage.lineage_graph.LineageGraph(response)

    def getLineageGraphLatestVersions(self, source_key):
        return self._getItemLatestVersions("lineage_graphs", source_key)

    def getLineageGraphHistory(self, source_key):
        return self._getItemHistory("lineage_graphs", source_key)

    def getLineageGraphVersion(self, id):
        response = self._getVersion("lineage_graphs", id)
        if response is not None:
            return model.usage.lineage_graph_version.LineageGraphVersion(response)
