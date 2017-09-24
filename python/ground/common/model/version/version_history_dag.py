from sets import Set

class VersionHistoryDag:

    def __init__(item_id, edges):
        self._item_id = item_id
        # self._edge_ids = edges.stream().map(VersionSuccessor::getId).collect(Collectors.toList())
        self._parent_child_map = {}
        # edges.forEach(edge -> self.add_to_parent_child_map(edge.getFromId(), edge.getToId()))

    def get_item_id():
        return self._item_id

    def get_edge_ids():
        return self._edge_ids

    def check_item_in_dag(id):
        return id in self._parent_child_map.keys() or id in self.get_leaves()

    def add_edge(parent_id, child_id, successor_id):
        self._edge_ids.add(successor_id)
        self.add_to_parent_child_map(parent_id, child_id)

    def get_parent(child_id):
        return [key for key in self._parent_child_map.keys() if child_id in self._parent_child_map[key]]

    def get_parent_child_pairs():
        result = {}
        for parent in self._parent_child_map.keys():
            children = self._parent_child_map[parent]
            for child in children:
                result[parent] = child
        return result

    def get_leaves():
        leaves = Set(self._parent_child_map.values())
        leaves = leaves.difference(self._parent_child_map.keys())
        return leaves

    def add_to_parent_child_map(parent, child):
        if parent not in self._parent_child_map.keys():
            self._parent_child_map[parent] = []
        self._parent_child_map[parent].append(child)
