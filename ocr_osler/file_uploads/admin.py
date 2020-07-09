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
            else:
                instance = File_upload(uploadedFile=afile)
                instance.name = afile
                instance.slug = slugify(afile)
            instance.uploadedBy = str(request.user)
            instance.save('ocr_osler/file_uploads/unscannedfiles')
            cleanFile(instance)
        

    def getDir(self, request, queryset):
        print(os.getcwd())

    def run_ocr(self, request, queryset):
        successfulCount=0
        errorCount=0

        for File_upload in queryset:  # create txt file and write ocr output to it
            File_upload.ocrStatusChoice = "completedocr"
            print(File_upload.ocrStatusChoice)
            readFile = Image.open(File_upload.uploadedFile)
            outputFile = "ocr_osler/file_uploads/scannedText/"+File_upload.slug+".txt"
            file = open(outputFile, "w")            
            file.write(tesserocr.image_to_text(readFile))
            file.close
            successfulCount += 1
 
        if successfulCount >= 1:  # alert user to status of action
            self.message_user(request, ngettext(
                '%d file was successfully sent to OCR module.',
                '%d files were successfully sent to OCR module.',
                successfulCount,
            ) % successfulCount, messages.SUCCESS)
        else:
            self.message_user(request, ngettext(
                '%d file could not be sent to OCR, check to make sure it is an image file.',
                '%d files could not be sent to OCR, check to make sure they are image files.',
                errorCount
            ) % errorCount, messages.ERROR)
    
    run_ocr.short_description = "Run OCR on selected files"

    actions = [run_ocr, getDir]
    list_display = ('name', 'slug', 'ocrStatusChoice', 'uploadedBy')


###helper methods

#checks if file extension is in the list compatible with tesserocr
imageFileExtensions = ['.png', '.jpg', '.jpeg', '.tiff', '.tif', '.bmp', '.gif']
def isImageFile(filePath):
    basename, extension = os.path.splitext(filePath)
    if extension.lower() in imageFileExtensions:
        return True
    else:
        return False

def cleanFile(fileUploadObj):
    fileObj = fileUploadObj.uploadedFile
    if hasattr(fileObj, "tag_v2[700]"):
        del fileObj.tag_v2[34377]
        del fileObj.tag_v2[700]


#converts pdf file to jpg and saved it to correct directory
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
