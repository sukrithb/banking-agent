from langchain_google_genai import ChatGoogleGenerativeAI

def gemini_auditor(state: AgentState):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    tx = state['raw_data']
    prompt = f"Analyze this UK transaction for AML risks: £{tx['amount']} from {tx['sender']}."
    response = llm.invoke(prompt)
    return {"audit_report": response.content}