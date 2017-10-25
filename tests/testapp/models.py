from django.db import models
from viewflow.models import Process


class SavableProcess(Process):
    text = models.TextField()
