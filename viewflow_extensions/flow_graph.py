import functools

import graphviz as gv
from viewflow import flow
from viewflow.base import Flow

try:
    from viewflow.flow.obsolete import Obsolete
    from viewflow.contrib.celery import Job
except ImportError:  # Pro only
    class Obsolete(Flow):
        pass

    class Job(Flow):
        pass


GATEWAY = {
    'shape': 'diamond',
    'xlabel': True,
    'fixedsize': 'true',
    'width': '0.75',
    'height': '0.75',
}


class FlowGraph(object):
    """
    Create graph for a given flow class.

    This class serves to create an overview of all the tasks from
    the given flow class and their connections with each other.

    Args:
        flow_cls: a subclass of .viewflow.base.Flow
    """

    node_attrs = {
        flow.Handler: {'shape': 'circle', 'xlabel': True, 'label': ''},
        flow.StartFunction: {'shape': 'doublecircle', 'xlabel': True, 'label': ''},
        flow.Function: {'shape': 'doublecircle', 'xlabel': True, 'label': ''},
        flow.If: dict(label='X', **GATEWAY),
        flow.Switch: dict(label='X', **GATEWAY),
        flow.Join: dict(label='O', **GATEWAY),
        flow.Split: dict(label='+', **GATEWAY),
        flow.End: {'shape': 'doublecircle', 'label': '', 'style': 'filled', 'fillcolor': 'black'},
        flow.StartSignal: {'shape': 'doublecircle', 'xlabel': True, 'label': ''},
        flow.Signal:  {'shape': 'doublecircle', 'xlabel': True, 'label': ''},
        flow.Start: {'shape': 'circle', 'xlabel': True, 'label': ''},
        Job:  {'shape': 'circle', 'xlabel': True, 'label': 'C'},
        Obsolete: {'style': 'invis'},
    }

    def __init__(self, flow_cls: Flow, **attrs):
        self.flow_cls = flow_cls
        self.attrs = attrs

    def get_next(self, node):
        """
        Get all next nodes from a given node.

        Args:
            node: an instance of one of .utils.viewflow_task_types

        Returns:
            List[Node]: a list of all children nodes of the given node.
        """
        if isinstance(node, flow.If):
            return [getattr(node, '_on_true'), getattr(node, '_on_false')]

        if isinstance(node, flow.Switch) or isinstance(node, flow.Split):
            branches = getattr(node, 'branches')
            return [b[0] for b in branches]

        if hasattr(node, '_next'):
            return [getattr(node, '_next')]

    @property
    def node_list(self):
        """
        Return a list of nodes for the given class.

        Returns:
            List[Node]: A list of all nodes in the flow class.
        """
        return {
            getattr(self.flow_cls, item): item
            for item in dir(self.flow_cls)
            if isinstance(getattr(self.flow_cls, item), flow.Node)
        }

    def get_nodes(self):
        return [
            (name, node, dict(self.node_attrs.get(type(node), {})))
            for node, name in self.node_list.items()
        ]

    def get_edges(self):
        """
        Return a list of edges of the flow.

        Returns:
            List[Node]: A list of list of tuples that consists of all the connections
                between the nodes in the flow.
        """
        edges = []
        for node, name in self.node_list.items():
            next_nodes = self.get_next(node)
            if next_nodes:
                for n in next_nodes:
                    edges.append((name, self.node_list[n]))
        return edges

    def _add_nodes(self, graph):
        for name, node, attrs in self.get_nodes():
            if attrs.get('xlabel') is True:
                attrs['xlabel'] = str(node)
            elif 'label' not in attrs:
                attrs['label'] = str(node)
            graph.node(name, **attrs)
        return graph

    def _add_edges(self, graph):
        edges = self.get_edges()
        for e in edges:
            graph.edge(*e)
        return graph

    def create_diagraph(self):
        """
        Return graph representation of the flow.

        Returns:
            graphviz.Digraph: graph instance

        """
        digraph = functools.partial(gv.Digraph, format='svg')
        graph = digraph()
        graph.attr('edge', labelfloat='true')
        graph.attr('graph', rankdir='TB')
        defaults = dict(fontname='sans-serif', shape='box')
        defaults.update(self.attrs)
        graph.attr('node', defaults)
        graph = self._add_edges(self._add_nodes(graph))
        return graph
