from fastapi import FastAPI, Depends, HTTPException
from fastapi_mcp import FastApiMCP
from typing import List

from src.models import TicketCreate, Ticket
from src.db import create_ticket, list_tickets, get_ticket, update_status, delete_ticket
from src.auth import get_current_user

app = FastAPI(title="Support API", description="Ticketing system", version="1.0")
@app.post("/tickets", response_model=Ticket, operation_id="create_support_ticket")
def api_create_ticket(
    payload: TicketCreate,
    user: dict = Depends(get_current_user)
):
    return create_ticket(payload.title, payload.description)

@app.get("/tickets", response_model=List[Ticket], operation_id="list_support_tickets")
def api_list_tickets(user: dict = Depends(get_current_user)):
    return list_tickets()

@app.get("/tickets/{ticket_id}", response_model=Ticket, operation_id="get_ticket_by_id")
def api_get_ticket(ticket_id: int, user: dict = Depends(get_current_user)):
    return get_ticket(ticket_id)

@app.put("/tickets/{ticket_id}/status", response_model=Ticket, operation_id="update_ticket_status")
def api_update_ticket_status(ticket_id: int, status: str, user: dict = Depends(get_current_user)):
    if status not in ["open", "closed", "pending"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    return update_status(ticket_id, status)

@app.delete("/tickets/{ticket_id}", response_model=Ticket, operation_id="delete_ticket")
def api_delete_ticket(ticket_id: int, user: dict = Depends(get_current_user)):
    return delete_ticket(ticket_id)

# Expose only select endpoints via MCP
mcp = FastApiMCP(
    app,
    describe_all_responses=True,  # Include all possible response schemas
    describe_full_response_schema=True  # Include full JSON schema in descriptions
)
mcp.mount()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
