from viewflow_extensions.test import ActivationFactory

from .testapp.flows import SavableFlow


def test_sth():
    factory = ActivationFactory(SavableFlow)
    activation = factory.savable_task
    assert activation == ''
