from django.db import models

from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel
from django.urls import reverse


# create File objects with ability to change ocr status
class File_upload(TimeStampedModel):
        name = models.CharField("File Name", max_length=255, default='undefined')
        slug = AutoSlugField("File Slug", unique=True, always_update=False, populate_from="name", primary_key=True)
        uploadedFile = models.FileField(
            upload_to='ocr_osler/file_uploads/unscannedfiles/', 
            default='ocr_osler/file_uploads/unscannedfiles/default.jpg'
        )
        uploadedBy = models.CharField("Uploaded By", max_length=255, default='undefined')
        # name = ''
        # slug=  ''
        # uploadedFile = ''
        #change ocr status when called to ocr functions
        class OCRStatus(models.TextChoices):
                awaitingOCR = "awaitingocr", "AwaitingOCR" 
                queuedForOCR = "queuedforocr", "QueuedForOCR"
                completedOCR = "completedocr", "CompletedOCR"

        ocrStatusChoice = models.CharField("OCR Status", max_length=20, 
                choices=OCRStatus.choices, default=OCRStatus.awaitingOCR)


        def changeOcrStatus(self,newStatus):
                self.OCRStatus = newStatus
                return self.OCRStatus


        def __str__(self):
             return self.name
  
        def get_absolute_url(self):
                return reverse(
                        'file_uploads:detail', kwargs={"slug": self.slug}
                )
