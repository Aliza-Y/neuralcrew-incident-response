import asyncio
from agents.triage_agent import main as triage_main
from agents.technical_agent import main as technical_main
from agents.comms_agent import main as comms_main
from agents.resolution_agent import main as resolution_main

async def run_all():
    print("="*50)
    print("NeuralCrew — Incident Response System")
    print("Starting all 4 agents...")
    print("="*50)
    await asyncio.gather(
        triage_main(),
        technical_main(),
        comms_main(),
        resolution_main(),
    )

if __name__ == "__main__":
    asyncio.run(run_all())