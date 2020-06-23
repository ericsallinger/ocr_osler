from django.contrib import admin

from .models import File_upload
from django.contrib import messages
from django.utils.translation import ngettext
from PIL import Image, ImageFilter



@admin.register(File_upload)
class File_uploadAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'ocrStatusChoice')
    
    #currently just changes the stauts of file model to 'completedocr'
    #TODO make this function call the actual OCR methods
    def run_ocr(self, request, queryset):
        updated = queryset.update(ocrStatusChoice='completedocr')

        self.message_user(request, ngettext(
            '%d story was successfully sent to OCR module.',
            '%d stories were successfully sent to OCR module.',
            updated,
        ) % updated, messages.SUCCESS)

    def openFile(self, request, queryset):
        for File_upload in queryset:
            readFile = Image.open(File_upload.uploadedFile)
            readFile.show()

        #todo
            #call a function (dummy for ocr) that manipulates the file(s) in the queryset

    run_ocr.short_description = "Run OCR on selected files"
    actions = [run_ocr,openFile]

