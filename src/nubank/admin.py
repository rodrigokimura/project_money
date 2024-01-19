from django.contrib import admin

from .models import Account, Event, EventCategory, Transaction, TransactionCategory


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["id", "category"]
    list_filter = ["category"]
    search_fields = ["category"]


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "event_count"]
    list_filter = ["name"]
    search_fields = ["name"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "description",
        "category",
        "amount",
        "timestamp",
    ]
    list_filter = ["category", "timestamp"]
    search_fields = ["category__name", "description"]


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "transaction_count", "amount_last_month"]
    list_filter = ["name"]
    search_fields = ["name"]
