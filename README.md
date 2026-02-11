# 🏦 Agentic Compliance Auditor
**Scaling Financial Oversight with LangGraph & Gemini**

## 🌟 Project Overview
This project implements a multi-agent workflow for AML (Anti-Money Laundering) compliance. It bridges the gap between high-volume data processing and nuanced AI reasoning, featuring a mandatory "Human-in-the-Loop" gate for high-stakes decisions.

## 🏗️ Architecture
The system is built on an event-driven **StateGraph**, ensuring scalability and fault tolerance.

```mermaid
graph TD
    A[Incoming Transaction] --> B(Node 1: Screener)
    B -->|Flagged| C{HITL Breakpoint}
    C -->|Approved| D(Node 2: Gemini Auditor)
    D --> E[Compliance Report]
    B -->|Cleared| F[End Process]