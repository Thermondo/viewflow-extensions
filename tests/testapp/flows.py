from viewflow import flow
from viewflow.base import Flow, this
from viewflow.flow.views import CreateProcessView

from .models import SavableProcess
from .views import SavableProcessView


class SavableFlow(Flow):
    process_class = SavableProcess
    start = flow.Start(CreateProcessView, fields=[]).Next(this.savable_task)
    savable_task = flow.View(SavableProcessView) \
        .Assign(username='admin') \
        .Next(this.end)
    end = flow.End()


class TestFlow(Flow):
    process_class = SavableProcess
    start = flow.Start(CreateProcessView, fields=[]).Next(this.savable_task)
    savable_task = flow.View(SavableProcessView) \
        .Assign(username='admin') \
        .Next(this.if_task)
    if_task = flow.If(1 == 1).Then(this.switch_task).Else(this.end)
    switch_task = flow.Switch().Case(this.end, cond=(1 == 1))
    end = flow.End()
