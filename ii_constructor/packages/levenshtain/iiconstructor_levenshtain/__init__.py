from dataclasses import dataclass
from typing import Any, Optional, Union

from iiconstructor_core.domain import InputDescription, StepVectorBaseClassificator, State
from iiconstructor_core.domain.primitives import Input, Name
from iiconstructor_core.domain.exceptions import NotExists
from iiconstructor_core.domain.porst import ScenarioInterface
import Levenshtein

@dataclass
class Synonym:
    value:str

    def __eq__(self, value: object) -> bool:
        return value.value == self.value

class SynonymsGroup:
    synonyms: list[Synonym]
    
    def __init__(self, other:Optional[Union['SynonymsGroup' , list[Synonym]]] = None):
        if isinstance(other, SynonymsGroup):
            self.synonyms = other.synonyms
        elif isinstance(other, list):
            for synonym in other:
                if not isinstance(synonym, Synonym):
                    raise TypeError(other)
            self.synonyms = other
        else:
            self.synonyms = []

class LevenshtainVector(InputDescription):
    synonyms: SynonymsGroup

    def __init__(self, name: Name, synonyms: SynonymsGroup = None) -> None:
        super().__init__(name)
        self.synonyms = SynonymsGroup() if synonyms is None else synonyms
    
class LevenshtainClassificator(StepVectorBaseClassificator):
    def __init__(self, project: ScenarioInterface) -> None:
        super().__init__(project)

    def calc(self, cur_input: Input, possible_inputs: dict[str, State]) -> Optional[State]:
        best_score = 0
        best: State = None

        for key, val in possible_inputs.items():
            vector = self._StepVectorBaseClassificator__project.get_vector(Name(key))
            if not isinstance(vector, LevenshtainVector):
                continue
            
            best_distance: int
            for synonym in vector.synonyms.synonyms:
                distance = Levenshtein.distance(synonym.value.lower(), cur_input.value.lower())

                if best is None or distance < best_distance:
                    best_distance = distance
                    best = val
                    continue

        if best_distance >= len(cur_input.value) / 2:
            raise NotExists(cur_input, "Подходящий вектор")

        return best