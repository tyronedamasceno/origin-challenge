from api.rules import RULES as RiskAlgorithmRules
from api.utils import get_base_scores, check_eligibility, format_risk_profile


def calculate_risk_profile(**kwargs):
    scores = get_base_scores(kwargs['risk_questions'])
    scores = check_eligibility(scores, **kwargs)

    for rule in RiskAlgorithmRules:
        scores = rule(scores, **kwargs)

    return format_risk_profile(scores)
