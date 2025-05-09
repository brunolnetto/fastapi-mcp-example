import asyncio
from typing import List
from enum import Enum
import json
from pydantic import BaseModel, Field

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.routing import APIRoute
from fastapi.responses import StreamingResponse
from fastmcp import FastMCP
from mcp.server.sse import SseServerTransport

from src.models import TicketCreate, Ticket
from src.db import create_ticket, list_tickets, get_ticket, update_status, delete_ticket
from src.auth import get_current_user

# === Core App Logic ===
app = FastAPI(title="Support API", description="Ticketing system", version="1.0")


# === Enums ===
class TicketStatus(str, Enum):
    open = "open"
    closed = "closed"
    pending = "pending"

# === Request Models ===
class UpdateStatusRequest(BaseModel):
    status: TicketStatus = Field(..., example="closed")

# === Updated Routes ===
@app.post(
    "/tickets",
    response_model=Ticket,
    operation_id="create_support_ticket",
    summary="Create a new support ticket",
    description="Creates a new support ticket with a title and description. Returns the created ticket."
)
def api_create_ticket(payload: TicketCreate, user: dict = Depends(get_current_user)):
    return create_ticket(payload.title, payload.description)

@app.get(
    "/tickets",
    response_model=List[Ticket],
    operation_id="list_support_tickets",
    summary="List all support tickets",
    description="Retrieves all existing tickets, including their ID, title, status, and description."
)
def api_list_tickets(user: dict = Depends(get_current_user)):
    return list_tickets()

@app.get(
    "/tickets/{ticket_id}",
    response_model=Ticket,
    operation_id="get_ticket_by_id",
    summary="Retrieve a support ticket by ID",
    description="Fetches a ticket using its ID. Returns the full details of the ticket."
)
def api_get_ticket(ticket_id: int, user: dict = Depends(get_current_user)):
    return get_ticket(ticket_id)

@app.put(
    "/tickets/{ticket_id}/status",
    response_model=Ticket,
    operation_id="update_ticket_status",
    summary="Update the status of a ticket",
    description="Changes the status of a support ticket. Valid statuses are: open, closed, pending."
)
def api_update_ticket_status(ticket_id: int, body: UpdateStatusRequest, user: dict = Depends(get_current_user)):
    return update_status(ticket_id, body.status)

@app.delete(
    "/tickets/{ticket_id}",
    response_model=Ticket,
    operation_id="delete_ticket",
    summary="Delete a ticket",
    description="Deletes a support ticket permanently based on its ID."
)
def api_delete_ticket(ticket_id: int, user: dict = Depends(get_current_user)):
    return delete_ticket(ticket_id)

# === MCP & SSE Integration ===
mcp = FastMCP.from_fastapi(
    app=app,
    describe_all_responses=True,
    describe_full_response_schema=True,
)

async def intercepted_post_handler(scope, receive, send):
    if scope["type"] != "http":
        return await transport.handle_post_message(scope, receive, send)

    # Custom receive wrapper to capture the body
    body = b""
    more_body = True

    async def wrapped_receive():
        nonlocal body, more_body
        message = await receive()
        if message["type"] == "http.request":
            body += message.get("body", b"")
            more_body = message.get("more_body", False)
        return message

    # Await full body
    while more_body:
        await wrapped_receive()

    try:
        parsed = json.loads(body)
        print("📨 Audited POST Payload:")
        print(json.dumps(parsed, indent=2))
    except Exception as e:
        print(f"⚠️ Failed to parse JSON body: {e}")

    # Replay receive with stored body
    async def replay_receive():
        yield {"type": "http.request", "body": body, "more_body": False}

    # Pipe back to original handler
    await transport.handle_post_message(scope, replay_receive().__anext__, send)


# SSE Transport
transport = SseServerTransport("/messages/")

@app.get("/sse/")
async def sse_endpoint(request: Request):
    async with transport.connect_sse(request.scope, request.receive, request._send) as streams:
        await mcp._mcp_server.run(
            streams[0], streams[1], mcp._mcp_server.create_initialization_options()
        )

# Mount /messages/ POST handler
app.mount("/messages/", intercepted_post_handler)

# === Entrypoint ===
if __name__ == "__main__":
    mcp.run(
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True
    )