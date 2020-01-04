from django.test import TestCase

from freezegun import freeze_time

from api import core, rules
from api.enum import Score, HouseOwnership, UserMaritalStatus


class InsuranceEligibilityTestCase(TestCase):
    def setUp(self):
        self.base_scores = core.get_base_scores([0, 0, 0])

    def test_calculating_base_scores(self):
        base_scores_1 = core.get_base_scores([0, 0, 0])
        base_scores_2 = core.get_base_scores([0, 1, 0])
        base_scores_3 = core.get_base_scores([1, 1, 1])
        self.assertEqual(
            base_scores_1, dict(auto=0, disability=0, home=0, life=0)
        )
        self.assertEqual(
            base_scores_2, dict(auto=1, disability=1, home=1, life=1)
        )
        self.assertEqual(
            base_scores_3, dict(auto=3, disability=3, home=3, life=3)
        )

    def test_check_eligibility_for_user_without_income_vehicle_or_houses(self):
        scores_without_income = core.check_eligibility(
            dict(self.base_scores), income=0, vehicle={'year': '2018'},
            house={"ownership_status": "owned"}, age=35
        )
        scores_without_vehicle = core.check_eligibility(
            dict(self.base_scores), income=1000, vehicle=None,
            house={"ownership_status": "owned"}, age=35
        )
        scores_without_house = core.check_eligibility(
            dict(self.base_scores), income=10000, vehicle={'year': '2018'},
            house=None, age=35
        )
        self.assertNotIn('disability', scores_without_income)
        self.assertNotIn('auto', scores_without_vehicle)
        self.assertNotIn('home', scores_without_house)

    def test_check_eligibility_for_user_over_60_years_old(self):
        scores_with_age_over_60 = core.check_eligibility(
            dict(self.base_scores), income=1000, vehicle={'year': '2018'},
            house={"ownership_status": "owned"}, age=61
        )
        self.assertNotIn('life', scores_with_age_over_60)
        self.assertNotIn('disability', scores_with_age_over_60)


class UtilsFunctionsTestCase(TestCase):
    def setUp(self):
        self.base_scores = core.get_base_scores([0, 0, 0])

    def test_add_and_deduct_risk_points(self):
        add_1_to_all = rules.add_risk_points(dict(self.base_scores), 1)
        add_2_to_auto_and_disability = rules.add_risk_points(
            dict(self.base_scores), 2, ('auto', 'disability')
        )
        deduct_1_from_all = rules.deduct_risk_points(dict(self.base_scores), 1)
        deduct_2_from_home_and_life = rules.deduct_risk_points(
            dict(self.base_scores), 2, ('home', 'life')
        )

        self.assertTrue(all(
            score == 1 for field, score in add_1_to_all.items())
        )
        self.assertTrue(all(
            score == -1 for field, score in deduct_1_from_all.items())
        )
        self.assertTrue(all(
            score == 2 for field, score in add_2_to_auto_and_disability.items()
            if field in ('auto', 'disability'))
        )
        self.assertTrue(all(
            score == -2 for field, score in deduct_2_from_home_and_life.items()
            if field in ('home', 'life'))
        )

    def test_getting_score_by_value(self):
        self.assertEqual(core.get_score_by_value(-1), Score.economic)
        self.assertEqual(core.get_score_by_value(0), Score.economic)

        self.assertEqual(core.get_score_by_value(1), Score.regular)
        self.assertEqual(core.get_score_by_value(2), Score.regular)

        self.assertEqual(core.get_score_by_value(3), Score.responsible)
        self.assertEqual(core.get_score_by_value(4), Score.responsible)


class RiskAlgorithmRulesTestCase(TestCase):
    def setUp(self):
        # Base scores start with 2
        self.base_scores = core.get_base_scores([1, 1, 0])

    def test_age_rule(self):
        under_30_user_scores = rules.handle_scores_by_age(
            dict(self.base_scores), age=29
        )
        between_30_40_user_scores = rules.handle_scores_by_age(
            dict(self.base_scores), age=35
        )
        self.assertTrue(all(
            score == 0 for field, score in under_30_user_scores.items())
        )
        self.assertTrue(all(
            score == 1 for field, score in between_30_40_user_scores.items())
        )

    def test_income_rule(self):
        over_200k_user_score = rules.handle_scores_by_income(
            dict(self.base_scores), income=200001
        )
        under_200k_user_score = rules.handle_scores_by_income(
            dict(self.base_scores), income=199999
        )
        self.assertTrue(all(
            score == 1 for field, score in over_200k_user_score.items())
        )
        self.assertTrue(all(
            score == 2 for field, score in under_200k_user_score.items())
        )

    def test_house_status_rule(self):
        mortgaged_house_user_score = rules.handle_scores_by_house_status(
            dict(self.base_scores),
            house={'ownership_status': HouseOwnership.mortgaged}
        )
        owned_house_user_score = rules.handle_scores_by_house_status(
            dict(self.base_scores),
            house={'ownership_status': HouseOwnership.owned}
        )
        self.assertTrue(all(
            score == 3 for field, score in mortgaged_house_user_score.items()
            if field in ('home', 'disability'))
        )
        self.assertTrue(all(
            score == 2 for field, score in owned_house_user_score.items()
            if field in ('home', 'disability'))
        )

    def test_dependents_rule(self):
        user_with_dependents_score = rules.handle_scores_by_dependents(
            dict(self.base_scores), dependents=1
        )
        user_without_dependent_score = rules.handle_scores_by_dependents(
            dict(self.base_scores), dependents=0
        )
        self.assertTrue(all(
            score == 3 for field, score in user_with_dependents_score.items()
            if field in ('life', 'disability'))
        )
        self.assertTrue(all(
            score == 2 for field, score in user_without_dependent_score.items()
            if field in ('life', 'disability'))
        )

    def test_marital_status_rule(self):
        user_married_score = rules.handle_scores_by_marital_status(
            dict(self.base_scores), marital_status=UserMaritalStatus.married
        )
        user_not_married_score = rules.handle_scores_by_marital_status(
            dict(self.base_scores), marital_status=UserMaritalStatus.single
        )
        self.assertEqual(user_married_score['life'], 3)
        self.assertEqual(user_married_score['disability'], 1)
        self.assertTrue(all(
            score == 2 for field, score in user_not_married_score.items())
        )

    @freeze_time('2020-01-04')
    def test_vehicle_rule(self):
        user_with_new_vehicle_score = rules.handle_scores_by_vehicle(
            dict(self.base_scores), vehicle={'year': 2019}
        )
        user_with_old_vehicle_score = rules.handle_scores_by_vehicle(
            dict(self.base_scores), vehicle={'year': 2012}
        )
        self.assertEqual(user_with_new_vehicle_score['auto'], 3)
        self.assertEqual(user_with_old_vehicle_score['auto'], 2)
