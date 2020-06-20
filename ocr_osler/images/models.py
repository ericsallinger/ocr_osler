from django.db import models

from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel


# create image objects with ability to change ocr status
class Image(TimeStampedModel):
        name = models.CharField("Image Name", max_length=255)
        slug = AutoSlugField("test slug", unique=True, always_update=False, populate_from="name", primary_key=True)
        imageFile = models.ImageField(upload_to='imagefiles/', default='imagefiles/default.jpg')

        #change ocr status when called to ocr functions
        class OCRStatus(models.TextChoices):
                awaitingOCR = "awaitingocr", "AwaitingOCR" 
                queuedForOCR = "queuedforocr", "QueuedForOCR"
                completedOCR = "completedocr", "CompletedOCR"

        ocrStatusChoice = models.CharField("OCR Status", max_length=20, 
                choices=OCRStatus.choices, default=OCRStatus.awaitingOCR)

        def __str__(self):
             return self.name
  
