from dataclasses import dataclass
from typing import List, Dict, Any
from abc import ABC, abstractmethod


@dataclass
class KeywordExtractionResult:
    keywords: List[str]
    phrases: List[str]
    metadata: Dict[str, Any]

class KeywordExtractionStrategy(ABC):
    @abstractmethod
    def extract(self, text: str) -> KeywordExtractionResult:
        pass