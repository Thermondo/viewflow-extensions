from django.utils.timezone import now
from viewflow import signals
from viewflow.activation import Activation, STATUS, all_leading_canceled


class ActivationFactory:

    def __init__(self, flow_cls):
        self.flow_cls = flow_cls

    def __getattribute__(self, item):
        flow_cls = super().__getattribute__('flow_cls')

        try:
            node = getattr(flow_cls, item)
            activation_class = node.activation_class

            class activation(activation_class):
                @Activation.status.transition(source=STATUS.PREPARED, target=STATUS.DONE)
                def done(self):
                    self.task.process = self.process
                    self.task.finished = now()
                    signals.task_finished.send(sender=self.flow_class, process=self.process, task=self.task)

                @Activation.status.transition(source=STATUS.DONE, conditions=[all_leading_canceled])
                def activate_next(self):
                    """Activate all outgoing edges."""
                    pass

                @Activation.status.transition(source=STATUS.UNRIPE)
                def initialize(self, flow_task, task):
                    """Initialize the activation instance."""
                    self.flow_task, flow_class = flow_task, flow_task.flow_class

                    self.process = flow_class.process_class(flow_class=flow_class)
                    self.task = task

                @classmethod
                def activate(cls, flow_task, task_model):
                    """Instantiate new task."""
                    task = task_model()

                    activation = cls()
                    activation.initialize(flow_task, task)

                    return activation

            return activation.activate(node, flow_cls.task_class)

        except AttributeError:
            return super().__getattribute__(item)
