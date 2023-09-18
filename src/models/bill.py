from datetime import date
from typing import Any
from uuid import UUID

from pydantic import BaseModel


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
