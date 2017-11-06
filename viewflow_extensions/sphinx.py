"""
Sphinx extension to automatically render BPMN graphs of Flows.

To enable this feature simply add ``viewflow_extensions.sphinx`` to your Sphinx configuration.

Example::

    extensions = [
        'sphinx.ext.autodoc',
        # ...
        'viewflow_extensions.sphinx',
    ]

"""
import inspect
import os
from tempfile import mkdtemp

from viewflow import chart
from viewflow.base import Flow

from . import __version__ as version


def process_flows(app, what, name, obj, options, lines):
    if inspect.isclass(obj) and issubclass(obj, Flow):
        tmp_dir = mkdtemp()
        file_name = "%s.svg" % obj._meta.flow_label
        svg_file_path = os.path.join(tmp_dir, file_name)

        grid = chart.calc_layout_data(obj)
        svg = chart.grid_to_svg(grid)
        with open(svg_file_path, 'w') as f:
            f.write(svg)
        lines.append('.. image:: /{}'.format(svg_file_path))
        lines.append('   :alt: {} flow graph'.format(obj._meta.flow_label))
        lines.append('   :target: /_images/{}'.format(file_name))
    return lines


def setup(app):
    app.connect('autodoc-process-docstring', process_flows)
    return {'version': version, 'parallel_read_safe': True}
