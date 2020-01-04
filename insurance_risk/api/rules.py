from datetime import datetime

from api.enum import HouseOwnership, UserMaritalStatus

RULES = []


def register_rule(func):
    RULES.append(func)
    return func


def add_risk_points(scores, value, fields='all'):
    scores.update({
        field: score + value
        for field, score in scores.items()
        if (fields == 'all') or (field in fields)
    })
    return scores


def deduct_risk_points(scores, value, fields='all'):
    return add_risk_points(scores, -value, fields)


@register_rule
def handle_scores_by_age(scores, age, **kwargs):
    if age < 30:
        return deduct_risk_points(scores, 2)
    elif age < 40:
        return deduct_risk_points(scores, 1)
    return scores


@register_rule
def handle_scores_by_income(scores, income, **kwargs):
    if income > 200000:
        scores = deduct_risk_points(scores, 1)
    return scores


@register_rule
def handle_scores_by_house_status(scores, house, **kwargs):
    if house and house['ownership_status'] == HouseOwnership.mortgaged:
        scores = add_risk_points(scores, 1, ('home', 'disability'))
    return scores


@register_rule
def handle_scores_by_dependents(scores, dependents, **kwargs):
    if dependents:
        scores = add_risk_points(scores, 1, ('life', 'disability'))
    return scores


@register_rule
def handle_scores_by_marital_status(scores, marital_status, **kwargs):
    if marital_status == UserMaritalStatus.married:
        scores = add_risk_points(scores, 1, ('life', ))
        scores = deduct_risk_points(scores, 1, ('disability', ))

    return scores


@register_rule
def handle_scores_by_vehicle(scores, vehicle, **kwargs):
    if vehicle and vehicle['year'] >= datetime.now().year - 5:
        scores = add_risk_points(scores, 1, ('auto', ))
    return scores
