from django.conf.urls import include, url
from viewflow.flow.viewset import FlowViewSet

from . import flows

urlpatterns = [
    url(r'^savable-flow/', include((FlowViewSet(flows.SavableFlow).urls, 'testapp'),
                                   namespace='savable')),
]
