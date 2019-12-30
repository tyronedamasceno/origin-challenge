from django.test import TestCase

from api import core


class RiskAlgorithmTestCase(TestCase):
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
