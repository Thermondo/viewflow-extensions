import os
import tempfile
from io import StringIO

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError


class TestFlowGraph:
    flow_path = 'tests.testapp.flows.TestFlow'

    def test_create_default(self):
        with StringIO() as stdout:
            call_command('flow_graph', self.flow_path, stdout=stdout)
            stdout.seek(0)
            graph = stdout.read()
        assert '<svg xmlns="http://www.w3.org/2000/svg" ' in graph

    def test_svg(self):
        with StringIO() as stdout:
            call_command('flow_graph', '--type=svg', self.flow_path, stdout=stdout)
            stdout.seek(0)
            graph = stdout.read()
        assert '<svg xmlns="http://www.w3.org/2000/svg" ' in graph

    def test_bpmn(self):
        with StringIO() as stdout:
            call_command('flow_graph', '--type=bpmn', self.flow_path, stdout=stdout)
            stdout.seek(0)
            graph = stdout.read()
        assert '<?xml version="1.0" encoding="UTF-8"?>\n<bpmn:definitions' in graph

    def test_output(self):
        file_name = os.path.join(tempfile.mkdtemp(), 'test.svg')
        with StringIO() as stdout:
            call_command('flow_graph', '--output=%s' % file_name, self.flow_path, stdout=stdout)
            stdout.seek(0)
            graph = stdout.read()
        assert graph == ''
        assert os.path.exists(file_name)
        with open(file_name) as fs:
            graph = fs.read()
        assert '<svg xmlns="http://www.w3.org/2000/svg" ' in graph

    def test_create_graph_wrong_name(self):
        """Test exceptions"""
        with pytest.raises(CommandError):
            call_command('flow_graph', "wrong_path.TestFlow")

        with pytest.raises(CommandError):
            call_command('flow_graph', "tests.testapp.flows.WrongFlow")

        with pytest.raises(CommandError):
            call_command('flow_graph', "wrong_path")

        with pytest.raises(CommandError):
            call_command('flow_graph', "--type='does-not-exist'")
