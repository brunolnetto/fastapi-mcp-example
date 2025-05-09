from src.models import Ticket, TicketStatus
from datetime import datetime
from typing import List, Optional

# In-memory store for tickets
tickets: List[Ticket] = []
ticket_counter = 0

def create_ticket(title: str, description: str) -> Ticket:
    """
    Create a new ticket with the provided title and description, and assign it a unique ID.
    The created_at and updated_at fields are set to the current datetime.

    Args:
        title (str): The title of the ticket.
        description (str): The description of the ticket.

    Returns:
        Ticket: The created ticket object.
    """
    global ticket_counter
    now = datetime.now()
    
    # Create the ticket object
    ticket = Ticket(
        id=ticket_counter,
        title=title,
        description=description,
        status=TicketStatus.OPEN,  # Default status is 'open'
        created_at=now,
        updated_at=now
    )

    # Add to in-memory ticket list
    tickets.append(ticket)
    ticket_counter += 1

    # Verbose output for debugging
    print(f"Ticket Created: {ticket}")
    print(f"Current Ticket List: {tickets}")

    return ticket

def list_tickets() -> List[Ticket]:
    """
    List all the tickets in the system.

    Returns:
        List[Ticket]: A list of all tickets.
    """
    print(f"Listing {len(tickets)} ticket(s).")
    return tickets

def get_ticket(ticket_id: int) -> Optional[Ticket]:
    """
    Retrieve a ticket by its unique ID.

    Args:
        ticket_id (int): The ID of the ticket to retrieve.

    Returns:
        Ticket: The ticket if found.
        
    Raises:
        ValueError: If the ticket with the provided ID does not exist.
    """
    try:
        ticket = next(t for t in tickets if t.id == ticket_id)
        print(f"Ticket Retrieved: {ticket}")
        return ticket
    except StopIteration:
        raise ValueError(f"Ticket with ID {ticket_id} not found.")

def update_status(ticket_id: int, status: str) -> Ticket:
    """
    Update the status of an existing ticket.

    Args:
        ticket_id (int): The ID of the ticket to update.
        status (str): The new status to set.

    Returns:
        Ticket: The updated ticket.
        
    Raises:
        ValueError: If the provided status is invalid.
    """
    if status not in TicketStatus._value2member_map_:
        raise ValueError(f"Invalid status '{status}'. Valid statuses are {', '.join([s.value for s in TicketStatus])}.")
    
    ticket = get_ticket(ticket_id)
    
    # Update ticket status and timestamp
    ticket.status = status
    ticket.updated_at = datetime.now()

    print(f"Ticket Status Updated: {ticket}")
    return ticket

def delete_ticket(ticket_id: int) -> Ticket:
    """
    Delete a ticket by its unique ID.

    Args:
        ticket_id (int): The ID of the ticket to delete.

    Returns:
        Ticket: The deleted ticket object.
        
    Raises:
        ValueError: If the ticket with the provided ID does not exist.
    """
    ticket = get_ticket(ticket_id)
    
    # Remove the ticket from the list
    global tickets
    tickets = [t for t in tickets if t.id != ticket_id]

    print(f"Ticket Deleted: {ticket}")
    print(f"Current Ticket List: {tickets}")

    return ticket
