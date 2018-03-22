# /usr/bin/env python3
import requests
import json
import numpy as np
import os
import git
import subprocess
from shutil import copyfile
# noinspection PyUnresolvedReferences
from ground.common.model.core.node import Node
# noinspection PyUnresolvedReferences
from ground.common.model.core.node_version import NodeVersion
# noinspection PyUnresolvedReferences
from ground.common.model.core.edge import Edge
# noinspection PyUnresolvedReferences
from ground.common.model.core.edge_version import EdgeVersion
# noinspection PyUnresolvedReferences
from ground.common.model.core.graph import Graph
# noinspection PyUnresolvedReferences
from ground.common.model.core.graph_version import GraphVersion
# noinspection PyUnresolvedReferences
from ground.common.model.core.structure import Structure
# noinspection PyUnresolvedReferences
from ground.common.model.core.structure_version import StructureVersion
# noinspection PyUnresolvedReferences
from ground.common.model.usage.lineage_edge import LineageEdge
# noinspection PyUnresolvedReferences
from ground.common.model.usage.lineage_edge_version import LineageEdgeVersion
# noinspection PyUnresolvedReferences
from ground.common.model.usage.lineage_graph import LineageGraph
# noinspection PyUnresolvedReferences
from ground.common.model.usage.lineage_graph_version import LineageGraphVersion
# noinspection PyUnresolvedReferences
from ground.common.model.version.tag import Tag

"""
Abstract class: do not instantiate
"""


class GroundAPI:
    headers = {"Content-type": "application/json"}

    ### EDGES ###
    def createEdge(self, sourceKey, fromNodeId, toNodeId, name="null", tags=None):
        d = {
            "sourceKey": sourceKey,
            "fromNodeId": fromNodeId,
            "toNodeId": toNodeId,
            "name": name
        }
        if tags is not None:
            d["tags"] = tags
        return d

    def createEdgeVersion(self, edgeId, toNodeVersionStartId, fromNodeVersionStartId, toNodeVersionEndId=None,
                          fromNodeVersionEndId=None, reference=None, referenceParameters=None, tags=None,
                          structureVersionId=None, parentIds=None):
        d = {
            "edgeId": edgeId,
            "fromNodeVersionStartId": fromNodeVersionStartId,
            "toNodeVersionStartId": toNodeVersionStartId
        }
        if toNodeVersionEndId is not None:
            d["toNodeVersionEndId"] = toNodeVersionEndId
        if fromNodeVersionEndId is not None:
            d["fromNodeVersionEndId"] = fromNodeVersionEndId
        if reference is not None:
            d["reference"] = reference
        if referenceParameters is not None:
            d["referenceParameters"] = referenceParameters
        if tags is not None:
            d["tags"] = tags
        if structureVersionId is not None:
            d["structureVersionId"] = structureVersionId
        if parentIds is not None:
            d["parentIds"] = parentIds
        return d

    def getEdge(self, sourceKey):
        raise NotImplementedError("Invalid call to GroundClient.getEdge")

    def getEdgeLatestVersions(self, sourceKey):
        raise NotImplementedError(
            "Invalid call to GroundClient.getEdgeLatestVersions")

    def getEdgeHistory(self, sourceKey):
        raise NotImplementedError(
            "Invalid call to GroundClient.getEdgeHistory")

    def getEdgeVersion(self, edgeId):
        raise NotImplementedError(
            "Invalid call to GroundClient.getEdgeVersion")

    ### NODES ###
    def createNode(self, sourceKey, name="null", tags=None):
        d = {
            "sourceKey": sourceKey,
            "name": name
        }
        if tags is not None:
            d["tags"] = tags
        return d

    def createNodeVersion(self, nodeId, reference=None, referenceParameters=None, tags=None,
                          structureVersionId=None, parentIds=None):
        d = {
            "nodeId": nodeId
        }
        if reference is not None:
            d["reference"] = reference
        if referenceParameters is not None:
            d["referenceParameters"] = referenceParameters
        if tags is not None:
            d["tags"] = tags
        if structureVersionId is not None:
            d["structureVersionId"] = structureVersionId
        if parentIds is not None:
            d["parentIds"] = parentIds
        return d

    def getNode(self, sourceKey):
        raise NotImplementedError("Invalid call to GroundClient.getNode")

    def getNodeLatestVersions(self, sourceKey):
        raise NotImplementedError(
            "Invalid call to GroundClient.getNodeLatestVersions")

    def getNodeHistory(self, sourceKey):
        raise NotImplementedError(
            "Invalid call to GroundClient.getNodeHistory")

    def getNodeVersion(self, nodeId):
        raise NotImplementedError(
            "Invalid call to GroundClient.getNodeVersion")

    def getNodeVersionAdjacentLineage(self, nodeId):
        raise NotImplementedError(
            "Invalid call to GroundClient.getNodeVersionAdjacentLineage")

    ### GRAPHS ###
    def createGraph(self, sourceKey, name="null", tags=None):
        d = {
            "sourceKey": sourceKey,
            "name": name
        }
        if tags is not None:
            d["tags"] = tags
        return d

    def createGraphVersion(self, graphId, edgeVersionIds, reference=None, referenceParameters=None,
                           tags=None, structureVersionId=None, parentIds=None):
        d = {
            "graphId": graphId,
            "edgeVersionIds": edgeVersionIds
        }
        if reference is not None:
            d["reference"] = reference
        if referenceParameters is not None:
            d["referenceParameters"] = referenceParameters
        if tags is not None:
            d["tags"] = tags
        if structureVersionId is not None:
            d["structureVersionId"] = structureVersionId
        if parentIds is not None:
            d["parentIds"] = parentIds
        return d

    def getGraph(self, sourceKey):
        raise NotImplementedError("Invalid call to GroundClient.getGraph")

    def getGraphLatestVersions(self, sourceKey):
        raise NotImplementedError(
            "Invalid call to GroundClient.getGraphLatestVersions")

    def getGraphHistory(self, sourceKey):
        raise NotImplementedError(
            "Invalid call to GroundClient.getGraphHistory")

    def getGraphVersion(self, graphId):
        raise NotImplementedError(
            "Invalid call to GroundClient.getGraphVersion")

    ### STRUCTURES ###
    def createStructure(self, sourceKey, name="null", tags=None):
        d = {
            "sourceKey": sourceKey,
            "name": name
        }
        if tags is not None:
            d["tags"] = tags
        return d

    def createStructureVersion(self, structureId, attributes, parentIds=None):
        d = {
            "structureId": structureId,
            "attributes": attributes
        }
        if parentIds is not None:
            d["parentIds"] = parentIds
        return d

    def getStructure(self, sourceKey):
        raise NotImplementedError("Invalid call to GroundClient.getStructure")

    def getStructureLatestVersions(self, sourceKey):
        raise NotImplementedError(
            "Invalid call to GroundClient.getStructureLatestVersions")

    def getStructureHistory(self, sourceKey):
        raise NotImplementedError(
            "Invalid call to GroundClient.getStructureHistory")

    def getStructureVersion(self, structureId):
        raise NotImplementedError(
            "Invalid call to GroundClient.getStructureVersion")

    ### LINEAGE EDGES ###
    def createLineageEdge(self, sourceKey, name="null", tags=None):
        d = {
            "sourceKey": sourceKey,
            "name": name
        }
        if tags is not None:
            d["tags"] = tags
        return d

    def createLineageEdgeVersion(self, lineageEdgeId, toRichVersionId, fromRichVersionId, reference=None,
                                 referenceParameters=None, tags=None, structureVersionId=None, parentIds=None):
        d = {
            "lineageEdgeId": lineageEdgeId,
            "toRichVersionId": toRichVersionId,
            "fromRichVersionId": fromRichVersionId
        }
        if reference is not None:
            d["reference"] = reference
        if referenceParameters is not None:
            d["referenceParameters"] = referenceParameters
        if tags is not None:
            d["tags"] = tags
        if structureVersionId is not None:
            d["structureVersionId"] = structureVersionId
        if parentIds is not None:
            d["parentIds"] = parentIds
        return d

    def getLineageEdge(self, sourceKey):
        raise NotImplementedError("Invalid call to GroundClient.getLineageEdge")

    def getLineageEdgeLatestVersions(self, sourceKey):
        raise NotImplementedError(
            "Invalid call to GroundClient.getLineageEdgeLatestVersions")

    def getLineageEdgeHistory(self, sourceKey):
        raise NotImplementedError(
            "Invalid call to GroundClient.getLineageEdgeHistory")

    def getLineageEdgeVersion(self, lineageEdgeId):
        raise NotImplementedError(
            "Invalid call to GroundClient.getLineageEdgeVersion")

    ### LINEAGE GRAPHS ###
    def createLineageGraph(self, sourceKey, name="null", tags=None):
        d = {
            "sourceKey": sourceKey,
            "name": name
        }
        if tags is not None:
            d["tags"] = tags
        return d

    def createLineageGraphVersion(self, lineageGraphId, lineageEdgeVersionIds, reference=None,
                                  referenceParameters=None, tags=None, structureVersionId=None, parentIds=None):
        d = {
            "lineageGraphId": lineageGraphId,
            "lineageEdgeVersionIds": lineageEdgeVersionIds
        }
        if reference is not None:
            d["reference"] = reference
        if referenceParameters is not None:
            d["referenceParameters"] = referenceParameters
        if tags is not None:
            d["tags"] = tags
        if structureVersionId is not None:
            d["structureVersionId"] = structureVersionId
        if parentIds is not None:
            d["parentIds"] = parentIds
        return d

    def getLineageGraph(self, sourceKey):
        raise NotImplementedError("Invalid call to GroundClient.getLineageGraph")

    def getLineageGraphLatestVersions(self, sourceKey):
        raise NotImplementedError(
            "Invalid call to GroundClient.getLineageGraphLatestVersions")

    def getLineageGraphHistory(self, sourceKey):
        raise NotImplementedError(
            "Invalid call to GroundClient.getLineageGraphHistory")

    def getLineageGraphVersion(self, lineageGraphId):
        raise NotImplementedError(
            "Invalid call to GroundClient.getLineageGraphVersion")

class GitImplementation(GroundAPI):
    def __init__(self):

        self.path = os.path.expanduser('~') + "/grit.d/"

        if not os.path.isdir(self.path):
            os.mkdir(self.path)
            self.repo = git.Repo.init(self.path)
            if not os.path.exists(self.path + '.gitignore'):
                with open(self.path + '.gitignore', 'w') as f:
                    f.write('next_id.txt\n')
                self.repo.index.add([self.path + '.gitignore'])
                self.repo.index.commit("Initialize Ground GitImplementation repository")
        if not os.path.exists(self.path + 'next_id.txt'):
            with open(self.path + 'next_id.txt', 'w') as f:
                f.write('0')


    def _get_rich_version_json(self, item_type, reference, reference_parameters,
                               tags, structure_version_id, parent_ids):
        item_id = self._gen_id()
        body = {"id": item_id, "class": item_type}
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

    def _deconstruct_rich_version_json(self, body):
        bodyRet = dict(body)
        if bodyRet["tags"]:
            bodyTags = {}
            for key, value in list((bodyRet["tags"]).items()):
                if isinstance(value, Tag):
                    bodyTags[key] = {'id': value.get_id(), 'key': value.get_key(), 'value': value.get_value()}
            bodyRet["tags"] = bodyTags

        return bodyRet

    def _create_item(self, item_type, source_key, name, tags):
        item_id = self._gen_id()
        body = {"sourceKey": source_key, "name": name, "class": item_type, "id": item_id}

        if tags:
            body["tags"] = tags

        return body

    def _deconstruct_item(self, item):
        body = {"id": item.get_id(), "class": type(item).__name__, "name": item.get_name(),
                "sourceKey": item.get_source_key()}

        if item.get_tags():
            bodyTags = {}
            for key, value in list((item.get_tags()).items()):
                if isinstance(value, Tag):
                    bodyTags[key] = {'id': value.get_id(), 'key': value.get_key(), 'value': value.get_value()}
            body["tags"] = bodyTags

        return body

    def _gen_id(self):
        with open(self.path + 'next_id.txt', 'r') as f:
            ids = json.loads(f.read())
        newid = len(ids)
        ids[newid] = newid
        with open(self.path + 'next_id.txt', 'w') as f2:
            f2.write(json.dumps(ids))
        return newid

    def _write_files(self, id, body):
        with open(self.path + str(id) + '.json', 'w') as f:
            f.write(json.dumps(body))

    def _read_files(self, sourceKey, className):
        files = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        for file in files:
            filename = file.split('.')
            if (filename[-1] == 'json') and (filename[0] != 'ids'):
                with open(self.path + file, 'r') as f:
                    fileDict = json.loads(f.read())
                    if (('sourceKey' in fileDict) and (fileDict['sourceKey'] == sourceKey)
                        and (fileDict['class'] == className)):
                        return fileDict

    def _read_version(self, id, className):
        files = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        for file in files:
            filename = file.split('.')
            if (filename[-1] == 'json') and (filename[0] == str(id)):
                with open(self.path + file, 'r') as f:
                    fileDict = json.loads(f.read())
                    if (fileDict['class'] == className):
                        return fileDict

    def _read_all_version(self, sourceKey, className, baseClassName):
        baseId = (self._read_files(sourceKey, baseClassName))['id']
        baseIdName = baseClassName[:1].lower() + baseClassName[1:] + "Id"

        versions = {}
        files = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        for file in files:
            filename = file.split('.')
            if (filename[-1] == 'json') and (filename[0] != 'ids'):
                with open(self.path + file, 'r') as f:
                    fileDict = json.loads(f.read())
                    if ((baseIdName in fileDict) and (fileDict[baseIdName] == baseId)
                        and (fileDict['class'] == className)):
                        versions[fileDict['id']] = fileDict
        return versions

    def _read_all_version_ever(self, className):
        versions = {}
        files = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        for file in files:
            filename = file.split('.')
            if (filename[-1] == 'json') and (filename[0] != 'ids'):
                with open(self.path + file, 'r') as f:
                    fileDict = json.loads(f.read())
                    if (fileDict['class'] == className):
                        versions[fileDict['id']] = fileDict
        return versions

    def _find_file(self, sourceKey, className):
        files = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        for file in files:
            filename = file.split('.')
            if (filename[-1] == 'json') and (filename[0] != 'ids'):
                with open(self.path + file, 'r') as f:
                    fileDict = json.loads(f.read())
                    if (('sourceKey' in fileDict) and (fileDict['sourceKey'] == sourceKey)
                        and (fileDict['class'] == className)):
                        return True
        return False

    def __run_proc__(self, bashCommand):
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        return str(output, 'UTF-8')

    def _commit(self, id, className):
        totFile = self.path + str(id) + '.json'
        self.repo.index.add([totFile])
        self.repo.index.commit("id: " + str(id) + ", class: " + className)

        ### EDGES ###
    def createEdge(self, sourceKey, fromNodeId, toNodeId, name="null", tags=None):
        if not self._find_file(sourceKey, Edge.__name__):
            body = self._create_item(Edge.__name__, sourceKey, name, tags)
            body["fromNodeId"] = fromNodeId
            body["toNodeId"] = toNodeId
            edge = Edge(body)
            edgeId = edge.get_id()
            #self.edges[sourceKey] = edge
            #self.edges[edgeId] = edge
            write = self._deconstruct_item(edge)
            write["fromNodeId"] = edge.get_from_node_id()
            write["toNodeId"] = edge.get_to_node_id()
            self._write_files(edgeId, write)
            self._commit(edgeId, Edge.__name__)
        else:
            edge = self._read_files(sourceKey, Edge.__name__)
            edgeId = edge['id']

        return edgeId

    def createEdgeVersion(self, edgeId, toNodeVersionStartId, fromNodeVersionStartId, toNodeVersionEndId=None,
                          fromNodeVersionEndId=None, reference=None, referenceParameters=None, tags=None,
                          structureVersionId=None, parentIds=None):
        body = self._get_rich_version_json(EdgeVersion.__name__, reference, referenceParameters,
                                           tags, structureVersionId, parentIds)

        body["edgeId"] = edgeId
        body["toNodeVersionStartId"] = toNodeVersionStartId
        body["fromNodeVersionStartId"] = fromNodeVersionStartId

        if toNodeVersionEndId > 0:
            body["toNodeVersionEndId"] = toNodeVersionEndId

        if fromNodeVersionEndId > 0:
            body["fromNodeVersionEndId"] = fromNodeVersionEndId

        edgeVersion = EdgeVersion(body)
        edgeVersionId = edgeVersion.get_id()

        #self.edgeVersions[edgeVersionId] = edgeVersion

        write = self._deconstruct_rich_version_json(body)
        self._write_files(edgeVersionId, write)
        self._commit(edgeVersionId, EdgeVersion.__name__)

        return edgeVersionId

    def getEdge(self, sourceKey):
        return self._read_files(sourceKey, Edge.__name__)


    def getEdgeLatestVersions(self, sourceKey):
        edgeVersionMap = self._read_all_version(sourceKey, EdgeVersion.__name__, Edge.__name__)
        edgeVersions = set(list(edgeVersionMap.keys()))
        is_parent = set([])
        for evId in edgeVersions:
            ev = edgeVersionMap[evId]
            if ('parentIds' in ev) and (ev['parentIds']):
                assert type(ev['parentIds']) == list
                for parentId in ev['parentIds']:
                    is_parent |= {parentId, }
        return [edgeVersionMap[Id] for Id in list(edgeVersions - is_parent)]

    def getEdgeHistory(self, sourceKey):
        edgeVersionMap = self._read_all_version(sourceKey, EdgeVersion.__name__, Edge.__name__)
        edgeVersions = set(list(edgeVersionMap.keys()))
        parentChild = {}
        for evId in edgeVersions:
            ev = edgeVersionMap[evId]
            if ('parentIds' in ev) and (ev['parentIds']):
                assert type(ev['parentIds']) == list
                for parentId in ev['parentIds']:
                    if not parentChild:
                        edgeId = ev['edgeId']
                        parentChild[str(edgeId)] = parentId
                    parentChild[str(parentId)] = ev['id']
        return parentChild

    def getEdgeVersion(self, edgeVersionId):
        return self._read_version(edgeVersionId, EdgeVersion.__name__)

    ### NODES ###
    def createNode(self, sourceKey, name="null", tags=None):
        if not self._find_file(sourceKey, Node.__name__):
            body = self._create_item(Node.__name__, sourceKey, name, tags)
            node = Node(body)
            nodeId = node.get_item_id()
            #self.nodes[sourceKey] = node
            #self.nodes[nodeId] = node
            write = self._deconstruct_item(node)
            self._write_files(nodeId, write)
            self._commit(nodeId, Node.__name__)
        else:
            node = self._read_files(sourceKey, Node.__name__)
            nodeId = node['id']

        return nodeId

    def createNodeVersion(self, nodeId, reference=None, referenceParameters=None, tags=None,
                          structureVersionId=None, parentIds=None):
        body = self._get_rich_version_json(NodeVersion.__name__, reference, referenceParameters,
                                           tags, structureVersionId, parentIds)

        body["nodeId"] = nodeId

        nodeVersion = NodeVersion(body)
        nodeVersionId = nodeVersion.get_id()

        #self.nodeVersions[nodeVersionId] = nodeVersion

        write = self._deconstruct_rich_version_json(body)
        self._write_files(nodeVersionId, write)
        self._commit(nodeVersionId, NodeVersion.__name__)

        return nodeVersionId


    def getNode(self, sourceKey):
        return self._read_files(sourceKey, Node.__name__)

    def getNodeLatestVersions(self, sourceKey):
        nodeVersionMap = self._read_all_version(sourceKey, NodeVersion.__name__, Node.__name__)
        nodeVersions = set(list(nodeVersionMap.keys()))
        is_parent = set([])
        for evId in nodeVersions:
            ev = nodeVersionMap[evId]
            if ('parentIds' in ev) and (ev['parentIds']):
                assert type(ev['parentIds']) == list
                for parentId in ev['parentIds']:
                    is_parent |= {parentId, }
        return [nodeVersionMap[Id] for Id in list(nodeVersions - is_parent)]

    def getNodeHistory(self, sourceKey):
        nodeVersionMap = self._read_all_version(sourceKey, NodeVersion.__name__, Node.__name__)
        nodeVersions = set(list(nodeVersionMap.keys()))
        parentChild = {}
        for evId in nodeVersions:
            ev = nodeVersionMap[evId]
            if ('parentIds' in ev) and (ev['parentIds']):
                assert type(ev['parentIds']) == list
                for parentId in ev['parentIds']:
                    if not parentChild:
                        nodeId = ev['nodeId']
                        parentChild[str(nodeId)] = parentId
                    parentChild[str(parentId)] = ev['id']
        return parentChild

    def getNodeVersion(self, nodeVersionId):
        return self._read_version(nodeVersionId, NodeVersion.__name__)


    def getNodeVersionAdjacentLineage(self, nodeVersionId):
        lineageEdgeVersionMap = self._read_all_version_ever(LineageEdgeVersion.__name__)
        lineageEdgeVersions = set(list(lineageEdgeVersionMap.keys()))
        adjacent = []
        for levId in lineageEdgeVersions:
            lev = lineageEdgeVersionMap[levId]
            if ((nodeVersionId == lev['toRichVersionId']) or (nodeVersionId == lev['fromRichVersionId'])):
                adjacent.append(lev)
        return adjacent


    ### GRAPHS ###
    def createGraph(self, sourceKey, name="null", tags=None):
        if not self._find_file(sourceKey, Graph.__name__):
            body = self._create_item(Graph.__name__, sourceKey, name, tags)
            graph = Graph(body)
            graphId = graph.get_item_id()
            #self.graphs[sourceKey] = graph
            #self.graphs[graphId] = graph
            write = self._deconstruct_item(graph)
            self._write_files(graphId, write)
            self._commit(graphId, Graph.__name__)
        else:
            graph = self._read_files(sourceKey, Graph.__name__)
            graphId = graph['id']

        return graphId


    def createGraphVersion(self, graphId, edgeVersionIds, reference=None,
                           referenceParameters=None, tags=None, structureVersionId=None, parentIds=None):
        body = self._get_rich_version_json(GraphVersion.__name__, reference, referenceParameters,
                                           tags, structureVersionId, parentIds)

        body["graphId"] = graphId
        body["edgeVersionIds"] = edgeVersionIds

        graphVersion = GraphVersion(body)
        graphVersionId = graphVersion.get_id()

        #self.graphVersions[graphVersionId] = graphVersion

        write = self._deconstruct_rich_version_json(body)
        self._write_files(graphVersionId, write)
        self._commit(graphVersionId, GraphVersion.__name__)

        return graphVersionId

    def getGraph(self, sourceKey):
        return self._read_files(sourceKey, Graph.__name__)

    def getGraphLatestVersions(self, sourceKey):
        graphVersionMap = self._read_all_version(sourceKey, GraphVersion.__name__, Graph.__name__)
        graphVersions = set(list(graphVersionMap.keys()))
        is_parent = set([])
        for evId in graphVersions:
            ev = graphVersionMap[evId]
            if ('parentIds' in ev) and (ev['parentIds']):
                assert type(ev['parentIds']) == list
                for parentId in ev['parentIds']:
                    is_parent |= {parentId, }
        return [graphVersionMap[Id] for Id in list(graphVersions - is_parent)]

    def getGraphHistory(self, sourceKey):
        graphVersionMap = self._read_all_version(sourceKey, GraphVersion.__name__, Graph.__name__)
        graphVersions = set(list(graphVersionMap.keys()))
        parentChild = {}
        for evId in graphVersions:
            ev = graphVersionMap[evId]
            if ('parentIds' in ev) and (ev['parentIds']):
                assert type(ev['parentIds']) == list
                for parentId in ev['parentIds']:
                    if not parentChild:
                        graphId = ev['graphId']
                        parentChild[str(graphId)] = parentId
                    parentChild[str(parentId)] = ev['id']
        return parentChild

    def getGraphVersion(self, graphVersionId):
        return self._read_version(graphVersionId, GraphVersion.__name__)

    ### STRUCTURES ###
    def createStructure(self, sourceKey, name="null", tags=None):
        if not self._find_file(sourceKey, Structure.__name__):
            body = self._create_item(Structure.__name__, sourceKey, name, tags)
            structure = Structure(body)
            structureId = structure.get_item_id()
            #self.structures[sourceKey] = structure
            #self.structures[structureId] = structure
            write = self._deconstruct_item(structure)
            self._write_files(structureId, write)
            self._commit(structureId, Structure.__name__)
        else:
            structure = self._read_files(sourceKey, Structure.__name__)
            structureId = structure['id']

        return structureId


    def createStructureVersion(self, structureId, attributes, parentIds=None):
        body = {
            "id": self._gen_id(),
            "class":StructureVersion.__name__,
            "structureId": structureId,
            "attributes": attributes
        }

        if parentIds:
            body["parentIds"] = parentIds

        structureVersion = StructureVersion(body)
        structureVersionId = structureVersion.get_id()

        #self.structureVersions[structureVersionId] = structureVersion

        write = dict(body)
        self._write_files(structureVersionId, write)
        self._commit(structureVersionId, StructureVersion.__name__)

        return structureVersionId

    def getStructure(self, sourceKey):
        return self._read_files(sourceKey, Structure.__name__)

    def getStructureLatestVersions(self, sourceKey):
        structureVersionMap = self._read_all_version(sourceKey, StructureVersion.__name__, Structure.__name__)
        structureVersions = set(list(structureVersionMap.keys()))
        is_parent = set([])
        for evId in structureVersions:
            ev = structureVersionMap[evId]
            if ('parentIds' in ev) and (ev['parentIds']):
                assert type(ev['parentIds']) == list
                for parentId in ev['parentIds']:
                    is_parent |= {parentId, }
        return [structureVersionMap[Id] for Id in list(structureVersions - is_parent)]

    def getStructureHistory(self, sourceKey):
        structureVersionMap = self._read_all_version(sourceKey, StructureVersion.__name__, Structure.__name__)
        structureVersions = set(list(structureVersionMap.keys()))
        parentChild = {}
        for evId in structureVersions:
            ev = structureVersionMap[evId]
            if ('parentIds' in ev) and (ev['parentIds']):
                assert type(ev['parentIds']) == list
                for parentId in ev['parentIds']:
                    if not parentChild:
                        structureId = ev['structureId']
                        parentChild[str(structureId)] = parentId
                    parentChild[str(parentId)] = ev['id']
        return parentChild

    def getStructureVersion(self, structureVersionId):
        return self._read_version(structureVersionId, StructureVersion.__name__)


    ### LINEAGE EDGES ###
    def createLineageEdge(self, sourceKey, name="null", tags=None):
        if not self._find_file(sourceKey, LineageEdge.__name__):
            body = self._create_item(LineageEdge.__name__, sourceKey, name, tags)
            lineageEdge = LineageEdge(body)
            lineageEdgeId = lineageEdge.get_id()
            #self.lineageEdges[sourceKey] = lineageEdge
            #self.lineageEdges[lineageEdgeId] = lineageEdge
            write = self._deconstruct_item(lineageEdge)
            self._write_files(lineageEdgeId, write)
            self._commit(lineageEdgeId, LineageEdge.__name__)
        else:
            lineageEdge = self._read_files(sourceKey, LineageEdge.__name__)
            lineageEdgeId = lineageEdge['id']

        return lineageEdgeId


    def createLineageEdgeVersion(self, lineageEdgeId, toRichVersionId, fromRichVersionId, reference=None,
                                 referenceParameters=None, tags=None, structureVersionId=None, parentIds=None):
        body = self._get_rich_version_json(LineageEdgeVersion.__name__, reference, referenceParameters,
                                           tags, structureVersionId, parentIds)

        body["lineageEdgeId"] = lineageEdgeId
        body["toRichVersionId"] = toRichVersionId
        body["fromRichVersionId"] = fromRichVersionId

        lineageEdgeVersion = LineageEdgeVersion(body)
        lineageEdgeVersionId = lineageEdgeVersion.get_id()

        #self.lineageEdgeVersions[lineageEdgeVersionId] = lineageEdgeVersion

        write = self._deconstruct_rich_version_json(body)
        self._write_files(lineageEdgeVersionId, write)
        self._commit(lineageEdgeVersionId, LineageEdgeVersion.__name__)

        return lineageEdgeVersionId

    def getLineageEdge(self, sourceKey):
        return self._read_files(sourceKey, LineageEdge.__name__)

    def getLineageEdgeLatestVersions(self, sourceKey):
        lineageEdgeVersionMap = self._read_all_version(sourceKey, LineageEdgeVersion.__name__, LineageEdge.__name__)
        lineageEdgeVersions = set(list(lineageEdgeVersionMap.keys()))
        is_parent = set([])
        for evId in lineageEdgeVersions:
            ev = lineageEdgeVersionMap[evId]
            if ('parentIds' in ev) and (ev['parentIds']):
                assert type(ev['parentIds']) == list
                for parentId in ev['parentIds']:
                    is_parent |= {parentId, }
        return [lineageEdgeVersionMap[Id] for Id in list(lineageEdgeVersions - is_parent)]

    def getLineageEdgeHistory(self, sourceKey):
        lineageEdgeVersionMap = self._read_all_version(sourceKey, LineageEdgeVersion.__name__, LineageEdge.__name__)
        lineageEdgeVersions = set(list(lineageEdgeVersionMap.keys()))
        parentChild = {}
        for evId in lineageEdgeVersions:
            ev = lineageEdgeVersionMap[evId]
            if ('parentIds' in ev) and (ev['parentIds']):
                assert type(ev['parentIds']) == list
                for parentId in ev['parentIds']:
                    if not parentChild:
                        lineageEdgeId = ev['lineageEdgeId']
                        parentChild[str(lineageEdgeId)] = parentId
                    parentChild[str(parentId)] = ev['id']
        return parentChild

    def getLineageEdgeVersion(self, lineageEdgeVersionId):
        return self._read_version(lineageEdgeVersionId, LineageEdgeVersion.__name__)

    ### LINEAGE GRAPHS ###
    def createLineageGraph(self, sourceKey, name="null", tags=None):
        if not self._find_file(sourceKey, LineageGraph.__name__):
            body = self._create_item(LineageGraph.__name__, sourceKey, name, tags)
            lineageGraph = LineageGraph(body)
            lineageGraphId = lineageGraph.get_id()
            #self.lineageGraphs[sourceKey] = lineageGraph
            #self.lineageGraphs[lineageGraphId] = lineageGraph
            write = self._deconstruct_item(lineageGraph)
            self._write_files(lineageGraphId, write)
            self._commit(lineageGraphId, LineageGraph.__name__)
        else:
            lineageGraph = self._read_files(sourceKey, LineageGraph.__name__)
            lineageGraphId = lineageGraph['id']

        return lineageGraphId


    def createLineageGraphVersion(self, lineageGraphId, lineageEdgeVersionIds, reference=None,
                                  referenceParameters=None, tags=None, structureVersionId=None, parentIds=None):
        body = self._get_rich_version_json(LineageGraphVersion.__name__, reference, referenceParameters,
                                           tags, structureVersionId, parentIds)

        body["lineageGraphId"] = lineageGraphId
        body["lineageEdgeVersionIds"] = lineageEdgeVersionIds

        lineageGraphVersion = LineageGraphVersion(body)
        lineageGraphVersionId = lineageGraphVersion.get_id()

        #self.lineageGraphVersions[lineageGraphVersionId] = lineageGraphVersion

        write = self._deconstruct_rich_version_json(body)
        self._write_files(lineageGraphVersionId, write)
        self._commit(lineageGraphVersionId, LineageGraphVersion.__name__)

        return lineageGraphVersionId

    def getLineageGraph(self, sourceKey):
        return self._read_files(sourceKey, LineageGraph.__name__)

    def getLineageGraphLatestVersions(self, sourceKey):
        lineageGraphVersionMap = self._read_all_version(sourceKey, LineageGraphVersion.__name__, LineageGraph.__name__)
        lineageGraphVersions = set(list(lineageGraphVersionMap.keys()))
        is_parent = set([])
        for evId in lineageGraphVersions:
            ev = lineageGraphVersionMap[evId]
            if ('parentIds' in ev) and (ev['parentIds']):
                assert type(ev['parentIds']) == list
                for parentId in ev['parentIds']:
                    is_parent |= {parentId, }
        return [lineageGraphVersionMap[Id] for Id in list(lineageGraphVersions - is_parent)]

    def getLineageGraphHistory(self, sourceKey):
        lineageGraphVersionMap = self._read_all_version(sourceKey, LineageGraphVersion.__name__, LineageGraph.__name__)
        lineageGraphVersions = set(list(lineageGraphVersionMap.keys()))
        parentChild = {}
        for evId in lineageGraphVersions:
            ev = lineageGraphVersionMap[evId]
            if ('parentIds' in ev) and (ev['parentIds']):
                assert type(ev['parentIds']) == list
                for parentId in ev['parentIds']:
                    if not parentChild:
                        lineageGraphId = ev['lineageGraphId']
                        parentChild[str(lineageGraphId)] = parentId
                    parentChild[str(parentId)] = ev['id']
        return parentChild

    def getLineageGraphVersion(self, lineageGraphVersionId):
        return self._read_version(lineageGraphVersionId, LineageGraphVersion.__name__)

    """
    def commit(self):
        stage = []
        for kee in self.graph.ids:
            if kee in self.graph.nodes:
                serial = self.graph.nodes[kee].to_json()
            elif kee in self.graph.nodeVersions:
                serial = self.graph.nodeVersions[kee].to_json()
            elif kee in self.graph.edges:
                serial = self.graph.edges[kee].to_json()
            elif kee in self.graph.edgeVersions:
                serial = self.graph.edgeVersions[kee].to_json()
            elif kee in self.graph.graphs:
                serial = self.graph.graphs[kee].to_json()
            elif kee in self.graph.graphVersions:
                serial = self.graph.graphVersions[kee].to_json()
            elif kee in self.graph.structures:
                serial = self.graph.structures[kee].to_json()
            elif kee in self.graph.structureVersions:
                serial = self.graph.structureVersions[kee].to_json()
            elif kee in self.graph.lineageEdges:
                serial = self.graph.lineageEdges[kee].to_json()
            elif kee in self.graph.lineageEdgeVersions:
                serial = self.graph.lineageEdgeVersions[kee].to_json()
            elif kee in self.graph.lineageGraphs:
                serial = self.graph.lineageGraphs[kee].to_json()
            else:
                serial = self.graph.lineageGraphVersions[kee].to_json()
            assert serial is not None
            with open(str(kee) + '.json', 'w') as f:
                f.write(serial)
            stage.append(str(kee) + '.json')
        repo = git.Repo.init(os.getcwd())
        repo.index.add(stage)
        repo.index.commit("ground commit")
        tree = repo.tree()
        with open('.jarvis', 'w') as f:
            for obj in tree:
                commithash = self.__run_proc__("git log " + obj.path).replace('\n', ' ').split()[1]
                if obj.path != '.jarvis':
                    f.write(obj.path + " " + commithash + "\n")
        repo.index.add(['.jarvis'])
        repo.index.commit('.jarvis commit')

    def load(self):
        if self.graph.ids:
            return
        os.chdir('../')

        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                return False

        listdir = [x for x in filter(is_number, os.listdir())]

        prevDir = str(len(listdir) - 1)
        os.chdir(prevDir)
        for _, _, filenames in os.walk('.'):
            for filename in filenames:
                filename = filename.split('.')
                if filename[-1] == 'json':
                    filename = '.'.join(filename)
                    with open(filename, 'r') as f:
                        self.to_class(json.loads(f.read()))
        os.chdir('../' + str(int(prevDir) + 1))
    """

class GroundImplementation(GroundAPI):
    def __init__(self, host='localhost', port=9000):
        self.host = host
        self.port = str(port)
        self.url = "http://" + self.host + ":" + self.port


class GroundClient(GroundAPI):
    def __new__(*args, **kwargs):
        if args and args[1].strip().lower() == 'git':
            return GitImplementation(**kwargs)
        elif args and args[1].strip().lower() == 'ground':
            # EXAMPLE CALL: GroundClient('ground', host='localhost', port=9000)
            return GroundImplementation(**kwargs)
        else:
            raise ValueError(
                "Backend not supported. Please choose 'git' or 'ground'")
