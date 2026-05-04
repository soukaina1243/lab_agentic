from mcp.server.fastmcp import FastMCP
import uvicorn

mcp = FastMCP("calculator-mcp")

@mcp.tool()
def calculate(expression: str) -> str:
    """Perform arithmetic calculations. Input: math expression like '150 * 5' or '750 / 3'"""
    try:
        allowed = {
            "__builtins__": {},
            "abs": abs, "round": round,
            "min": min, "max": max,
        }
        result = eval(expression, allowed)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}"

if __name__ == "__main__":
    app = mcp.sse_app()
    uvicorn.run(app, host="127.0.0.1", port=3005)