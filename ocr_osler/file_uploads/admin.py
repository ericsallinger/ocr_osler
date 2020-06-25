from django.contrib import admin

from .models import File_upload
from django.contrib import messages
from django.utils.translation import ngettext
import os
from PIL import Image, ImageFilter
import tesserocr
from pdf2image import convert_from_path



@admin.register(File_upload)
class File_uploadAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'ocrStatusChoice')
    
  

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
            outputFile = bareName+".txt"
            file = open(outputFile, "w")

            #check if you need to convert to pdf
            if isImageFile(filePath):
                readFile = Image.open(File_upload.uploadedFile)
                file.write(tesserocr.image_to_text(readFile))
                file.close
                os. chdir("../../..")           
            else:
                readFile = Image.open(convertToImage(filePath))       
                print(tesserocr.image_to_text(readFile))

        # alert user to status of action   
        updated = queryset.update(ocrStatusChoice='completedocr')
        self.message_user(request, ngettext(
            '%d story was successfully sent to OCR module.',
            '%d stories were successfully sent to OCR module.',
            updated,
        ) % updated, messages.SUCCESS)
    run_ocr.short_description = "Run OCR on selected files"
    
    actions = [run_ocr]

#helper methods

def isImageFile(filePath):
    imageFileExtensions = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif']
    basename, extension = os.path.splitext(filePath)
    if extension.lower() in imageFileExtensions:
        return True
    else:
        return False

def convertToImage(filePath):
    convertedImage = convert_from_path(filePath, 500)
    print("made it")
    basename, extension = os.path.splitext(filePath)
    newPath = basename + ".jpg"
    return convertedImage.save(newPath, 'JPEG')

