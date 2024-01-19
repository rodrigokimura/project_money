from django.core.management.base import BaseCommand, CommandError

from ...models import Account, Event, Transaction


class Command(BaseCommand):
    def handle(self, *args, **options):
        p = self.stdout.write
        p("Erasing tables...")
        Transaction.objects.all().delete()
        Account.objects.all().delete()
        Event.objects.all().delete()
