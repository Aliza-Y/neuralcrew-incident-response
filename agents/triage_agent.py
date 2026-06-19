import asyncio
import os

from dotenv import load_dotenv
from band import Agent
from band.adapters import LangGraphAdapter
from band.config import load_agent_config
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

SYSTEM_PROMPT = """
You are the Triage Agent for an internal incident response workflow.

Your job is to quickly classify incoming incidents and hand them off to Technical.
When @Triage is mentioned, do the following:

1. Read the incident description carefully.
2. Classify severity as one of: P0, P1, P2, P3.
3. Identify:
   - impacted systems
   - impacted users
   - likely incident type
   - urgency
   - whether escalation is required immediately
4. Summarize the incident in a short, structured format.
5. End with a clear handoff to @Technical for investigation.

Output format:
- Incident Summary
- Severity
- Category
- Impact
- Immediate Action
- Handoff

Be concise, precise, and operational.
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

    agent_id, api_key = load_agent_config("triage")
    agent = Agent.create(
        adapter=adapter,
        agent_id=agent_id,
        api_key=api_key,
    )

    print("Triage Agent is live!")
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())