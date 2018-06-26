# /usr/bin/env python3
import json
import os
import git
import subprocess

from shutil import copyfile
# noinspection PyUnresolvedReferences
from grit.common.model.core.node import Node
# noinspection PyUnresolvedReferences
from grit.common.model.core.node_version import NodeVersion
# noinspection PyUnresolvedReferences
from grit.common.model.core.edge import Edge
# noinspection PyUnresolvedReferences
from grit.common.model.core.edge_version import EdgeVersion
# noinspection PyUnresolvedReferences
from grit.common.model.core.graph import Graph
# noinspection PyUnresolvedReferences
from grit.common.model.core.graph_version import GraphVersion
# noinspection PyUnresolvedReferences
from grit.common.model.core.structure import Structure
# noinspection PyUnresolvedReferences
from grit.common.model.core.structure_version import StructureVersion
# noinspection PyUnresolvedReferences
from grit.common.model.usage.lineage_edge import LineageEdge
# noinspection PyUnresolvedReferences
from grit.common.model.usage.lineage_edge_version import LineageEdgeVersion
# noinspection PyUnresolvedReferences
from grit.common.model.usage.lineage_graph import LineageGraph
# noinspection PyUnresolvedReferences
from grit.common.model.usage.lineage_graph_version import LineageGraphVersion
# noinspection PyUnresolvedReferences
from grit.common.model.version.tag import Tag

from grit import globals
from grit import gizzard

class GroundClient(object):

    def __init__(self):

        self._items = ['edge', 'graph', 'node', 'structure', 'lineage_edge', 'lineage_graph', 'index']
        self.path = globals.GRIT_D

        self.cls2loc = {
            'Edge' : 'edge/',
            'edge': 'edge/',
            'EdgeVersion' : 'edge/',
            'edgeversion': 'edge/',
            'Graph' : 'graph/',
            'graph': 'graph/',
            'GraphVersion' : 'graph/',
            'graphversion': 'graph',
            'Node' : 'node/',
            'node': 'node/',
            'NodeVersion' : 'node/',
            'nodeversion': 'nodeversion/',
            'Structure' : 'structure/',
            'structure' : 'structure/',
            'StructureVersion' : 'structure/',
            'structureversion' : 'structure/',
            'LineageEdge' : 'lineage_edge/',
            'lineageedge' : 'lineage_edge/',
            'LineageEdgeVersion' : 'lineage_edge/',
            'lineageedgeversion' : 'lineage_edge/',
            'LineageGraph' : 'lineage_graph/',
            'lineagegraph' : 'lineage_graph/',
            'LineageGraphVersion' : 'lineage_graph/',
            'lineagegraphversion' : 'lineage_graph/'
        }

        if not os.path.isdir(self.path):
            os.mkdir(self.path)
            for item in self._items:
                os.mkdir(self.path + item)
        if not os.path.exists(self.path + 'next_id.txt'):
            with open(self.path + 'next_id.txt', 'w') as f:
                f.write('0')
        if not os.path.exists(self.path + 'index/' + 'index.json'):
            with open(self.path + 'index/' + 'index.json', 'w') as f:
                json.dump({}, f)
        if not os.path.exists(self.path + 'index/index_version.json'):
            with open(self.path + 'index/index_version.json', 'w') as f:
                json.dump({}, f)


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

        if structure_version_id and int(structure_version_id) > 0:
            body["structureVersionId"] = structure_version_id

        if parent_ids:
            body["parentIds"] = parent_ids

        return body

    def _deconstruct_rich_version_json(self, body):
        # This method needs MORE TESTING
        bodyRet = dict(body)
        if "tags" in bodyRet and bodyRet["tags"]:
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
            newid = int(f.read())
        nxtid = str(newid + 1)
        with open(self.path + 'next_id.txt', 'w') as f:
            f.write(nxtid)
        return str(newid)

    def _write_files(self, sourceKey, body, className):
        sourceKey = str(sourceKey)
        filename = sourceKey + '.json'
        route = os.path.join(self.path + self.cls2loc[className], sourceKey)

        if os.path.isdir(route):
            repo = git.Repo(route)
        else:
            repo = git.Repo.init(route)

        if 'Version' in className:
            vbody = body['ItemVersion']

            parents = []
            if 'parentIds' in vbody:
                parents = vbody['parentIds']

            if parents is None or len(parents) == 0:
                # Get root/first commit
                commit, id = gizzard.get_commits(sourceKey, self.cls2loc[className])[-1]
                detached_head = True

                for branch, commit_of_branch in gizzard.get_branch_commits(sourceKey, self.cls2loc[className]):
                    if commit_of_branch == commit:
                        gizzard.runThere(['git', 'checkout', branch], sourceKey, self.cls2loc[className])
                        detached_head = False
                        break

                if detached_head:
                    gizzard.runThere(['git', 'checkout', commit], sourceKey, self.cls2loc[className])
                    new_name = gizzard.new_branch_name(sourceKey, self.cls2loc[className])
                    gizzard.runThere(['git', 'checkout', '-b', new_name], sourceKey, self.cls2loc[className])

                # assert: Now at branch with head attached to first commit
            elif len(parents) == 1:
                commit = gizzard.id_to_commit(parents[0], sourceKey, self.cls2loc[className])
                detached_head = True

                for branch, commit_of_branch in gizzard.get_branch_commits(sourceKey, self.cls2loc[className]):
                    if commit_of_branch == commit:
                        gizzard.runThere(['git', 'checkout', branch], sourceKey, self.cls2loc[className])
                        detached_head = False
                        break

                if detached_head:
                    gizzard.runThere(['git', 'checkout', commit], sourceKey, self.cls2loc[className])
                    new_name = gizzard.new_branch_name(sourceKey, self.cls2loc[className])
                    gizzard.runThere(['git', 'checkout', '-b', new_name], sourceKey, self.cls2loc[className])

                # assert: Now at branch with head attached to some commit
            else:
                commits = [gizzard.id_to_commit(p, sourceKey, self.cls2loc[className]) for p in parents]
                branches = []

                for commit in commits:
                    detached_head = True

                    for branch, commit_of_branch in gizzard.get_branch_commits(sourceKey, self.cls2loc[className]):
                        if commit_of_branch == commit:
                            gizzard.runThere(['git', 'checkout', branch], sourceKey, self.cls2loc[className])
                            detached_head = False
                            branches.append(branch)
                            break

                    if detached_head:
                        gizzard.runThere(['git', 'checkout', commit], sourceKey, self.cls2loc[className])
                        new_name = gizzard.new_branch_name(sourceKey, self.cls2loc[className])
                        gizzard.runThere(['git', 'checkout', '-b', new_name], sourceKey, self.cls2loc[className])
                        branches.append(new_name)

                gizzard.runThere(['git', 'merge', '-s', 'ours', '-m', 'id: -1, class: Merge'] + branches[0:-1],
                                 sourceKey, self.cls2loc[className])
                gizzard.runThere(['git', 'branch', '-D'] + branches[0:-1], sourceKey, self.cls2loc[className])

        with open(os.path.join(route, filename), 'w') as f:
            json.dump(body, f)

        repo.index.add([os.path.join(route, filename)])

        if 'Version' in className:
            repo.index.commit("id: {}, class: {}".format(body["ItemVersion"]["id"], className))
        else:
            repo.index.commit("id: {}, class: {}".format(body["Item"]["id"], className))


    def _read_files(self, sourceKey, className, layer):
        route = os.path.join(self.path + self.cls2loc[className], sourceKey)
        with open(os.path.join(route, sourceKey + '.json'), 'r') as f:
            fileDict = json.load(f)
            fileDict = fileDict[layer]
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
        ruta = os.path.join(self.path + self.cls2loc[className], sourceKey)
        return os.path.isdir(ruta)

    def _map_index(self, id, sourceKey):
        # Sloppy index: must read full file to get mapping. Make clever
        # Also, assuming index can fit in memory
        id = str(id)
        ruta = self.path + 'index/'
        with open(ruta + 'index.json', 'r') as f:
            d = json.load(f)
        d[id] = sourceKey
        with open(ruta + 'index.json', 'w') as f:
            json.dump(d, f)

    def _map_version_index(self, id, sourceKey):
        id = str(id)
        ruta = self.path + 'index/'
        with open(ruta + 'index_version.json', 'r') as f:
            d = json.load(f)
        d[id] = sourceKey
        with open(ruta + 'index_version.json', 'w') as f:
            json.dump(d, f)


    def _read_map_index(self, id):
        # Sloppy index: must read full file to get mapping. Make clever
        # Also, assuming index can fit in memory
        id = str(id)
        ruta = self.path + 'index/'
        with open(ruta + 'index.json', 'r') as f:
            d = json.load(f)
        if id not in d:
            raise KeyError(
                "No such key in index: {}".format(id))
        return d[id]

    def _read_map_version_index(self, id):
        id = str(id)
        ruta = self.path + 'index/'
        with open(ruta + 'index_version.json', 'r') as f:
            d = json.load(f)
        if id not in d:
            raise KeyError(
                "No such key in index: {}".format(id))
        return d[id]

    def __run_proc__(self, bashCommand):
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        return str(output, 'UTF-8')

    def _commit(self, id, className, sourcekey):
        # Warning: Piggy-backing index file commit
        totFile = self.path + self.cls2loc[className] + sourcekey + '.json'
        self.repo.index.add([totFile, self.path + 'index/index.json', self.path + 'index/index_version.json'])
        self.repo.index.commit("id: " + str(id) + ", class: " + className)

    @staticmethod
    def _readable_to_conventional(filename):
        filename = filename.split('.')
        assert len(filename) == 3
        filename.reverse()
        filename = '.'.join(filename[1:])

        return filename

    @staticmethod
    def _conventional_to_readable(filename):
        filename = filename.split('.')
        assert len(filename) == 2
        filename.reverse()
        filename.append('txt')

        return '.'.join(filename)


    ### EDGES ###
    def create_edge(self, source_key, name, from_node_id, to_node_id, tags=None):
        if not self._find_file(source_key, Edge.__name__):
            fromNodeId = str(from_node_id)
            toNodeId = str(to_node_id)

            # Enforcing some integrity constraints
            self._read_map_index(fromNodeId)
            self._read_map_index(toNodeId)

            body = self._create_item(Edge.__name__, source_key, name, tags)
            body["fromNodeId"] = fromNodeId
            body["toNodeId"] = toNodeId
            edge = Edge(body)
            edgeId = str(edge.get_id())
            write = self._deconstruct_item(edge)
            write["fromNodeId"] = edge.get_from_node_id()
            write["toNodeId"] = edge.get_to_node_id()
            write = {"Item": write, "ItemVersion": {}}
            self._write_files(source_key, write, Edge.__name__)
            self._map_index(edgeId, source_key)
        else:
            raise FileExistsError(
                "Edge with source key '{}' already exists.".format(source_key))

        return edge

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

        # Missing integrity constraint checks:
        # Passed in node versions must be versions of nodes that are linked by an edge with edgeId == edgeId

        body = self._get_rich_version_json(EdgeVersion.__name__, reference, reference_parameters,
                                           tags, structure_version_id, parent_ids)

        body["edgeId"] = str(edge_id)
        body["toNodeVersionStartId"] = str(to_node_version_start_id)
        body["fromNodeVersionStartId"] = str(from_node_version_start_id)

        if to_node_version_end_id and int(to_node_version_end_id) > 0:
            body["toNodeVersionEndId"] = str(to_node_version_end_id)

        if from_node_version_end_id and int(from_node_version_end_id) > 0:
            body["fromNodeVersionEndId"] = str(from_node_version_end_id)

        sourceKey = self._read_map_index(edge_id)
        edge = self.get_edge(sourceKey)

        edgeVersion = EdgeVersion(body)
        edgeVersionId = str(edgeVersion.get_id())

        write = self._deconstruct_rich_version_json(body)
        write = {"Item": edge.to_dict(), "ItemVersion": write}
        self._write_files(sourceKey, write, EdgeVersion.__name__)
        self._map_version_index(edgeVersionId, sourceKey)

        return edgeVersion

    def get_edge(self, source_key):
        if not self._find_file(source_key, Edge.__name__):
            raise FileNotFoundError(
                "Edge with source key '{}' does not exist.".format(source_key))
        return Edge(self._read_files(source_key, Edge.__name__, "Item"))


    def get_edge_latest_versions(self, source_key):
        latest_versions = []
        for branch, commit in gizzard.get_branch_commits(source_key, 'edge'):
            gizzard.runThere(['git', 'checkout', branch], source_key, 'edge')
            readfiles = self._read_files(source_key, Edge.__name__, "ItemVersion")
            if readfiles:
                ev = EdgeVersion(readfiles)
                latest_versions.append(ev)

        return latest_versions

    def get_edge_history(self, source_key):
        return gizzard.gitdag(source_key, 'edge')

    def get_edge_version(self, evid):
        sourceKey = self._read_map_version_index(evid)
        for commit, id in gizzard.get_ver_commits(sourceKey, 'edge'):
            if id == int(evid):
                with gizzard.chinto(os.path.join(globals.GRIT_D, 'edge', sourceKey)):
                    with gizzard.chkinto(commit):
                        readfiles = self._read_files(sourceKey, Edge.__name__, "ItemVersion")
                    ev = EdgeVersion(readfiles)
                return ev
        raise RuntimeError("Reached invalid line in getEdgeVersion")

    ### NODES ###
    def create_node(self, source_key, name="null", tags=None):
        if not self._find_file(source_key, Node.__name__):
            body = self._create_item(Node.__name__, source_key, name, tags)
            node = Node(body)
            nodeId = str(node.get_item_id())
            write = self._deconstruct_item(node)
            write = {"Item" : write, "ItemVersion": {}}
            self._write_files(source_key, write, Node.__name__)
            self._map_index(nodeId, source_key)
        else:
            raise FileExistsError(
                "Node with source key '{}' already exists.".format(source_key))

        return node

    def create_node_version(self,
                            node_id,
                            reference=None,
                            reference_parameters=None,
                            tags=None,
                            structure_version_id=-1,
                            parent_ids=None):

        body = self._get_rich_version_json(NodeVersion.__name__, reference, reference_parameters,
                                           tags, structure_version_id, parent_ids)

        body["nodeId"] = str(node_id)

        sourceKey = self._read_map_index(node_id)
        node = self.get_node(sourceKey)

        nodeVersion = NodeVersion(body)
        nodeVersionId = str(nodeVersion.get_id())

        write = self._deconstruct_rich_version_json(body)
        write = {"Item": node.to_dict(), "ItemVersion": write}
        self._write_files(sourceKey, write, NodeVersion.__name__)
        self._map_version_index(nodeVersionId, sourceKey)
        return nodeVersion


    def get_node(self, source_key):
        if not self._find_file(source_key, Node.__name__):
            raise FileNotFoundError(
                "Node with source key '{}' does not exist.".format(source_key))
        return Node(self._read_files(source_key, Node.__name__, "Item"))

    def get_node_latest_versions(self, source_key):
        latest_versions = []
        for branch, commit in gizzard.get_branch_commits(source_key, 'node'):
            gizzard.runThere(['git', 'checkout', branch], source_key, 'node')
            readfiles = self._read_files(source_key, Node.__name__, "ItemVersion")
            if readfiles:
                nv = NodeVersion(readfiles)
                latest_versions.append(nv)
        return latest_versions

    def get_node_history(self, source_key):
        return gizzard.gitdag(source_key, 'node')

    def get_node_version(self, nvid):
        sourceKey = self._read_map_version_index(nvid)
        for commit, id in gizzard.get_ver_commits(sourceKey, 'node'):
            if id == int(nvid):
                with gizzard.chinto(os.path.join(globals.GRIT_D, 'node', sourceKey)):
                    with gizzard.chkinto(commit):
                        readfiles = self._read_files(sourceKey, Node.__name__, "ItemVersion")
                    nv = NodeVersion(readfiles)
                return nv
        raise RuntimeError("Reached invalid line in getNodeVersion")

    def get_node_version_adjacent_lineage(self, id):
        # All incoming and outgoing edges
        # Delaying implementation
        lineageEdgeVersionMap = self._read_all_version_ever(LineageEdgeVersion.__name__)
        lineageEdgeVersions = set(list(lineageEdgeVersionMap.keys()))
        adjacent = []
        for levId in lineageEdgeVersions:
            lev = lineageEdgeVersionMap[levId]
            if ((id == lev['toRichVersionId']) or (id == lev['fromRichVersionId'])):
                adjacent.append(lev)
        return adjacent


    ### GRAPHS ###
    def create_graph(self, source_key, name="null", tags=None):
        if not self._find_file(source_key, Graph.__name__, "Item"):
            body = self._create_item(Graph.__name__, source_key, name, tags)
            graph = Graph(body)
            graphId = graph.get_item_id()
            #self.graphs[sourceKey] = graph
            #self.graphs[graphId] = graph
            write = self._deconstruct_item(graph)
            self._write_files(graphId, write)
            self._commit(graphId, Graph.__name__)
        else:
            graph = self._read_files(source_key, Graph.__name__)
            graphId = graph['id']

        return graphId


    def create_graph_version(self,
                             graph_id,
                             edge_version_ids,
                             reference=None,
                             reference_parameters=None,
                             tags=None,
                             structure_version_id=-1,
                             parent_ids=None):

        body = self._get_rich_version_json(GraphVersion.__name__, reference, reference_parameters,
                                           tags, structure_version_id, parent_ids)

        body["graphId"] = graph_id
        body["edgeVersionIds"] = edge_version_ids

        graphVersion = GraphVersion(body)
        graphVersionId = graphVersion.get_id()

        write = self._deconstruct_rich_version_json(body)
        self._write_files(graphVersionId, write)
        self._commit(graphVersionId, GraphVersion.__name__)

        return graphVersionId

    def get_graph(self, source_key):
        return self._read_files(source_key, Graph.__name__)

    def get_graph_latest_versions(self, source_key):
        graphVersionMap = self._read_all_version(source_key, GraphVersion.__name__, Graph.__name__)
        graphVersions = set(list(graphVersionMap.keys()))
        is_parent = set([])
        for evId in graphVersions:
            ev = graphVersionMap[evId]
            if ('parentIds' in ev) and (ev['parentIds']):
                assert type(ev['parentIds']) == list
                for parentId in ev['parentIds']:
                    is_parent |= {parentId, }
        return [graphVersionMap[Id] for Id in list(graphVersions - is_parent)]

    def get_graph_history(self, source_key):
        graphVersionMap = self._read_all_version(source_key, GraphVersion.__name__, Graph.__name__)
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

    def get_graph_version(self, id):
        return self._read_version(id, GraphVersion.__name__)

    ### STRUCTURES ###
    def create_structure(self, source_key, name="null", tags=None):
        if not self._find_file(source_key, Structure.__name__):
            body = self._create_item(Structure.__name__, source_key, name, tags)
            structure = Structure(body)
            structureId = structure.get_item_id()
            #self.structures[sourceKey] = structure
            #self.structures[structureId] = structure
            write = self._deconstruct_item(structure)
            self._write_files(structureId, write)
            self._commit(structureId, Structure.__name__)
        else:
            structure = self._read_files(source_key, Structure.__name__)
            structureId = structure['id']

        return structureId


    def create_structure_version(self,
                                 structure_id,
                                 attributes,
                                 parent_ids=None):

        body = {
            "id": self._gen_id(),
            "class":StructureVersion.__name__,
            "structureId": structure_id,
            "attributes": attributes
        }

        if parent_ids:
            body["parentIds"] = parent_ids

        structureVersion = StructureVersion(body)
        structureVersionId = structureVersion.get_id()

        #self.structureVersions[structureVersionId] = structureVersion

        write = dict(body)
        self._write_files(structureVersionId, write)
        self._commit(structureVersionId, StructureVersion.__name__)

        return structureVersionId

    def get_structure(self, source_key):
        return self._read_files(source_key, Structure.__name__)

    def get_structure_latest_versions(self, source_key):
        structureVersionMap = self._read_all_version(source_key, StructureVersion.__name__, Structure.__name__)
        structureVersions = set(list(structureVersionMap.keys()))
        is_parent = set([])
        for evId in structureVersions:
            ev = structureVersionMap[evId]
            if ('parentIds' in ev) and (ev['parentIds']):
                assert type(ev['parentIds']) == list
                for parentId in ev['parentIds']:
                    is_parent |= {parentId, }
        return [structureVersionMap[Id] for Id in list(structureVersions - is_parent)]

    def get_structure_history(self, source_key):
        structureVersionMap = self._read_all_version(source_key, StructureVersion.__name__, Structure.__name__)
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

    def get_structure_version(self, id):
        return self._read_version(id, StructureVersion.__name__)


    ### LINEAGE EDGES ###
    def create_lineage_edge(self, source_key, name="null", tags=None):
        if not self._find_file(source_key, LineageEdge.__name__):
            body = self._create_item(LineageEdge.__name__, source_key, name, tags)
            lineageEdge = LineageEdge(body)
            lineageEdgeId = str(lineageEdge.get_id())
            write = self._deconstruct_item(lineageEdge)
            write = {"Item": write, "ItemVersion": {}}
            self._write_files(source_key, write, LineageEdge.__name__)
            self._map_index(lineageEdgeId, source_key)
        else:
            raise FileExistsError(
                "Lineage Edge with source key '{}' already exists.".format(source_key))

        return lineageEdge


    def create_lineage_edge_version(self,
                                    edge_id,
                                    to_rich_version_id,
                                    from_rich_version_id,
                                    reference=None,
                                    reference_parameters=None,
                                    tags=None,
                                    structure_version_id=-1,
                                    parent_ids=None):

        body = self._get_rich_version_json(LineageEdgeVersion.__name__, reference, reference_parameters,
                                           tags, structure_version_id, parent_ids)

        body["lineageEdgeId"] = edge_id
        body["toRichVersionId"] = to_rich_version_id
        body["fromRichVersionId"] = from_rich_version_id

        sourceKey = self._read_map_index(edge_id)
        lineage_edge = self.get_lineage_edge(sourceKey)

        lineageEdgeVersion = LineageEdgeVersion(body)
        lineageEdgeVersionId = str(lineageEdgeVersion.get_id())

        write = self._deconstruct_rich_version_json(body)
        write = {"Item": lineage_edge.to_dict(), "ItemVersion": write}
        self._write_files(sourceKey, write, LineageEdgeVersion.__name__)
        self._map_version_index(lineageEdgeVersionId, sourceKey)

        return lineageEdgeVersion

    def get_lineage_edge(self, source_key):
        if not self._find_file(source_key, LineageEdge.__name__):
            raise FileNotFoundError(
                "Lineage Edge with source key '{}' does not exist".format(source_key))

        return LineageEdge(self._read_files(source_key, LineageEdge.__name__, "Item"))

    def get_lineage_edge_latest_versions(self, source_key):
        latest_versions = []
        for branch, commit in gizzard.get_branch_commits(source_key, 'lineage_edge'):
            gizzard.runThere(['git', 'checkout', branch], source_key, 'lineage_edge')
            readfiles = self._read_files(source_key, LineageEdge.__name__, "ItemVersion")
            if readfiles:
                lev = LineageEdgeVersion(readfiles)
                latest_versions.append(lev)
        return latest_versions

    def get_lineage_edge_history(self, source_key):
        return gizzard.gitdag(source_key, 'lineage_edge')

    def get_lineage_edge_version(self, levid):
        sourceKey = self._read_map_version_index(levid)
        for commit, id in gizzard.get_ver_commits(sourceKey, 'lineage_edge'):
            if id == int(levid):
                with gizzard.chinto(os.path.join(globals.GRIT_D, 'lineage_edge', sourceKey)):
                    with gizzard.chkinto(commit):
                        readfiles = self._read_files(sourceKey, LineageEdge.__name__, "ItemVersion")
                    lev = LineageEdgeVersion(readfiles)
                return lev
        raise RuntimeError("Reached invalid line in getNodeVersion")

    ### LINEAGE GRAPHS ###
    def create_lineage_graph(self, source_key, name="null", tags=None):
        if not self._find_file(source_key, LineageGraph.__name__):
            body = self._create_item(LineageGraph.__name__, source_key, name, tags)
            lineageGraph = LineageGraph(body)
            lineageGraphId = lineageGraph.get_id()
            write = self._deconstruct_item(lineageGraph)
            self._write_files(lineageGraphId, write)
            self._commit(lineageGraphId, LineageGraph.__name__)
        else:
            lineageGraph = self._read_files(source_key, LineageGraph.__name__)
            lineageGraphId = lineageGraph['id']

        return lineageGraphId


    def create_lineage_graph_version(self,
                                     lineage_graph_id,
                                     lineage_edge_version_ids,
                                     reference=None,
                                     reference_parameters=None,
                                     tags=None,
                                     structure_version_id=-1,
                                     parent_ids=None):
    
        body = self._get_rich_version_json(LineageGraphVersion.__name__, reference, reference_parameters,
                                           tags, structure_version_id, parent_ids)

        body["lineageGraphId"] = lineage_graph_id
        body["lineageEdgeVersionIds"] = lineage_edge_version_ids

        lineageGraphVersion = LineageGraphVersion(body)
        lineageGraphVersionId = lineageGraphVersion.get_id()

        write = self._deconstruct_rich_version_json(body)
        self._write_files(lineageGraphVersionId, write)
        self._commit(lineageGraphVersionId, LineageGraphVersion.__name__)

        return lineageGraphVersionId

    def get_lineage_graph(self, source_key):
        return self._read_files(source_key, LineageGraph.__name__)

    def get_lineage_graph_latest_versions(self, source_key):
        lineageGraphVersionMap = self._read_all_version(source_key, LineageGraphVersion.__name__, LineageGraph.__name__)
        lineageGraphVersions = set(list(lineageGraphVersionMap.keys()))
        is_parent = set([])
        for evId in lineageGraphVersions:
            ev = lineageGraphVersionMap[evId]
            if ('parentIds' in ev) and (ev['parentIds']):
                assert type(ev['parentIds']) == list
                for parentId in ev['parentIds']:
                    is_parent |= {parentId, }
        return [lineageGraphVersionMap[Id] for Id in list(lineageGraphVersions - is_parent)]

    def get_lineage_graph_history(self, source_key):
        lineageGraphVersionMap = self._read_all_version(source_key, LineageGraphVersion.__name__, LineageGraph.__name__)
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

    def get_lineage_graph_version(self, id):
        return self._read_version(id, LineageGraphVersion.__name__)
