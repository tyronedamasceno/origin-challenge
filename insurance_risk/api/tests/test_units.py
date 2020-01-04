from django.test import TestCase

from api import core


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


class RiskAlgorithmRulesTestCase(TestCase):
    def setUp(self):
        self.base_scores = core.get_base_scores([0, 0, 0])

    def test_add_and_deduct_risk_points(self):
        add_1_to_all = core.add_risk_points(dict(self.base_scores), 1)
        add_2_to_auto_and_disability = core.add_risk_points(
            dict(self.base_scores), 2, ('auto', 'disability')
        )
        deduct_1_from_all = core.deduct_risk_points(dict(self.base_scores), 1)
        deduct_2_from_home_and_life = core.deduct_risk_points(
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
