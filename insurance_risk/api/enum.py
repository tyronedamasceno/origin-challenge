from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return [(e.name, e.value) for e in cls]


class Score(ChoiceEnum):
    economic = 'economic'
    ineligible = 'ineligible'
    regular = 'regular'
    responsible = 'responsible'
