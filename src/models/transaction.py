from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


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
