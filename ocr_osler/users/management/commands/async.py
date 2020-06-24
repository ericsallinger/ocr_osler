from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Runs task asynchrously'

    def handle(self, *args, **kwargs):
        self.stdout.write("Hi")
