from __future__ import absolute_import, unicode_literals

import importlib

from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):
    """
    Create graphs from the path to flow class using graphviz.

    Example usage::

        usage: manage.py flow_graph [--svg] flow_path

        Create graph for the given flow.

        positional arguments:
          flow_path             complete path to your flow, i.e. myapp.flows.Flow

    .. note:: This extensions requires ``graphviz`` to be installed.

    """

    help = 'Create graph for the given flow.'

    def add_arguments(self, parser):
        parser.add_argument('flow_path', nargs=1, type=str,
                            help="complete path to your flow, i.e. myapp.flows.Flow")

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
        try:
            from viewflow import chart
        except ImportError:
            from viewflow_extensions.flow_graph import FlowGraph
            flow_graph = FlowGraph(flow_cls)
            graph = flow_graph.create_diagraph()
            graph.render(filename='{}'.format(flow_path[0]))
        else:
            grid = chart.calc_layout_data(flow_cls)
            svg = chart.grid_to_svg(grid)
            with open(flow_path[0], 'w') as f:
                f.write("%s.svg" % svg)
