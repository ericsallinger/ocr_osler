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
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings


@admin.register(File_upload)
class File_uploadAdmin(admin.ModelAdmin):
    exclude = ['name', 'slug','ocrStatusChoice','uploadedBy']

     # allow for multiple file uploads
    def save_model(self, request, obj, form, change):
        obj.save()
        files = request.FILES.getlist('photos_multiple')
        File_upload.objects.filter(name='undefined').delete()
        for afile in files:
            #save non imagefiles locally so they can be converted to images
            if not isImageFile(str(afile)):
                path = default_storage.save('ocr_osler/file_uploads/unscannedfiles/'+str(afile), ContentFile(afile.read()))
                tmp_file = os.path.join(settings.MEDIA_ROOT, path) 
                convertedPath = convertToImage(str(afile))
                instance = File_upload(uploadedFile="ocr_osler/file_uploads/unscannedfiles/"+convertedPath)
                instance.name = convertedPath
                instance.slug = slugify(convertedPath)
                instance.uploadedBy = str(request.user)
                instance.save('ocr_osler/file_uploads/unscannedfiles')
                print(instance.uploadedFile)
            else:
                instance = File_upload(uploadedFile=afile)
                instance.name = afile
                instance.slug = slugify(afile)
                instance.uploadedBy = str(request.user)
                instance.save('ocr_osler/file_uploads/unscannedfiles')
                print(instance.uploadedFile)

    #calls tesserocr and prints to shell. also changes the stauts of file model to 'completedocr'
    #currently only supports images (Not pdfs)
    def getDir(self, request, queryset):
        print(os.getcwd())
    def run_ocr(self, request, queryset):
        successfulCount=0
        errorCount=0
        for File_upload in queryset:
           
            # filePath = str(File_upload.uploadedFile)
            # path, fileName = os.path.split(filePath)
            # bareName, extension = os.path.splitext(fileName)

            #prepare to save file in output directory
            
            outputFile = "ocr_osler/file_uploads/scannedText/"+File_upload.slug+".txt"
            file = open(outputFile, "w")

            #check if you need to convert to pdf
            # if isImageFile(filePath):
            print(os.getcwd() + 'from the method')  
            readFile = Image.open(File_upload.uploadedFile)
            # os.chdir("ocr_osler/file_uploads/scannedText/")
            file.write(tesserocr.image_to_text(readFile))
            file.close
            successfulCount += 1
                           
            # else:
            #     # os. chdir("../../..")
            #     readFile = Image.open(convertToImage(filePath))       
            #     print("not an image")
            # os.chdir("../../../")

        # alert user to status of action
        if successfulCount > 1:
            self.message_user(request, ngettext(
                '%d file was successfully sent to OCR module.',
                '%d files were successfully sent to OCR module.',
                successfulCount,
            ) % successfulCount, messages.SUCCESS)
        self.message_user(request, ngettext(
            '%d file could not be sent to OCR, check to make sure it is an image file.',
            '%d files could not be sent to OCR, check to make sure they are image files.',
            errorCount
        ) % errorCount, messages.ERROR)
    
    run_ocr.short_description = "Run OCR on selected files"

    actions = [run_ocr, getDir]
    list_display = ('name', 'slug', 'ocrStatusChoice', 'uploadedBy')

#helper methods

def isImageFile(filePath):
    imageFileExtensions = ['.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.gif']
    basename, extension = os.path.splitext(filePath)
    if extension.lower() in imageFileExtensions:
        return True
    else:
        return False


def convertToImage(filePath):
    os.chdir("ocr_osler/file_uploads/unscannedfiles/")
    convertedImages = convert_from_path(filePath, 500)
    basename, extension = os.path.splitext(filePath)
    num=1
    for page in convertedImages:
        newPath = basename + "_" + str(num) + ".jpg"
        page.save(newPath, 'JPEG')
        num += 1
    os.chdir("../../../")
    return newPath
