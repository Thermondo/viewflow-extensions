# -*- coding: utf-8 -*-
import datetime
import importlib
import inspect
import sys

import os

import django

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

year = datetime.datetime.now().strftime("%Y")

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.testapp.settings")
django.setup()

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('../tests.testapp'))
sys.path.insert(0, os.path.abspath('..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.intersphinx',
    'sphinx.ext.linkcode',
    'sphinxcontrib.spelling',
]


def linkcode_resolve(domain, info):
    """Link source code to GitHub."""
    project = 'viewflow-extensions'
    github_user = 'Thermondo'
    head = 'master'

    if domain != 'py' or not info['module']:
        return None
    filename = info['module'].replace('.', '/')
    mod = importlib.import_module(info['module'])
    basename = os.path.splitext(mod.__file__)[0]
    if basename.endswith('__init__'):
        filename += '/__init__'
    item = mod
    lineno = ''
    for piece in info['fullname'].split('.'):
        item = getattr(item, piece)
        try:
            lineno = '#L%d' % inspect.getsourcelines(item)[1]
        except (TypeError, IOError):
            pass
    return ("https://github.com/%s/%s/blob/%s/%s.py%s" %
            (github_user, project, head, filename, lineno))


intersphinx_mapping = {
    'python': ('http://docs.python.org/3.5', None),
    'django': ('https://docs.djangoproject.com/en/stable/',
               'https://docs.djangoproject.com/en/stable/_objects/'),
    'viewflow': ('https://viewflow.readthedocs.io/en/latest/', None),
}

# spell check
spelling_word_list_filename = 'spelling_wordlist.txt'
spelling_show_suggestions = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

master_doc = 'index'

project = 'Viewflow Extensions'
copyright = '%s, Thermondo GmbH' % year

exclude_patterns = ['_build']

pygments_style = 'sphinx'


def skip(app, what, name, obj, skip, options):
    if name == "__init__" and obj.__doc__:
        return False
    return skip


def setup(app):
    app.connect("autodoc-skip-member", skip)


autodoc_default_flags = ['members', 'show-inheritance']
autodoc_member_order = 'bysource'

inheritance_graph_attrs = dict(rankdir='TB')

inheritance_node_attrs = dict(shape='rect', fontsize=14, fillcolor='gray90',
                              color='gray30', style='filled')

inheritance_edge_attrs = dict(penwidth=0.75)

if on_rtd:
    html_theme = 'default'
else:
    html_theme = 'sphinx_rtd_theme'
