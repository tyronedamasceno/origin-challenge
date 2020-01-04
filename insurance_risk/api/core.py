from api.rules import RULES as RiskAlgorithmRules
from api.enum import InsuranceTypes, Score


def get_base_scores(risk_questions):
    base_value = sum(risk_questions)
    return {
        "auto": base_value,
        "disability": base_value,
        "home": base_value,
        "life": base_value
    }


def check_eligibility(scores, income, vehicle, house, age, **kwargs):
    if not vehicle:
        scores.pop('auto', None)
    if not house:
        scores.pop('home', None)
    if not income:
        scores.pop('disability', None)

    if age > 60:
        scores.pop('disability', None)
        scores.pop('life', None)

    return scores


def calculate_risk_profile(**kwargs):
    scores = get_base_scores(kwargs['risk_questions'])
    scores = check_eligibility(scores, **kwargs)

    for rule in RiskAlgorithmRules:
        scores = rule(scores, **kwargs)

    return scores


def get_score_by_value(value):
    if value <= 0:
        return Score.economic
    elif value <= 2:
        return Score.regular
    return Score.responsible


def format_risk_profile(risk_profile):
    formated_risk_profile = {}
    for field, score in risk_profile.items():
        formated_risk_profile[field] = get_score_by_value(score).value

    for insurance in InsuranceTypes.choices():
        if insurance.name not in formated_risk_profile:
            formated_risk_profile[insurance.name] = Score.ineligible.value

    return formated_risk_profile
