import unittest
from flask import Flask

from configs.constants import DATA, LOW_RISK_PAYLOAD, MEDIUM_RISK_PAYLOAD, HIGH_RISK_PAYLOAD, CREDIT_RATING, \
    RATING_AAA, RATING_BBB, RATING_C, CREDIT_RATING_ENDPOINT
from routes.rating_route import api


class TestCalculateCreditRating(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up Flask app for testing"""
        cls.app = Flask(__name__)
        cls.app.register_blueprint(api)
        cls.client = cls.app.test_client()

    def test_calculate_credit_rating_low_risk(self):
        """Test a valid payload"""
        payload = LOW_RISK_PAYLOAD
        response = self.client.post(CREDIT_RATING_ENDPOINT, json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(CREDIT_RATING, response.json[DATA])
        self.assertEqual(response.json[DATA][CREDIT_RATING], RATING_AAA)

    def test_calculate_credit_rating_medium_risk(self):
        """Test a high-risk payload"""
        payload = MEDIUM_RISK_PAYLOAD

        response = self.client.post(CREDIT_RATING_ENDPOINT, json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(CREDIT_RATING, response.json[DATA])
        self.assertEqual(response.json[DATA][CREDIT_RATING], RATING_BBB)

    def test_calculate_credit_rating_high_risk(self):
        """Test a high-risk payload"""
        payload = HIGH_RISK_PAYLOAD
        response = self.client.post(CREDIT_RATING_ENDPOINT, json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(CREDIT_RATING, response.json[DATA])
        self.assertEqual(response.json[DATA][CREDIT_RATING], RATING_C)


if __name__ == "__main__":
    unittest.main()
