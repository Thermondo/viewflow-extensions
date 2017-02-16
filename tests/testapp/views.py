from viewflow.flow.views import UpdateProcessView

from viewflow_extensions.views import SavableViewActivationMixin


class SavableProcessView(SavableViewActivationMixin, UpdateProcessView):
    fields = ['text']
