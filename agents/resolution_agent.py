import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai
from band import Agent
from band.config import load_agent_config

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

End with: INCIDENT CLOSED — [timestamp] — Full audit trail available in this Band room.
"""

class GeminiResolutionAgent:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_PROMPT,
        )

    def respond(self, message: str) -> str:
        response = self.model.generate_content(message)
        return response.text


async def main():
    load_dotenv()

    gemini_agent = GeminiResolutionAgent()

    class GeminiAdapter:
        def __init__(self, agent):
            self.agent = agent

        async def handle_message(self, message: str) -> str:
            return self.agent.respond(message)

    adapter_instance = GeminiAdapter(gemini_agent)

    agent_id, api_key = load_agent_config("resolution")
    agent = Agent.create(
        adapter=adapter_instance,
        agent_id=agent_id,
        api_key=api_key
    )

    print("Resolution Agent is live!")
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())