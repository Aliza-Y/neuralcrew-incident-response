import asyncio
import os
from dotenv import load_dotenv
from band import Agent
from band.adapters import CrewAIAdapter
from band.config import load_agent_config

async def main():
    load_dotenv()

    adapter = CrewAIAdapter(
        model="gemini/gemini-1.5-flash",
        role="Communications Specialist",
        goal="Write clear internal and external incident communications for enterprise incidents",
        backstory="""You are an expert at translating technical problems into clear 
        communications for different audiences. When @Comms is mentioned with a technical 
        analysis, you must write TWO things:

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

        Then hand off: @Resolution please verify the fix and close this incident.""",
        verbose=True,
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