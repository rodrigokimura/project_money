from __future__ import annotations

import json
from datetime import date, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel
from pynubank import Nubank

from config import Config


class Summary(BaseModel):
    due_date: date
    effective_due_date: date
    close_date: date
    open_date: date
    total_balance: float


class Bill(BaseModel):
    id: UUID | None = None
    state: str
    summary: Summary
    link: str | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]):
        data["link"] = data.get("_links", {}).get("self", {}).get("href")
        return cls(**data)


class Transaction(BaseModel):
    description: str
    amount: float
    time: datetime
    source: str | None = None
    title: str
    amount_without_iof: int | None = None
    account: UUID | None = None
    details: Details
    id: UUID
    tokenized: bool = False
    href: str

    def __hash__(self):
        return self.id.__hash__()

    @classmethod
    def from_api(cls, data: dict[str, Any]):
        instance = cls(**data)
        instance.amount /= 100
        return instance


class Details(BaseModel):
    subcategory: str
    status: str | None = None


class Client:
    def __init__(self) -> None:
        self.nubank = Nubank()
        settings = Config()
        self.nubank.authenticate_with_cert(settings.cpf, settings.password, "cert.p12")
        self.card_feed: dict[str, Any] = {}
        self.transactions: list[Transaction] = []
        self.bills: list[Bill] = []

    def load_card_feed(self):
        self.card_feed: dict[str, Any] = self.nubank.get_card_feed()

    def export_card_feed(self):
        with open("card_feed.json", mode="w") as f:
            json.dump(self.card_feed, f)

    def read_card_feed_from_file(self) -> dict[str, Any]:
        with open("card_feed.json", mode="r") as f:
            return json.load(f)

    def get_transactions(self):
        if not self.transactions:
            self.load_transactions()
        return self.transactions

    def load_bills(self):
        self.bills = [Bill.from_api(b) for b in self.nubank.get_bills()]

    def get_bill_details(self, id: UUID):
        if not self.bills:
            self.load_bills()
        link = next(b.link for b in self.bills if b.id == id)
        return self.nubank.get_bill_details({"_links": {"self": {"href": link}}})

    def load_transactions(self):
        self.transactions = [
            Transaction.from_api(event)
            for event in self.card_feed.get("events", [])
            if event.get("category") == "transaction"
        ]
