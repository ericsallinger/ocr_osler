from django.contrib import admin
from django import forms

from .models import File_upload
from django.contrib import messages
from django.utils.translation import ngettext
from django.template.defaultfilters import slugify
import os
from PIL import Image, ImageFilter
import tesserocr
from pdf2image import convert_from_path


@admin.register(File_upload)
class File_uploadAdmin(admin.ModelAdmin):
    exclude = ['name']
    # exclude = ['fileUpload']
     # allow for multiple file uploads
    def save_model(self, request, obj, form, change):
        obj.save()
        files = request.FILES.getlist('photos_multiple')
        print(File_upload.objects.all())
        File_upload.objects.filter(slug='file_upload').delete()

        
        for afile in files:
            # obj.uploadedFile.create(uploadedFile=afile)
            instance = File_upload(uploadedFile=afile)
            instance.name = afile
            instance.slug = slugify(afile)
            instance.save()

    #calls tesserocr and prints to shell. also changes the stauts of file model to 'completedocr'
    #currently only supports images (Not pdfs)
    def run_ocr(self, request, queryset):
        for File_upload in queryset:
            fileCounter = 1
           
            filePath = str(File_upload.uploadedFile)
            path, fileName = os.path.split(filePath)
            bareName, extension = os.path.splitext(fileName)

            #prepare to save file in output directory
            os.chdir("ocr_osler/file_uploads/scannedText/")
            outputFile = File_upload.slug+".txt"
            file = open(outputFile, "w")

            #check if you need to convert to pdf
            if isImageFile(filePath):
                readFile = Image.open(File_upload.uploadedFile)
                file.write(tesserocr.image_to_text(readFile))
                file.close
                           
            else:
                # readFile = Image.open(convertToImage(filePath))       
                print("not an image")
            os. chdir("../../..")

        # alert user to status of action   
        updated = queryset.update(ocrStatusChoice='completedocr')
        self.message_user(request, ngettext(
            '%d story was successfully sent to OCR module.',
            '%d stories were successfully sent to OCR module.',
            updated,
        ) % updated, messages.SUCCESS)
    
    run_ocr.short_description = "Run OCR on selected files"
    
    actions = [run_ocr]
    list_display = ('name', 'slug', 'ocrStatusChoice')

#helper methods

def isImageFile(filePath):
    imageFileExtensions = ['.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.gif']
    basename, extension = os.path.splitext(filePath)
    if extension.lower() in imageFileExtensions:
        return True
    else:
        return False

def convertToImage(filePath):
    convertedImage = convert_from_path(filePath, 500)
    basename, extension = os.path.splitext(filePath)
    newPath = basename + ".jpg"
    return convertedImage.save(newPath, 'JPEG')

