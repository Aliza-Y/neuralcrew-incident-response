import asyncio
import os
from dotenv import load_dotenv
from band import Agent
from band.adapters import LangGraphAdapter
from band.config import load_agent_config
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

SYSTEM_PROMPT = """
You are the Resolution Agent, the final step in enterprise incident response.

When @Resolution is mentioned, you must:
1. Confirm the fix has been applied based on what Technical Agent reported
2. Write a post-mortem report with these sections:
   - Incident Summary
   - Timeline (when it started, when detected, when resolved)
   - Root Cause
   - Fix Applied
   - Prevention Steps (3 things to prevent this in future)
3. Declare the incident CLOSED with a timestamp

End with: INCIDENT CLOSED — [current timestamp] — Full audit trail available in this Band room.
"""

async def main():
    load_dotenv()

    adapter = LangGraphAdapter(
        llm=ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0,
        ),
        # checkpointer=InMemorySaver(),
        custom_section=SYSTEM_PROMPT,
    )

    agent_id, api_key = load_agent_config("resolution")
    agent = Agent.create(adapter=adapter, agent_id=agent_id, api_key=api_key)

    print("Resolution Agent is live!")

    while True:
        try:
            await agent.run()
        except Exception as e:
            print(f"Disconnected: {e} — reconnecting in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())