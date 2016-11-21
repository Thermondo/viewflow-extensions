"""
Sphinx extension to automatically render BPMN graphs of Flows.

Viewflow-Extensions comes with a Sphinx extensions that render BPMN graphs as SVG
and automatically attaches them to the documentation of each flow.

To enable this feature simply add ``viewflow_extensions.sphinx`` to your Sphinx configuration.

Example::

    extensions = [
        'sphinx.ext.autodoc',
        # ...
        'viewflow_extensions.sphinx',
    ]


.. note:: This extensions requires ``graphviz`` to be installed
    as well as the Sphinx extension ``sphinx.ext.autodoc`` to be enabled.

"""
import inspect
import os
from tempfile import mkdtemp

from viewflow.base import Flow

from . import __version__ as version


def process_flows(app, what, name, obj, options, lines):
    if inspect.isclass(obj) and issubclass(obj, Flow):
        tmp_dir = mkdtemp()
        file_name = os.path.join(tmp_dir, obj._meta.flow_label)
        try:
            from viewflow import chart
        except ImportError:
            from .flow_graph import FlowGraph
            flow_graph = FlowGraph(flow_cls=obj)
            graph = flow_graph.create_diagraph()
            svg_file_path = graph.render(filename=file_name)
        else:
            grid = chart.calc_layout_data(obj)
            svg = chart.grid_to_svg(grid)
            svg_file_path = "%s.svg" % file_name
            with open(svg_file_path, 'w') as f:
                f.write(svg)
        lines.append('.. image:: /{}'.format(svg_file_path))
        lines.append('   :target: /{}'.format(svg_file_path))
    return lines


def setup(app):
    app.connect('autodoc-process-docstring', process_flows)
    return {'version': version, 'parallel_read_safe': True}
