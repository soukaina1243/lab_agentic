from mcp.server.fastmcp import FastMCP
import uvicorn

mcp = FastMCP("finance-mcp")

@mcp.tool()
def estimate_budget(destination: str, days: int) -> str:
    """Estimate total travel cost in USD. Input: destination name and number of days."""
    cost_per_day = {
        "Barcelona": 150,
        "Paris": 200,
        "Tokyo": 180,
    }
    daily = cost_per_day.get(destination, 120)
    total = daily * days
    return f"Estimated budget for {days} days in {destination}: ${total} USD (≈${daily}/day for accommodation, food, transport)."

if __name__ == "__main__":
    app = mcp.sse_app()
    uvicorn.run(app, host="127.0.0.1", port=3002)