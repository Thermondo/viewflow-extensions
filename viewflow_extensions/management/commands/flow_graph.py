from __future__ import absolute_import, unicode_literals

import importlib

from django.core.management import BaseCommand, CommandError
from django.utils.six import text_type

from viewflow_extensions.flow_graph import FlowGraph


class Command(BaseCommand):
    """
    Create graphs from the path to flow class using graphviz.

    Example usage::

        usage: manage.py flow_graph [--svg] flow_path

        Create graph for the given flow.

        positional arguments:
          flow_path             complete path to your flow, i.e. myapp.flows.Flow

        optional arguments:
          -s, --svg             create graph as svg file

    .. note:: This extensions requires ``graphviz`` to be installed.

    """

    help = 'Create graph for the given flow.'

    def add_arguments(self, parser):
        parser.add_argument('flow_path', nargs=1, type=str,
                            help="complete path to your flow, i.e. myapp.flows.Flow")
        parser.add_argument("-s", "--svg",  action="store_true",
                            help="create graph as svg file")

    def handle(self, **options):
        flow_path = options.get('flow_path')
        try:
            file_path, flow_name = flow_path[0].rsplit('.', 1)
        except ValueError:
            raise CommandError("Please, specify the full path to your flow.")
        try:
            flows_file = importlib.import_module(file_path)
            flow_cls = getattr(flows_file, flow_name)
        except ImportError:
            raise CommandError("Could not find file %s" % (file_path, ))
        except (AttributeError, TypeError):
            raise CommandError("Could not find the flow with the name %s" % (flow_name, ))

        flow_graph = FlowGraph(flow_cls)
        graph = flow_graph.create_diagraph()
        if options.get('svg'):
            graph.render(filename='{}'.format(flow_path[0]))
        else:
            self.stdout.write(text_type(graph))
