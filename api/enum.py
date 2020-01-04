from collections import namedtuple
from enum import Enum

choice = namedtuple('Choice', 'name value')


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return [choice(e.name, e.value) for e in cls]


class InsuranceTypes(ChoiceEnum):
    auto = "auto"
    disability = "disability"
    home = "home"
    life = "life"


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
