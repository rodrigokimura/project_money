from .client import Client
from .models import Account, Event, EventCategory, Transaction, TransactionCategory


def sync(call_service: bool = True):
    print("Staring import process...")
    c = Client()

    if call_service:
        print("Loading card feed...")
        c.load_card_feed()
        print("Exporting card feed...")
        c.export_card_feed()
        card_feed = c.card_feed
    else:
        print("Reading events...")
        card_feed = c.read_card_feed_from_file()

    print("Erasing events...")
    EventCategory.objects.all().delete()
    Event.objects.all().delete()

    print("Recreating event categories...")
    categories = {e.get("category") for e in card_feed.get("events", [])}
    categories = [EventCategory(name=c) for c in categories]
    EventCategory.objects.bulk_create(
        categories,
        update_conflicts=False,
        unique_fields=["name"],
    )

    print("Recreating events...")
    events = [
        Event(
            id=e.pop("id"),
            category=EventCategory(name=e.pop("category")),
            data=e,
        )
        for e in card_feed.get("events", [])
    ]

    Event.objects.bulk_create(
        events,
        update_conflicts=True,
        unique_fields=["id"],
        update_fields=["data"],
    )


def process():
    transactions = Event.transactions()
    print(transactions.count())

    print("Erasing tables...")
    Account.objects.all().delete()
    Transaction.objects.all().delete()
    TransactionCategory.objects.all().delete()

    print("Creating accounts...")
    accounts = {t.data.get("account") for t in transactions}
    accounts = [Account(id=a) for a in accounts if a]
    Account.objects.bulk_create(
        accounts,
        update_conflicts=False,
        unique_fields=["id"],
    )
    print("Creating categories...")
    categories = {t.data.get("title", "").lower() for t in transactions}
    categories = [TransactionCategory(name=c) for c in categories if c]
    TransactionCategory.objects.bulk_create(
        categories,
        update_conflicts=False,
        unique_fields=["name"],
    )

    print("Creating transactions...")
    transactions = [
        Transaction(
            id=t.id,
            event=Event.objects.get(id=t.id),
            account=Account.objects.filter(id=t.data.get("account")).first(),
            description=t.data.get("description"),
            timestamp=t.data.get("time"),
            amount=t.data.get("amount", 0) / 100,
            category=TransactionCategory(name=t.data.get("title", "").lower()),
            source=t.data.get("source"),
            details=t.data.get("details"),
        )
        for t in transactions
    ]
    Transaction.objects.bulk_create(
        transactions,
        update_conflicts=False,
        unique_fields=["id"],
    )
