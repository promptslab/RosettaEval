from rosettaeval.loader.tasks.base import Adapter
from rosettaeval.loader.tasks.medmcqa import MedMcQaQueryAdapter
from rosettaeval.loader.tasks.medqa import MedQaQueryAdapter

KNOWN_ADAPTERS = [
    MedQaQueryAdapter,
    MedMcQaQueryAdapter,
]
