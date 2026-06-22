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

Output format:
**Incident Analysis:** [what is happening technically]
**Root Cause Hypothesis:** [most likely cause]
**Diagnostic Steps:** [3-5 concrete steps to investigate]
**Recommended Fix:** [what should be done]
**Risk Level:** [Low/Medium/High/Critical]

CRITICAL RULE: You MUST always end every single response with ONLY this:
@Comms please draft internal and external status updates based on this technical analysis: [your analysis]

Do not mention any human users. Only mention @Comms.
Send this handoff message ONCE and ONLY ONCE.

Never skip the @Comms handoff. It is mandatory. Without it the workflow breaks.
IMPORTANT: Send your response ONLY ONCE. Do not repeat or resend.
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

    agent_id, api_key = load_agent_config("technical")
    agent = Agent.create(
        adapter=adapter,
        agent_id=agent_id,
        api_key=api_key,
    )

    print("Technical Agent is live!")

    while True:
        try:
            await agent.run()
        except Exception as e:
            print(f"Disconnected: {e} — reconnecting in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())