from rosetta_eval.loader.adapters.base import Adapter
from rosetta_eval.loader.adapters.medmcqa import MedMcQaQueryAdapter
from rosetta_eval.loader.adapters.medqa import MedQaQueryAdapter

KNOWN_ADAPTERS = [
    MedQaQueryAdapter,
    MedMcQaQueryAdapter,
]
