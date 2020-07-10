from django.core.management.base import BaseCommand
from file_uploads.models.py import ocrStatusChoice
from multiprocessing import Process
# Handles two tasks, recieve_image and return_message. To avoid task queue of
# OCR taking too long and resulting in a timeout, we
# return a message asynchrously


class Command(BaseCommand):
    help = 'Runs task asynchrously'
    test = False
    def handle(self, *args, **kwargs):
        def runOCR():
            test = True
            time.sleep(60)
            test = False

            #while true:
                #if (ocrStatusChoice == "AwaitingOCR"):
                #    test = True
                #    time.sleep(60)
                #    test = False

        def update():
            while test is True:
                self.stdout.write("OCR is processing")
        if __name__ == '__main__':
            Process(target=runOCR).start()
            Process(target=update).start()
