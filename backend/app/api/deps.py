from app.services.gemini_service import GeminiService
from app.services.simulation_engine import InMemorySimulationStore, SimulationEngine
from app.services.tiger_service import TigerService

simulation_store = InMemorySimulationStore()
tiger_service = TigerService()
gemini_service = GeminiService()
simulation_engine = SimulationEngine(store=simulation_store, tiger_service=tiger_service, gemini_service=gemini_service)


def get_simulation_engine() -> SimulationEngine:
    return simulation_engine
