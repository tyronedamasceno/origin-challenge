from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return [(e.name, e.value) for e in cls]


class HouseOwnership(ChoiceEnum):
    owned = 'owned'
    mortgaged = 'mortgaged'


class Score(ChoiceEnum):
    economic = 'economic'
    ineligible = 'ineligible'
    regular = 'regular'
    responsible = 'responsible'


class UserMaritalStatus(ChoiceEnum):
    single = 'single'
    married = 'married'
