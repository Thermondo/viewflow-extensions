import pytest
from viewflow.test import FlowTest

from .testapp.flows import SavableFlow


class TestSavableViewActivationMixin:

    @pytest.mark.django_db
    def test_save(self, admin_user):
        with FlowTest(SavableFlow, namespace='savable') as flow:
            start_process(flow)
            save_savable_task(flow, admin_user, post_kwargs={'text': 'asdf'})

    @pytest.mark.django_db
    def test_default_behavior(self, admin_user):
        with FlowTest(SavableFlow, namespace='savable') as flow:
            start_process(flow)
            execute_savable_task(flow, {'text': 'asdf'})

    @pytest.mark.django_db
    def test_save_empty_field(self, admin_user):
        with FlowTest(SavableFlow, namespace='savable') as flow:
            start_process(flow)
            save_savable_task(flow, admin_user, post_kwargs={'text': ''})

    @pytest.mark.django_db
    def test_done_empty_field_should_fail(self, admin_user):
        with FlowTest(SavableFlow, namespace='savable') as flow:
            start_process(flow)
            with pytest.raises(AssertionError):
                execute_savable_task(flow, {'text': ''})


def start_process(flow):
    flow.Task(SavableFlow.start).User('admin').Execute() \
        .Assert(lambda p: p.created is not None, 'Process did not start.')


def save_savable_task(flow, admin_user, post_kwargs):
    process = SavableFlow.process_class.objects.get()
    task = process.active_tasks().first()
    url_args = flow.Task(SavableFlow.savable_task).url_args.copy()
    task_url = SavableFlow.savable_task.get_task_url(
        url_type='execute', task=task, user=admin_user, namespace='savable', **url_args)
    form = flow.app.get(task_url, user=admin_user).form

    for key, value in post_kwargs.items():
        form[key] = value

    form.submit('_save').follow()

    process.refresh_from_db()
    assert not process.finished, 'The process is finished.'
    assert process.text == post_kwargs['text'], 'Text was not saved.'


def execute_savable_task(flow, post_kwargs):
    flow.Task(SavableFlow.savable_task).User('admin').Execute(post_kwargs) \
        .Assert(lambda p: p.finished, 'Process is not finished.')
