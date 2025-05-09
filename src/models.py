from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# Ticket Status Enum
class TicketStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    PENDING = "pending"

# === Request Models ===
class TicketCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1, max_length=500)

class BaseTicket(BaseModel):
    id: int
    title: str
    description: str
    status: TicketStatus = TicketStatus.OPEN
    created_at: datetime
    updated_at: Optional[datetime] = None

class Ticket(BaseTicket):
    created_at: datetime
    updated_at: Optional[datetime] = None

# === Request Models ===
class UpdateStatusRequest(BaseTicket):
    ...
