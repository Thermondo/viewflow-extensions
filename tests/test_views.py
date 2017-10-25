import pytest
from viewflow.test import FlowTest

from .testapp.flows import SavableFlow


class TestSavableViewActivationMixin:

    @staticmethod
    def attempt_save(admin_user, post_kwargs):
        with FlowTest(SavableFlow, namespace='savable') as flow:
            flow.Task(SavableFlow.start).User('admin').Execute() \
                .Assert(lambda p: p.created is not None, 'Process did not start.')

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

    @pytest.mark.django_db
    def test_save(self, admin_user):
        self.attempt_save(admin_user, post_kwargs={'text': 'asdf'})

    @pytest.mark.django_db
    def test_default_behavior(self, admin_user):
        with FlowTest(SavableFlow, namespace='savable') as flow:
            flow.Task(SavableFlow.start).User('admin').Execute() \
                .Assert(lambda p: p.created is not None, 'Process did not start.')
            flow.Task(SavableFlow.savable_task).User('admin').Execute({'text': 'asdf',}) \
                .Assert(lambda p: p.finished, 'Process is not finished.')

    @pytest.mark.django_db
    def test_save_empty_field(self, admin_user):
        self.attempt_save(admin_user, post_kwargs={'text': ''})

    @pytest.mark.django_db
    def test_done_empty_field_should_fail(self, admin_user):
        with FlowTest(SavableFlow, namespace='savable') as flow:
            flow.Task(SavableFlow.start).User('admin').Execute() \
                .Assert(lambda p: p.created is not None, 'Process did not start.')
            with pytest.raises(AssertionError):
                flow.Task(SavableFlow.savable_task).User('admin').Execute({'text': '',}) \
                    .Assert(lambda p: p.finished, 'Process is not finished.')
