import importlib

from django.core.management import BaseCommand, CommandError
from viewflow import chart

BPMN = 'bpmn'
SVG = 'svg'


class Command(BaseCommand):
    """Create graphs from the path to flow class."""

    help = 'Create graph for the given flow.'

    def add_arguments(self, parser):
        parser.add_argument('flow_path', nargs=1, type=str,
                            help="complete path to your flow, i.e. myapp.flows.Flow")
        parser.add_argument('--type', '-t', dest='graph_type', choices=[SVG, BPMN], default=SVG)
        parser.add_argument('--output', '-o', dest='output', type=str, default='',
                            help="Write graph to given filename.")

    def handle(self, **options):
        flow_path = options.get('flow_path')
        output = options.get('output')
        graph_type = options.get('graph_type')
        try:
            file_path, flow_name = flow_path[0].rsplit('.', 1)
        except ValueError as e:
            raise CommandError("Please, specify the full path to your flow.") from e
        try:
            flows_file = importlib.import_module(file_path)
            flow_cls = getattr(flows_file, flow_name)
        except ImportError as e:
            raise CommandError("Could not find file %s" % (file_path,)) from e
        except (AttributeError, TypeError) as e:
            raise CommandError("Could not find the flow with the name %s" % (flow_name,)) from e

        grid = chart.calc_layout_data(flow_cls)
        if graph_type == SVG:
            graph = chart.grid_to_svg(grid)
        if graph_type == BPMN:
            graph = chart.grid_to_bpmn(grid)
        if output != '':
            with open(output, 'w') as f:
                f.write(graph)
        else:
            self.stdout.write(graph)
