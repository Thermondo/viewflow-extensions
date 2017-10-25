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

    _save = False

    def post(self, request, *args, **kwargs):
        self._save = True if '_save' in request.POST else False
        return super().post(request, *args, **kwargs)

    def get_form_class(self):
        """If the task was only saved, treat all form fields as not required."""
        form_class = super().get_form_class()
        if self._save:
            for field in form_class.base_fields.values():
                field.required = False
        return form_class

    def save_task(self):
        """Transition to save the task and return to ``ASSIGNED`` state."""
        task = self.request.activation.task
        task.status = STATUS.ASSIGNED
        task.save()

    def activation_done(self, *args, **kwargs):
        """Complete the ``activation`` or save only, depending on form submit."""
        if self._save:
            self.save_task()
        else:
            super().activation_done(*args, **kwargs)

    def get_success_url(self):
        """Stay at the same page, if the task was only saved."""
        if self._save:
            return self.request.get_full_path()
        return super().get_success_url()
