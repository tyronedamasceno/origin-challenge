from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from freezegun import freeze_time

RISK_PROFILE_URL = reverse('risk-profile')


class RiskProfileEndpointTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.base_payload = {
            "age": 35,
            "dependents": 2,
            "house": {"ownership_status": "owned"},
            "income": 0,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

    def test_endpoint_only_accepts_post_requests(self):
        request_methods = [
            self.client.get, self.client.put, self.client.patch,
            self.client.delete
        ]
        for request_method in request_methods:
            response = request_method(RISK_PROFILE_URL)
            self.assertEqual(
                response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
            )

    def test_risk_profile_requires_valid_json_payload(self):
        body_params = [
            'age', 'dependents', 'income', 'marital_status', 'risk_questions',
        ]
        response = self.client.post(RISK_PROFILE_URL, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        for param in body_params:
            self.assertIn(param, response.data)

    @freeze_time('2020-01-04')
    def test_successful_risk_profile_calculating(self):
        expected_response = {
            "auto": "regular",
            "disability": "ineligible",
            "home": "economic",
            "life": "regular"
        }
        response = self.client.post(
            RISK_PROFILE_URL, self.base_payload, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)
