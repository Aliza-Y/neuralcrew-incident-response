import asyncio
import os

from dotenv import load_dotenv
from band import Agent
from band.adapters import LangGraphAdapter
from band.config import load_agent_config
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

SYSTEM_PROMPT = """
You are the Technical Agent in an internal incident response workflow.

Your job is to investigate incidents after triage and identify the most likely root cause.
When @Technical is mentioned, do the following:

1. Analyze the incident summary from Triage.
2. Investigate likely technical causes.
3. Suggest concrete diagnostic steps.
4. Recommend the most likely fix or remediation.
5. Flag if the issue needs escalation, rollback, or immediate containment.
6. Hand off to @Comms with a technical summary suitable for status updates.

Output format:
- Incident Analysis
- Root Cause Hypothesis
- Diagnostic Steps
- Recommended Fix
- Risk Level
- Handoff to Comms

Be concise, precise, and engineering-focused.
"""

async def main():
    load_dotenv()

    adapter = LangGraphAdapter(
        llm=ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0,
        ),
        checkpointer=InMemorySaver(),
    )

    agent_id, api_key = load_agent_config("technical")
    agent = Agent.create(
        adapter=adapter,
        agent_id=agent_id,
        api_key=api_key,
    )

    print("Technical Agent is live!")
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())