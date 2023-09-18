from datetime import datetime
from typing import Any
from uuid import UUID

import pandas as pd
from pynubank import Nubank

from config import Config
from models.bill import Bill
from models.transaction import Transaction


class Client:
    def __init__(self) -> None:
        self.nubank = Nubank()
        settings = Config()
        self.nubank.authenticate_with_cert(settings.cpf, settings.password, "cert.p12")
        self.card_feed: dict[str, Any] = self.nubank.get_card_feed()
        self.transactions: list[Transaction] = []
        self.bills: list[Bill] = []

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

    def sum_by_amount(self, date_range: tuple[datetime, datetime] | None = None):
        df = pd.DataFrame([s.__dict__ for s in self.transactions])
        if date_range:
            start, end = date_range
            df = df[(df["time"] > start.isoformat()) & (df["time"] < end.isoformat())]
        df = df.groupby(["title"]).sum(numeric_only=True)
        return df["amount"]
