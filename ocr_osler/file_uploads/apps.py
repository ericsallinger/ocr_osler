from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class File_UploadConfig(AppConfig):
    name = "ocr_osler.file_uploads"
    verbose_name = _("File_Uploads")
