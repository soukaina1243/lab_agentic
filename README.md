# 🌍 Agentic Travel Planning Assistant

Built with LangChain, MCP, Ollama and Streamlit.

## Stack
- Python 3.10
- LangChain 0.3.25
- MCP 1.6.0
- Ollama (llama3.2)
- Streamlit

## MCP Tool Servers
| Tool | Port |
|---|---|
| Destination Search | 3001 |
| Budget Calculator | 3002 |
| Weather | 3003 |
| Currency Converter | 3004 |
| Calculator | 3005 |

## Setup

### 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/travel_agent.git
cd travel_agent

### 2. Create virtual environment
py -3.10 -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Pull Ollama model
ollama pull llama3.2

### 5. Start MCP servers (separate terminals)
python servers/destination_mcp.py
python servers/budget_mcp.py
python servers/weather_mcp.py
python servers/currency_mcp.py
python servers/calculator_mcp.py

### 6. Run the app
streamlit run app.py