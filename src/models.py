from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class TicketStatus(str):
    OPEN = "open"
    CLOSED = "closed"
    PENDING = "pending"

class TicketCreate(BaseModel):
    title: str
    description: str

class Ticket(BaseModel):
    id: int
    title: str
    description: str
    status: Literal["open", "pending", "closed"] = "open"
    created_at: datetime
    updated_at: datetime
