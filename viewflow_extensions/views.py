"""
Views for view nodes that add additional behavior.

.. inheritance-diagram:: viewflow_extensions.views
    :parts: 1
"""
from viewflow.activation import STATUS


class SavableViewActivationMixin:
    """
    Add save option to `.viewflow.flow.ManagedViewActivation`.

    Usage::

        from viewflow.flow.views import UpdateProcessView

        class MyCustomView(SavableViewMixin, UpdateProcessView):
            pass

    All you have to do is to add a new submit button with the name
    ``_save`` to your template.

    Template example::

        <button type="submit" name="_save">
          {% trans 'Save' %}
        </button>

    """

    def save_task(self):
        """Transition to save the task and return to ``ASSIGNED`` state."""
        task = self.request.activation.task
        task.status = STATUS.ASSIGNED
        task.save()

    def activation_done(self, *args, **kwargs):
        """Complete the ``activation`` or save only, depending on form submit."""
        if '_save' in self.request.POST:
            self.save_task()
        else:
            super().activation_done(*args, **kwargs)

    def get_success_url(self):
        """Stay at the same page, if the task was only saved."""
        if '_save' in self.request.POST:
            return self.request.get_full_path()
        return super().get_success_url()
