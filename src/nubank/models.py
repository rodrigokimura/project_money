import uuid

from django.db import models
from django.utils import timezone


class EventCategory(models.Model):
    name = models.TextField(primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = "Event Categories"

    def event_count(self):
        return Event.objects.filter(category=self).count()

    def __str__(self):
        return str(self.name)


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    data = models.JSONField()

    @classmethod
    def transactions(cls):
        return cls.objects.filter(category="transaction")


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class TransactionCategory(models.Model):
    name = models.TextField(primary_key=True, editable=False)

    class Meta:
        verbose_name_plural = "Transaction Categories"

    def transaction_count(self):
        return Transaction.objects.filter(category=self).count()

    def amount_last_month(self):
        n = timezone.now()

        return (
            Transaction.objects.filter(
                category=self, timestamp__month=n.month, timestamp__year=n.year
            )
            .aggregate(models.Sum("amount"))
            .get("amount__sum")
        )

    def __str__(self):
        return str(self.name)


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    timestamp = models.DateTimeField()
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    source = models.TextField(null=True)
    details = models.JSONField()
