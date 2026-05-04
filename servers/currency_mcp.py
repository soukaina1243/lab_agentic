from mcp.server.fastmcp import FastMCP
import uvicorn

mcp = FastMCP("currency-mcp")

@mcp.tool()
def convert_currency(amount: float, from_currency: str = "USD", to_currency: str = "EUR") -> str:
    """Convert an amount between currencies. Input: amount, source currency, target currency."""
    rates = {
        ("USD", "EUR"): 0.92,
        ("USD", "GBP"): 0.79,
        ("USD", "JPY"): 149.5,
        ("USD", "MAD"): 10.1,
        ("EUR", "USD"): 1.09,
        ("GBP", "USD"): 1.27,
        ("JPY", "USD"): 0.0067,
        ("MAD", "USD"): 0.099,
    }
    key = (from_currency.upper(), to_currency.upper())
    rate = rates.get(key, 1.0)
    converted = round(amount * rate, 2)
    return f"{amount} {from_currency.upper()} = {converted} {to_currency.upper()} (rate: {rate})"

if __name__ == "__main__":
    app = mcp.sse_app()
    uvicorn.run(app, host="127.0.0.1", port=3004)