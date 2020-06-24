from django.contrib import admin

from .models import File_upload
from django.contrib import messages
from django.utils.translation import ngettext
from PIL import Image, ImageFilter
import tesserocr



@admin.register(File_upload)
class File_uploadAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'ocrStatusChoice')
    
    #calls tesserocr and prints to shell. also changes the stauts of file model to 'completedocr'
    #currently only supports images (Not pdfs)
    def run_ocr(self, request, queryset):
        for File_upload in queryset:
            readFile = Image.open(File_upload.uploadedFile)
            # readFile.show()
            print(tesserocr.image_to_text(readFile))

        updated = queryset.update(ocrStatusChoice='completedocr')
        self.message_user(request, ngettext(
            '%d story was successfully sent to OCR module.',
            '%d stories were successfully sent to OCR module.',
            updated,
        ) % updated, messages.SUCCESS)
    run_ocr.short_description = "Run OCR on selected files"
    
    actions = [run_ocr]

