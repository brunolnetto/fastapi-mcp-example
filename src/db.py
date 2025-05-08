from src.models import Ticket
from datetime import datetime
from typing import List

tickets: List[Ticket] = []
ticket_counter = 1

def create_ticket(title: str, description: str) -> Ticket:
    global ticket_counter
    now = datetime.now()
    ticket = Ticket(
        id=ticket_counter,
        title=title,
        description=description,
        created_at=now,
        updated_at=now
    )
    tickets.append(ticket)
    ticket_counter += 1
    return ticket

def list_tickets() -> List[Ticket]:
    return tickets

def get_ticket(ticket_id: int) -> Ticket:
    return next(t for t in tickets if t.id == ticket_id)

def update_status(ticket_id: int, status: str) -> Ticket:
    ticket = get_ticket(ticket_id)
    ticket.status = status
    ticket.updated_at = datetime.now()
    return ticket

def delete_ticket(ticket_id: int) -> Ticket:
    global tickets
    ticket = get_ticket(ticket_id)
    tickets = [t for t in tickets if t.id != ticket_id]
    return ticket