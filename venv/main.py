from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# Import our logic
from state import AgentState
from nodes import screener_node, gemini_auditor

load_dotenv()

# 1. Initialize Graph
workflow = StateGraph(AgentState)

# 2. Add Nodes
workflow.add_node("screener", screener_node)
workflow.add_node("auditor", gemini_auditor)

# 3. Define Flow
workflow.set_entry_point("screener")

# Logic: If flagged, go to Auditor. Otherwise, finish.
workflow.add_conditional_edges(
    "screener",
    lambda state: "auditor" if state["is_flagged"] else END
)

workflow.add_edge("auditor", END)

# 4. Compile with Memory & HITL Breakpoint
# This tells the graph to STOP before the auditor runs
checkpointer = MemorySaver()
app = workflow.compile(
    checkpointer=checkpointer, 
    interrupt_before=["auditor"]
)

# --- Test Execution ---
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "1"}}
    initial_input = {
        "transaction_data": {"id": "TX123", "amount": 15000, "country": "UK"},
        "logs": ["Process started."]
    }

    print("--- Running Screener ---")
    for event in app.stream(initial_input, config):
        print(event)

    print("\n--- SYSTEM PAUSED: Awaiting Human Approval ---")
    # In a real app, this is where a human would review the logs
    # To resume, we just stream again with None as input
    
    user_action = input("Type 'yes' to approve Gemini analysis: ")
    if user_action.lower() == "yes":
        print("--- Resuming for Gemini Audit ---")
        for event in app.stream(None, config):
            print(event)