from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

RISK_URL = reverse('risk-profile')


class RiskProfileEndpointTestCase(TestCase):
    def setup(self):
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
        wrong_methods = [
            self.client.get, self.client.patch, self.client.get,
            self.client.delete, self.client, put
        ]
        for request_method in wrong_methods:
            response = request_method(RISK_URL)
            self.assertEqual(
                response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
            )
