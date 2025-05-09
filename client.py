import asyncio
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP

# Use url parameter directly
server = MCPServerHTTP(url="http://localhost:8000/sse")

PROVIDER_NAME = "openai"
MODEL_NAME = "gpt-4o-mini"
PYDANTIC_AI_MODEL = f"{PROVIDER_NAME}:{MODEL_NAME}"

agent = Agent(PYDANTIC_AI_MODEL, mcp_servers=[server], verbose=True)

USE_CASES = [
    {
        "name": "Create then list tickets",
        "prompt": """Create a ticket titled "Broken login flow" with description "User reports login redirect fails".
                     Then list all tickets and confirm it's there."""
    },
    {
        "name": "Create then close ticket",
        "prompt": """Create a ticket titled "Delayed shipment" with description "Order #4421 not received."
                     Then mark it as closed."""
    },
    {
        "name": "Create then simulate delete",
        "prompt": """Create a ticket titled "To be removed" with any description.
                     Then update the ticket title to "REMOVED" and set status to "closed"."""
    }
]


async def main():
    async with agent.run_mcp_servers():
        for case in USE_CASES:
            print(f"\n🧪 {case['name']}")
            result = await agent.run(case["prompt"])
            print(result.output)
            print("—" * 60)


if __name__ == "__main__":
    asyncio.run(main())
