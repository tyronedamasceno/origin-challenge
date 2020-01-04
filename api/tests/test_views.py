from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from freezegun import freeze_time

RISK_URL = reverse('risk-profile')


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
            response = request_method(RISK_URL)
            self.assertEqual(
                response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
            )

    def test_risk_profile_requires_valid_json_payload(self):
        body_params = [
            'age', 'dependents', 'income', 'marital_status', 'risk_questions',
            'house', 'vehicle'
        ]
        response = self.client.post(RISK_URL, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        for param in body_params:
            self.assertIn(param, response.data)

    def test_endpoint_validate_integer_fields(self):
        payload = dict(self.base_payload)
        int_fields = ('age', 'dependents', 'income')
        for field in int_fields:
            payload[field] = -1

        response = self.client.post(RISK_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), len(int_fields))
        for field in int_fields:
            self.assertIn(field, response.data)

    def test_endpoint_validate_risk_questions(self):
        payload = dict(self.base_payload)
        wrong_formats_for_risk_questions = (
            'x', 1, [], [1, 1], [1, 1, 1, 1], [1, 2, 1], [0, -1, 1]
        )

        for risk_questions in wrong_formats_for_risk_questions:
            payload['risk_questions'] = risk_questions
            response = self.client.post(RISK_URL, payload, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(len(response.data), 1)
            self.assertIn('risk_questions', response.data)

    @freeze_time('2020-01-04')
    def test_successful_risk_profile_calculating_with_example_input(self):
        expected_response = {
            "auto": "regular",
            "disability": "ineligible",
            "home": "economic",
            "life": "regular"
        }
        response = self.client.post(RISK_URL, self.base_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)
