from abc import ABC, abstractmethod
from utils.decorators import log_method
from configs.constants import (
    LTV_HIGH_THRESHOLD, LTV_MEDIUM_THRESHOLD, LTV_HIGH_SCORE, LTV_MEDIUM_SCORE, LTV_LOW_SCORE,
    DTI_HIGH_THRESHOLD, DTI_MEDIUM_THRESHOLD, DTI_HIGH_SCORE, DTI_MEDIUM_SCORE, DTI_LOW_SCORE,
    CREDIT_SCORE_GOOD, CREDIT_SCORE_POOR, CREDIT_SCORE_GOOD_DEDUCTION, CREDIT_SCORE_POOR_ADDITION, CREDIT_SCORE_NEUTRAL,
    LOAN_TYPE_FIXED, LOAN_TYPE_ADJUSTABLE, LOAN_TYPE_FIXED_SCORE, LOAN_TYPE_ADJUSTABLE_SCORE,
    PROPERTY_TYPE_SINGLE_FAMILY, PROPERTY_TYPE_CONDO, PROPERTY_TYPE_SINGLE_FAMILY_SCORE, PROPERTY_TYPE_CONDO_SCORE,
    RATING_SCORE_AAA, RATING_SCORE_BBB, RATING_AAA, RATING_BBB, RATING_C,
    ERROR_MSG_LTV, ERROR_MSG_DTI, ERROR_MSG_CREDIT_SCORE, ERROR_MSG_LOAN_TYPE, ERROR_MSG_PROPERTY_TYPE,
    ERROR_MSG_TOTAL_RISK, ERROR_MSG_CREDIT_RATING
)
from typing import List
from utils.logger import project_logger


class RiskScoreCalculator(ABC):
    @abstractmethod
    def calculate(self, mortgage) -> int:
        """
        Abstract method to calculate risk score for a given mortgage.

        Args:
            mortgage (Mortgage): The mortgage object to calculate the risk score.

        Returns:
            int: The calculated risk score.
        """
        pass


class LoanToValueRisk(RiskScoreCalculator):
    @log_method
    def calculate(self, mortgage) -> int:
        """
        Calculate the Loan-to-Value (LTV) risk score.

        Args:
            mortgage (Mortgage): The mortgage object containing loan_amount and property_value.

        Returns:
            int: The calculated LTV risk score.
        """
        try:
            ltv = mortgage.loan_amount / mortgage.property_value
            if ltv > LTV_HIGH_THRESHOLD:
                return LTV_HIGH_SCORE
            elif ltv > LTV_MEDIUM_THRESHOLD:
                return LTV_MEDIUM_SCORE
            return LTV_LOW_SCORE
        except Exception as e:
            project_logger.error(f"{ERROR_MSG_LTV}: {e}")
            raise ValueError(ERROR_MSG_LTV) from e


class DebtToIncomeRisk(RiskScoreCalculator):
    @log_method
    def calculate(self, mortgage) -> int:
        """
        Calculate the Debt-to-Income (DTI) risk score.

        Args:
            mortgage (Mortgage): The mortgage object containing debt_amount and annual_income.

        Returns:
            int: The calculated DTI risk score.
        """
        try:
            dti = (mortgage.debt_amount / mortgage.annual_income) * 100
            if dti > DTI_HIGH_THRESHOLD:
                return DTI_HIGH_SCORE
            elif dti > DTI_MEDIUM_THRESHOLD:
                return DTI_MEDIUM_SCORE
            return DTI_LOW_SCORE
        except Exception as e:
            project_logger.error(f"{ERROR_MSG_DTI}: {e}")
            raise ValueError(ERROR_MSG_DTI) from e


class CreditScoreRisk(RiskScoreCalculator):
    def calculate(self, mortgage) -> int:
        """
        Calculate the Credit Score risk score.

        Args:
            mortgage (Mortgage): The mortgage object containing credit_score.

        Returns:
            int: The calculated Credit Score risk score.
        """
        try:
            if mortgage.credit_score >= CREDIT_SCORE_GOOD:
                return CREDIT_SCORE_GOOD_DEDUCTION
            elif mortgage.credit_score < CREDIT_SCORE_POOR:
                return CREDIT_SCORE_POOR_ADDITION
            return CREDIT_SCORE_NEUTRAL
        except Exception as e:
            project_logger.error(f"{ERROR_MSG_CREDIT_SCORE}: {e}")
            raise ValueError(ERROR_MSG_CREDIT_SCORE) from e


class LoanTypeRisk(RiskScoreCalculator):
    def calculate(self, mortgage) -> int:
        """
        Calculate the Loan Type risk score.

        Args:
            mortgage (Mortgage): The mortgage object containing loan_type.

        Returns:
            int: The calculated Loan Type risk score.
        """
        try:
            if mortgage.loan_type == LOAN_TYPE_FIXED:
                return LOAN_TYPE_FIXED_SCORE
            elif mortgage.loan_type == LOAN_TYPE_ADJUSTABLE:
                return LOAN_TYPE_ADJUSTABLE_SCORE
            return 0  # Fallback for unexpected loan types
        except Exception as e:
            project_logger.error(f"{ERROR_MSG_LOAN_TYPE}: {e}")
            raise ValueError(ERROR_MSG_LOAN_TYPE) from e


class PropertyTypeRisk(RiskScoreCalculator):
    def calculate(self, mortgage) -> int:
        """
        Calculate the Property Type risk score.

        Args:
            mortgage (Mortgage): The mortgage object containing property_type.

        Returns:
            int: The calculated Property Type risk score.
        """
        try:
            if mortgage.property_type == PROPERTY_TYPE_CONDO:
                return PROPERTY_TYPE_CONDO_SCORE
            elif mortgage.property_type == PROPERTY_TYPE_SINGLE_FAMILY:
                return PROPERTY_TYPE_SINGLE_FAMILY_SCORE
            return 0  # Fallback for unexpected property types
        except Exception as e:
            project_logger.error(f"{ERROR_MSG_PROPERTY_TYPE}: {e}")
            raise ValueError(ERROR_MSG_PROPERTY_TYPE) from e


class CreditRatingService:
    def __init__(self):
        """
        Initialize the CreditRatingService with a list of risk calculators.
        """
        self.risk_calculators: List[RiskScoreCalculator] = [
            LoanToValueRisk(),
            DebtToIncomeRisk(),
            CreditScoreRisk(),
            LoanTypeRisk(),
            PropertyTypeRisk()
        ]

    def calculate_risk_score(self, mortgage) -> int:
        """
        Calculate the total risk score for a mortgage based on all risk calculators.

        Args:
            mortgage (Mortgage): The mortgage object to calculate the risk score.

        Returns:
            int: The total risk score calculated by summing up individual risk scores.
        """
        try:
            return sum(calculator.calculate(mortgage) for calculator in self.risk_calculators)
        except Exception as e:
            project_logger.error(f"{ERROR_MSG_TOTAL_RISK}: {e}")
            raise ValueError(ERROR_MSG_TOTAL_RISK) from e

    def calculate_credit_rating(self, mortgages: List) -> str:
        """
        Calculate the overall credit rating based on the risk score of multiple mortgages.

        Args:
            mortgages (List[Mortgage]): A list of mortgage objects to calculate the credit rating.

        Returns:
            str: The calculated credit rating based on the total risk score.
        """
        try:
            total_score = sum(self.calculate_risk_score(m) for m in mortgages)

            avg_credit_score = sum(m.credit_score for m in mortgages) / len(mortgages)
            if avg_credit_score >= CREDIT_SCORE_GOOD:
                total_score -= 1
            elif avg_credit_score < CREDIT_SCORE_POOR:
                total_score += 1

            if total_score <= RATING_SCORE_AAA:
                return RATING_AAA
            elif total_score <= RATING_SCORE_BBB:
                return RATING_BBB
            return RATING_C
        except Exception as e:
            project_logger.error(f"{ERROR_MSG_CREDIT_RATING}: {e}")
            raise ValueError(ERROR_MSG_CREDIT_RATING) from e
