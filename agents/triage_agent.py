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

Output format:
**Incident Summary:** [brief description]
**Severity:** [P0/P1/P2/P3]
**Category:** [type of incident]
**Impact:** [users and systems affected]
**Immediate Action:** [what needs to happen]

CRITICAL RULE: You MUST always end every single response with this exact format:
@Technical [paste your full incident summary here so Technical can investigate]

Never skip the @Technical handoff. It is mandatory. Without it the workflow breaks.
"""

async def main():
    load_dotenv()

    adapter = LangGraphAdapter(
        llm=ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0,
        ),
        checkpointer=InMemorySaver(),
        custom_section=SYSTEM_PROMPT,
    )

    agent_id, api_key = load_agent_config("triage")
    agent = Agent.create(
        adapter=adapter,
        agent_id=agent_id,
        api_key=api_key,
    )

    print("Triage Agent is live!")

    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("band").setLevel(logging.DEBUG)

    while True:
        try:
            await agent.run()
        except Exception as e:
            print(f"Disconnected: {e} — reconnecting in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())