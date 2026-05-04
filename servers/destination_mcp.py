from mcp.server.fastmcp import FastMCP
import uvicorn

mcp = FastMCP("travel-search-mcp")

@mcp.tool()
def search_destination(destination: str) -> str:
    """Retrieve tourist attractions, landmarks and activities. Input: city name like 'Barcelona'"""
    data = {
        "Barcelona": "Sagrada Familia, Park Güell, Las Ramblas, Gothic Quarter, Barceloneta Beach",
        "Paris": "Eiffel Tower, Louvre, Notre-Dame, Montmartre, Champs-Élysées",
        "Tokyo": "Shibuya Crossing, Senso-ji Temple, Shinjuku, Mount Fuji day trip, Akihabara",
    }
    return data.get(destination, f"Top attractions in {destination}: city center, local markets, museums, parks.")

if __name__ == "__main__":
    app = mcp.sse_app()
    uvicorn.run(app, host="127.0.0.1", port=3001)