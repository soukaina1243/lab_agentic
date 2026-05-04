import streamlit as st
from agent import run_travel_agent

st.set_page_config(page_title="🌍 Agentic Travel Planner", layout="wide")
st.title("🌍 Agentic Travel Planner")
st.caption("Powered by LangChain + MCP + Ollama (llama3.2)")

with st.sidebar:
    st.header("ℹ️ MCP Tool Servers")
    st.markdown("""
- 🗺️ **Destination Search** — port 3001
- 💰 **Budget Calculator** — port 3002
- 🌤️ **Weather Tool** — port 3003
- 💱 **Currency Converter** — port 3004
- 🔢 **Calculator** — port 3005
""")
    st.divider()
    st.header("💡 Example Queries")
    st.markdown("""
- *Plan a 5-day trip to Barcelona with budget in EUR*
- *I want to visit Tokyo in July for 7 days, what's my budget in JPY?*
- *Plan a Paris trip in December for 3 days*
""")

query = st.text_area(
    "✏️ Describe your trip",
    placeholder="e.g. Plan a 5-day trip to Barcelona with budget in EUR",
    height=100
)

if st.button("🚀 Plan My Trip", type="primary"):
    if not query.strip():
        st.warning("Please describe your trip first.")
    else:
        with st.spinner("🤖 Agent is planning your trip..."):
            try:
                answer, tool_log = run_travel_agent(query)

                st.subheader("📋 Your Travel Plan")
                st.write(answer)

                if tool_log:
                    st.subheader("🔧 Tool Calls Made")
                    for i, call in enumerate(tool_log, 1):
                        with st.expander(f"Step {i}: {call['tool']}"):
                            st.write(f"**Input:** {call['input']}")
                            st.write(f"**Output:** {call['output']}")

                st.success("✅ Plan generated successfully!")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Make sure all 5 MCP servers are running in separate terminals.")