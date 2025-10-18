from pydantic import BaseModel, Field
from typing import Optional, List

class YearlyData(BaseModel):
    """
    Описывает структуру финансовых и операционных показателей компании за один конкретный год.
    """
    year: int
    revenue: float
    profit: float
    employees: int
    taxes: float
    payroll: float
    profit_tax: float = Field(alias="profitTax")
    property_tax: float = Field(alias="propertyTax")
    personal_income_tax: float = Field(alias="personalIncomeTax")

class CompanyData(BaseModel):
    """
    Описывает полную структуру данных по одной компании, 
    включая ее общие реквизиты и массив годовых финансовых показателей.
    """
    id: int
    name: str
    inn: str
    industry: str
    activity_type: str = Field(alias="activityType")
    financials: List[YearlyData]

class AnalysisInsights(BaseModel):
    """
    Описывает структуру с результатами анализа от ИИ-агентов.
    """
    critical: List[str]
    warning: List[str]
    positive: List[str]
    info: List[str]