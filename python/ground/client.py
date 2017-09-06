import requests

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
                return request.json()
            except ValueError:
                raise RuntimeError("Unexpected error: Could not decode JSON response from server. Response was " + str(response) + ".")
        else:
            pass

    def _makePostRequest(self, endpoint, body, return_json=True):
        request = requests.post(self.url + endpoint, json=body)

        if return_json:
            try:
                return request.json()
            except ValueError:
                raise RuntimeError("Unexpected error: Could not decode JSON response from server. Response was " + str(response) + ".")
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

        return self._makePostRequest(endpoint, body)

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

        return self._makePostRequest(endpoint, body)

    def getEdge(self, source_key):
        return self._getItem("edges", source_key)

    def getEdgeLatestVersions(self, source_key):
        return self._getItemLatestVersions("edges", source_key)

    def getEdgeHistory(self, source_key):
        return self._getItemHistory("edges", source_key)

    def getEdgeVersion(self, id):
        return self._getVersion("edges", id)

    '''
    GRAPH METHODS
    '''

    def createGraph(self, source_key, name, tags={}):
        return self._createItem("graphs", source_key, name, tags);

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

        return self._makePostRequest(endpoint, body)

    def getGraph(self, source_key):
        return self._getItem("graphs", source_key)

    def getGraphLatestVersions(self, source_key):
        return self._getItemLatestVersions("graphs", source_key)

    def getGraphHistory(self, source_key):
        return self._getItemHistory("graphs", source_key)

    def getGraphVersion(self, id):
        return self._getVersion("graphs", id)

    '''
    NODE METHODS
    '''

    def createNode(self, source_key, name, tags={}):
        return self._createItem("nodes", source_key, name, tags);

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

        return self._makePostRequest(endpoint, body)

    def getNode(self, source_key):
        return self._getItem("nodes", source_key)

    def getNodeLatestVersions(self, source_key):
        return self._getItemLatestVersions("nodes", source_key)

    def getNodeHistory(self, source_key):
        return self._getItemHistory("nodes", source_key)

    def getNodeVersion(self, id):
        return self._getVersion("nodes", id)

    def getNodeVersionAdjacentLineage(self, id):
        return self._makeGetRequest("/versions/nodes/adjacent/lineage/" + str(id))

    '''
    STRUCTURE METHODS
    '''

    def createStructure(self, source_key, name, tags={}):
        return self._createItem("structures", source_key, name, tags);

    def createStructureVersion(self,
            structure_id,
            attributes,
            parent_ids=[]):

        endpoint = "/versions/structures"

        body = {"structureId": structure_id, "attributes": attributes}

        return self._makePostRequest(endpoint, body)

    def getStructure(self, source_key):
        return self._getItem("structures", source_key)

    def getStructureLatestVersions(self, source_key):
        return self._getItemLatestVersions("structures", source_key)

    def getStructureHistory(self, source_key):
        return self._getItemHistory("structures", source_key)

    def getStructureVersion(self, id):
        return self._getVersion("structures", id)

    '''
    LINEAGE EDGE METHODS
    '''

    def createLineageEdge(self, source_key, name, tags={}):
        return self._createItem("lineage_edges", source_key, name, tags);

    def createLineageEdgeVersion(self,
            edge_id,
            to_rich_version_start_id,
            from_rich_version_start_id,
            reference=None,
            reference_parameters={},
            tags={},
            structure_version_id=-1,
            parent_ids=[]):

        endpoint = "/versions/edges"
        body = self._getRichVersionJson(reference, reference_parameters, tags, structure_version_id, parent_ids)

        body["edgeId"] = edge_id
        body["toRichVersionStartId"] = to_rich_version_start_id
        body["fromRichVersionStartId"] = from_rich_version_start_id

        return self._makePostRequest(endpoint, body)

    def getLineageEdge(self, source_key):
        return self._getItem("lineage_edges", source_key)

    def getLineageEdgeLatestVersions(self, source_key):
        return self._getItemLatestVersions("lineage_edges", source_key)

    def getLineageEdgeHistory(self, source_key):
        return self._getItemHistory("lineage_edges", source_key)

    def getLineageEdgeVersion(self, id):
        return self._getVersion("lineage_edges", id)

    '''
    LINEAGE GRAPH METHODS
    '''

    def createLineageGraph(self, source_key, name, tags={}):
        return self._createItem("lineage_graphs", source_key, name, tags);

    def createLineageGraphVersion(self,
            lineage_graph_id,
            lineage_edge_version_ids,
            reference=None,
            reference_parameters={},
            tags={},
            structure_version_id=-1,
            parent_ids=[]):

        endpoint = "/versions/graphs"
        body = self._getRichVersionJson(reference, reference_parameters, tags, structure_version_id, parent_ids)

        body["graphId"] = graph_id
        body["lineageEVersionIds"] = lineage_edge_version_ids

        return self._makePostRequest(endpoint, body)

    def getLineageGraph(self, source_key):
        return self._getItem("lineage_graphs", source_key)

    def getLineageGraphLatestVersions(self, source_key):
        return self._getItemLatestVersions("lineage_graphs", source_key)

    def getLineageGraphHistory(self, source_key):
        return self._getItemHistory("lineage_graphs", source_key)

    def getLineageGraphVersion(self, id):
        return self._getVersion("lineage_graphs", id)
