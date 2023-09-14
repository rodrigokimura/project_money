from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CardStatement(BaseModel):
    description: str
    category: str
    amount: int
    time: datetime
    source: str
    title: str
    amount_without_iof: int
    account: UUID
    details: Details
    id: UUID
    tokenized: bool
    href: str


class Details(BaseModel):
    status: str
    subcategory: str
