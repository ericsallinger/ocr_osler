from django.db import models

from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel

class Image(TimeStampedModel):
        name = models.CharField("test string", max_length=255)
        slug = AutoSlugField("test slug", unique=True, always_update=False, populate_from="name")