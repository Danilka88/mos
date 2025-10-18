from typing import Dict, Any, List
import json

from api.models import CompanyData, YearlyData
from api.agents.base import BaseAnalysisAgent

# Data Extraction Agents
from api.agents.enterprise.agents import (
    RevenueAgent, NetProfitAgent, EmployeeCountAgent, MoscowEmployeeCountAgent,
    PayrollTotalAgent, PayrollMoscowAgent, AvgSalaryTotalAgent, AvgSalaryMoscowAgent,
    TaxesMoscowNoExciseAgent, ProfitTaxAgent, PropertyTaxAgent, LandTaxAgent,
    NDFLAgent, TransportTaxAgent, OtherTaxesAgent, ExciseTaxesAgent,
    InvestmentsMoscowAgent, ExportVolumeAgent, PropertyComplexAgent, DataExtractionAgent,
)

# Analysis Agents
from api.agents.enterprise.analysis_agents import (
    CriticalEventsAgent, GrowthPointsAgent, AttentionZonesAgent, InterestingFactsAgent
)

class AnalysisOrchestrator:
    """Оркестратор для извлечения данных и проведения анализа по предприятию."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        # Agents for data extraction
        self.extraction_agents: Dict[str, DataExtractionAgent] = {
            "revenue": RevenueAgent(ollama_model=ollama_model),
            "net_profit": NetProfitAgent(ollama_model=ollama_model),
            "employee_count": EmployeeCountAgent(ollama_model=ollama_model),
            "moscow_employee_count": MoscowEmployeeCountAgent(ollama_model=ollama_model),
            "payroll_total": PayrollTotalAgent(ollama_model=ollama_model),
            "payroll_moscow": PayrollMoscowAgent(ollama_model=ollama_model),
            "avg_salary_total": AvgSalaryTotalAgent(ollama_model=ollama_model),
            "avg_salary_moscow": AvgSalaryMoscowAgent(ollama_model=ollama_model),
            "taxes_moscow_no_excise": TaxesMoscowNoExciseAgent(ollama_model=ollama_model),
            "profit_tax": ProfitTaxAgent(ollama_model=ollama_model),
            "property_tax": PropertyTaxAgent(ollama_model=ollama_model),
            "land_tax": LandTaxAgent(ollama_model=ollama_model),
            "ndfl": NDFLAgent(ollama_model=ollama_model),
            "transport_tax": TransportTaxAgent(ollama_model=ollama_model),
            "other_taxes": OtherTaxesAgent(ollama_model=ollama_model),
            "excise_taxes": ExciseTaxesAgent(ollama_model=ollama_model),
            "investments_moscow": InvestmentsMoscowAgent(ollama_model=ollama_model),
            "export_volume": ExportVolumeAgent(ollama_model=ollama_model),
            "property_complex": PropertyComplexAgent(ollama_model=ollama_model),
        }
        
        # Agents for analysis
        self.analysis_agents: Dict[str, BaseAnalysisAgent] = {
            "critical_events": CriticalEventsAgent(ollama_model=ollama_model),
            "growth_points": GrowthPointsAgent(ollama_model=ollama_model),
            "attention_zones": AttentionZonesAgent(ollama_model=ollama_model),
            "interesting_facts": InterestingFactsAgent(ollama_model=ollama_model),
        }

    def process_text_with_agents(self, text: str, all_fields: List[str]) -> Dict[str, Any]:
        """Запускает агентов по извлечению данных из текста."""
        results = {}
        for agent_name, agent_instance in self.extraction_agents.items():
            print(f"Запуск агента извлечения данных: {agent_name}")
            agent_result = agent_instance.extract_data(text, all_fields)
            results.update(agent_result)
        return results

    def transform_to_nested(self, flat_data: Dict[str, Any]) -> CompanyData:
        """
        Преобразует плоский словарь данных вложенную структуру CompanyData.
        """
        # Извлекаем ИНН и имя компании
        inn = flat_data.get("ИНН", "")
        company_name = flat_data.get("Наименование организации", "Неизвестная компания")
        industry = flat_data.get("Основная отрасль", "Неизвестная отрасль")
        activity_type = flat_data.get("Вид деятельности по основному ОКВЭД", "Неизвестный вид деятельности")

        # Группируем финансовые данные по годам
        financials_by_year: Dict[int, Dict[str, Any]] = {}
        for key, value in flat_data.items():
            if isinstance(key, str):
                # Определяем год из ключа
                year_match = None
                for year_val in range(2017, 2026): # Предполагаем годы с 2017 по 2025
                    if str(year_val) in key:
                        year_match = year_val
                        break
                
                if year_match:
                    year = year_match
                    if year not in financials_by_year:
                        financials_by_year[year] = {"year": year}
                    
                    # Очистка ключа для соответствия YearlyData
                    if "Выручка предприятия" in key: financials_by_year[year]["revenue"] = value
                    elif "Чистая прибыль (убыток)" in key: financials_by_year[year]["profit"] = value
                    elif "численность персонала (всего по компании)" in key: financials_by_year[year]["employees"] = value
                    elif "Налоги, уплаченные в бюджет Москвы (без акцизов)" in key: financials_by_year[year]["taxes"] = value
                    elif "Фонд оплаты труда всех сотрудников организации" in key: financials_by_year[year]["payroll"] = value
                    elif "Налог на прибыль" in key: financials_by_year[year]["profitTax"] = value # Используем alias
                    elif "Налог на имущество" in key: financials_by_year[year]["propertyTax"] = value # Используем alias
                    elif "НДФЛ" in key: financials_by_year[year]["personalIncomeTax"] = value # Используем alias
                    elif "Транспортный налог" in key: financials_by_year[year]["transport_tax"] = value
                    elif "Прочие налоги" in key: financials_by_year[year]["other_taxes"] = value
                    elif "Акцизы" in key: financials_by_year[year]["excise_taxes"] = value
                    elif "Инвестиции в Мск" in key: financials_by_year[year]["investments_moscow"] = value
                    elif "Объем экспорта" in key: financials_by_year[year]["export_volume"] = value
                    elif "Средняя з.п. всех сотрудников организации" in key: financials_by_year[year]["avg_salary_total"] = value
                    elif "Средняя з.п. сотрудников, работающих в Москве" in key: financials_by_year[year]["avg_salary_moscow"] = value

        yearly_data_list = []
        for year in sorted(financials_by_year.keys()):
            # Заполняем отсутствующие поля значениями по умолчанию или None
            yd_data = financials_by_year[year]
            yearly_data_list.append(YearlyData(
                year=year,
                revenue=yd_data.get("revenue", 0.0),
                profit=yd_data.get("profit", 0.0),
                employees=yd_data.get("employees", 0),
                taxes=yd_data.get("taxes", 0.0),
                payroll=yd_data.get("payroll", 0.0),
                profitTax=yd_data.get("profitTax", 0.0),
                propertyTax=yd_data.get("propertyTax", 0.0),
                personalIncomeTax=yd_data.get("personalIncomeTax", 0.0),
                # Добавьте остальные поля YearlyData с значениями по умолчанию
                # Для полей, которые не извлекаются агентами, можно оставить 0.0 или None
                # Например, если transport_tax не извлекается, он будет None по умолчанию
            ))

        # Создаем CompanyData
        company_data = CompanyData(
            id=hash(inn), # Простой способ получить ID, можно использовать UUID
            name=company_name,
            inn=inn,
            industry=industry,
            activityType=activity_type,
            financials=yearly_data_list
        )
        return company_data

    def run_analysis(self, company: CompanyData) -> Dict[str, List[str]]:
        """Запускает аналитических агентов для сгенерированных данных одной компании."""
        analysis_results = {}
        
        # Агенты анализа теперь принимают Pydantic модель CompanyData
        for agent_name, agent_instance in self.analysis_agents.items():
            print(f"Запуск аналитического агента: {agent_name}")
            insights = agent_instance.analyze(company)
            analysis_results[agent_name.replace("_events", "").replace("_points", "").replace("_zones", "").replace("facts", "")] = insights
            
        return analysis_results
