import unittest
from unittest.mock import MagicMock

from configs.constants import (
    LTV_HIGH_SCORE,
    LTV_MEDIUM_SCORE,
    LTV_LOW_SCORE,
    DTI_HIGH_SCORE,
    DTI_MEDIUM_SCORE,
    DTI_LOW_SCORE,
    CREDIT_SCORE_GOOD,
    CREDIT_SCORE_POOR,
    CREDIT_SCORE_GOOD_DEDUCTION,
    CREDIT_SCORE_POOR_ADDITION,
    CREDIT_SCORE_NEUTRAL,
    LOAN_TYPE_FIXED,
    LOAN_TYPE_ADJUSTABLE,
    LOAN_TYPE_FIXED_SCORE,
    LOAN_TYPE_ADJUSTABLE_SCORE,
    PROPERTY_TYPE_SINGLE_FAMILY,
    PROPERTY_TYPE_CONDO,
    PROPERTY_TYPE_SINGLE_FAMILY_SCORE,
    PROPERTY_TYPE_CONDO_SCORE,
    RATING_AAA,
    RATING_BBB,
    RATING_C,
)
from domain.credit_rating import LoanToValueRisk, DebtToIncomeRisk, CreditScoreRisk, LoanTypeRisk, PropertyTypeRisk, \
    CreditRatingService


class TestRiskCalculators(unittest.TestCase):
    def setUp(self):
        self.mortgage = MagicMock()

    def test_loan_to_value_risk(self):
        calculator = LoanToValueRisk()

        self.mortgage.loan_amount = 91
        self.mortgage.property_value = 100
        self.assertEqual(calculator.calculate(self.mortgage), LTV_HIGH_SCORE)

        self.mortgage.loan_amount = 81
        self.mortgage.property_value = 100
        self.assertEqual(calculator.calculate(self.mortgage), LTV_MEDIUM_SCORE)

        self.mortgage.loan_amount = 50
        self.mortgage.property_value = 100
        self.assertEqual(calculator.calculate(self.mortgage), LTV_LOW_SCORE)

    def test_debt_to_income_risk(self):
        calculator = DebtToIncomeRisk()

        self.mortgage.debt_amount = 60
        self.mortgage.annual_income = 100
        self.assertEqual(calculator.calculate(self.mortgage), DTI_HIGH_SCORE)

        self.mortgage.debt_amount = 41
        self.mortgage.annual_income = 100
        self.assertEqual(calculator.calculate(self.mortgage), DTI_MEDIUM_SCORE)

        self.mortgage.debt_amount = 10
        self.mortgage.annual_income = 100
        self.assertEqual(calculator.calculate(self.mortgage), DTI_LOW_SCORE)

    def test_credit_score_risk(self):
        calculator = CreditScoreRisk()

        self.mortgage.credit_score = CREDIT_SCORE_GOOD
        self.assertEqual(calculator.calculate(self.mortgage), CREDIT_SCORE_GOOD_DEDUCTION)

        self.mortgage.credit_score = CREDIT_SCORE_POOR - 1
        self.assertEqual(calculator.calculate(self.mortgage), CREDIT_SCORE_POOR_ADDITION)

        self.mortgage.credit_score = (CREDIT_SCORE_POOR + CREDIT_SCORE_GOOD) // 2
        self.assertEqual(calculator.calculate(self.mortgage), CREDIT_SCORE_NEUTRAL)

    def test_loan_type_risk(self):
        calculator = LoanTypeRisk()

        self.mortgage.loan_type = LOAN_TYPE_FIXED
        self.assertEqual(calculator.calculate(self.mortgage), LOAN_TYPE_FIXED_SCORE)

        self.mortgage.loan_type = LOAN_TYPE_ADJUSTABLE
        self.assertEqual(calculator.calculate(self.mortgage), LOAN_TYPE_ADJUSTABLE_SCORE)

    def test_property_type_risk(self):
        calculator = PropertyTypeRisk()

        self.mortgage.property_type = PROPERTY_TYPE_CONDO
        self.assertEqual(calculator.calculate(self.mortgage), PROPERTY_TYPE_CONDO_SCORE)

        self.mortgage.property_type = PROPERTY_TYPE_SINGLE_FAMILY
        self.assertEqual(calculator.calculate(self.mortgage), PROPERTY_TYPE_SINGLE_FAMILY_SCORE)


class TestCreditRatingService(unittest.TestCase):
    def setUp(self):
        self.service = CreditRatingService()
        self.mortgage1 = MagicMock()
        self.mortgage2 = MagicMock()

    def test_calculate_risk_score(self):
        self.mortgage1.loan_amount = 90
        self.mortgage1.property_value = 100
        self.mortgage1.debt_amount = 60
        self.mortgage1.annual_income = 100
        self.mortgage1.credit_score = CREDIT_SCORE_GOOD
        self.mortgage1.loan_type = LOAN_TYPE_FIXED
        self.mortgage1.property_type = PROPERTY_TYPE_CONDO

        total_score = self.service.calculate_risk_score(self.mortgage1)
        self.assertIsInstance(total_score, int)

    def test_calculate_credit_rating(self):
        self.mortgage1.credit_score = CREDIT_SCORE_GOOD
        self.mortgage2.credit_score = CREDIT_SCORE_POOR

        self.mortgage1.loan_amount = 90
        self.mortgage1.property_value = 100
        self.mortgage2.loan_amount = 50
        self.mortgage2.property_value = 100

        self.mortgage1.debt_amount = 60
        self.mortgage1.annual_income = 100
        self.mortgage2.debt_amount = 20
        self.mortgage2.annual_income = 100

        self.mortgage1.loan_type = LOAN_TYPE_FIXED
        self.mortgage2.loan_type = LOAN_TYPE_ADJUSTABLE

        self.mortgage1.property_type = PROPERTY_TYPE_SINGLE_FAMILY
        self.mortgage2.property_type = PROPERTY_TYPE_CONDO

        rating = self.service.calculate_credit_rating([self.mortgage1, self.mortgage2])
        self.assertIn(rating, [RATING_AAA, RATING_BBB, RATING_C])


if __name__ == "__main__":
    unittest.main()
