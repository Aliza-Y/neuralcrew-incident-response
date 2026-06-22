import asyncio
import os
from dotenv import load_dotenv
from band import Agent
from band.adapters import LangGraphAdapter
from band.config import load_agent_config
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

SYSTEM_PROMPT = """
You are the Communications Agent for enterprise incident response.

When @Comms is mentioned with a technical analysis, you must write TWO things:

1. INTERNAL UPDATE (for the engineering/ops team):
- What happened
- Current status
- What is being done
- Next update time

2. EXTERNAL STATUS PAGE UPDATE (for customers):
- Simple, non-technical language
- Acknowledge the issue without revealing internal details
- Apologize for disruption
- State when next update will be posted

CRITICAL RULE: You MUST always end every single response with this exact format:
@Resolution please verify the fix and close this incident based on this summary: [paste full summary here]

Never skip the @Resolution handoff. It is mandatory.
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

    agent_id, api_key = load_agent_config("comms")
    agent = Agent.create(adapter=adapter, agent_id=agent_id, api_key=api_key)

    print("Comms Agent is live!")

    while True:
        try:
            await agent.run()
        except Exception as e:
            print(f"Disconnected: {e} — reconnecting in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())