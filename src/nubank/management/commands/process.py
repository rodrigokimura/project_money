from django.core.management.base import BaseCommand

from ...utils import process


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--call-service", action="store_true")

    def handle(self, *args, **options):
        process()
