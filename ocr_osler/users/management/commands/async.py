from django.core.management.base import BaseCommand

# Handles two tasks, recieve_image and return_message. To avoid task queue of
# OCR taking too long and resulting in a timeout, we
# return a message asynchrously


class Command(BaseCommand):
    help = 'Runs task asynchrously'

    def handle(self, *args, **kwargs):
        self.stdout.write("Hi")
