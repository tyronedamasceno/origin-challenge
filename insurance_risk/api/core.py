from datetime import datetime

from api.enum import HouseOwnership, UserMaritalStatus, Score, InsuranceTypes


def get_base_scores(risk_questions):
    base_value = sum(risk_questions)
    return {
        "auto": base_value,
        "disability": base_value,
        "home": base_value,
        "life": base_value
    }


def check_eligibility(scores, income, vehicle, house, age):
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


def add_risk_points(scores, value, fields='all'):
    scores.update({
        field: score + value
        for field, score in scores.items()
        if (fields == 'all') or (field in fields)
    })
    return scores


def deduct_risk_points(scores, value, fields='all'):
    return add_risk_points(scores, -value, fields)


def handle_scores_by_age(scores, age):
    if age < 30:
        return deduct_risk_points(scores, 2)
    elif age < 40:
        return deduct_risk_points(scores, 1)
    return scores


def handle_scores_by_income(scores, income):
    if income > 200000:
        scores = deduct_risk_points(scores, 1)
    return scores


def handle_scores_by_house_status(scores, house):
    if house and house['ownership_status'] == HouseOwnership.mortgaged:
        scores = add_risk_points(scores, 1, ('home', 'disability'))
    return scores


def handle_scores_by_dependents(scores, dependents):
    if dependents:
        scores = add_risk_points(scores, 1, ('life', 'disability'))
    return scores


def handle_scores_by_marital_status(scores, marital_status):
    if marital_status == UserMaritalStatus.married:
        scores = add_risk_points(scores, 1, ('life', ))
        scores = deduct_risk_points(scores, 1, ('disability', ))

    return scores


def handle_scores_by_vehicle(scores, vehicle):
    if vehicle and vehicle['year'] >= datetime.now().year - 5:
        scores = add_risk_points(scores, 1, ('vehicle', ))
    return scores


def calculate_risk_profile(age, dependents, income, marital_status,
                           risk_questions, house=None, vehicle=None):
    scores = get_base_scores(risk_questions)
    scores = check_eligibility(scores, income, vehicle, house, age)

    scores = handle_scores_by_age(scores, age)
    scores = handle_scores_by_income(scores, income)
    scores = handle_scores_by_house_status(scores, house)
    scores = handle_scores_by_dependents(scores, dependents)
    scores = handle_scores_by_marital_status(scores, marital_status)
    scores = handle_scores_by_vehicle(scores, vehicle)

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
