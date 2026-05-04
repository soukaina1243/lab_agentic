from mcp.server.fastmcp import FastMCP
import uvicorn

mcp = FastMCP("weather-mcp")

@mcp.tool()
def get_weather(destination: str, month: str = "June") -> str:
    """Get typical weather conditions for a destination. Input: city name and optional month."""
    weather_data = {
        "Barcelona": {
            "June": "Warm and sunny, 25°C avg. Perfect for outdoor activities.",
            "December": "Mild, 12°C avg. Good for sightseeing, fewer crowds.",
            "July": "Hot and sunny, 28°C avg. Great for beach activities.",
        },
        "Paris": {
            "June": "Mild, 20°C avg. Occasional rain. Mix of indoor/outdoor.",
            "December": "Cold, 5°C avg. Festive atmosphere, indoor activities.",
            "July": "Warm, 24°C avg. Busy tourist season.",
        },
        "Tokyo": {
            "June": "Rainy season, 22°C avg. Prefer indoor activities.",
            "December": "Cold and dry, 8°C avg. Good for winter illuminations.",
            "July": "Hot and humid, 30°C avg. Summer festivals.",
        },
    }
    city_data = weather_data.get(destination, {})
    return city_data.get(
        month,
        f"Typical weather in {destination} in {month}: moderate temperatures, check local forecast."
    )

if __name__ == "__main__":
    app = mcp.sse_app()
    uvicorn.run(app, host="127.0.0.1", port=3003)