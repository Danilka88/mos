from langchain_core.prompts import PromptTemplate
from typing import List
import json

from api.agents.base import BaseAnalysisAgent
from api.models import CompanyData

class IndustryAnalysisAgent(BaseAnalysisAgent):
    """Базовый класс для агентов-аналитиков по отрасли."""
    def analyze(self, industry_name: str, companies: List[CompanyData]) -> List[str]:
        """
        Анализирует данные по отрасли и возвращает список инсайтов.
        """
        raise NotImplementedError

class IndustryCriticalEventsAgent(IndustryAnalysisAgent):
    """Агент для выявления критических событий в отрасли."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["industry_name", "companies_data_json"],
            template='''
            Ты - отраслевой аналитик. Проанализируй предоставленные JSON-данные по компаниям в отрасли '{industry_name}'.
            Твоя задача - выявить критические события на уровне всей отрасли.

            Критические события в отрасли это:
            - Общее снижение выручки или прибыли у большинства компаний в последнем отчетном году.
            - Значительное падение темпов роста отрасли по сравнению с предыдущими периодами.

            Для каждого найденного события, сформулируй краткий и ясный вывод в одну строку.
            Например: "Наблюдается общее снижение выручки в отрасли на 15% в 2023 году."
            
            Если критических событий не найдено, верни пустой JSON массив.
            Твой ответ должен быть ТОЛЬКО JSON массивом строк.

            Данные по компаниям отрасли:
            {companies_data_json}

            Результат анализа (JSON массив строк):
            '''
        )
        self.chain = self.prompt | self.llm

    def analyze(self, industry_name: str, companies: List[CompanyData]) -> List[str]:
        companies_data_json = json.dumps([c.dict(by_alias=True) for c in companies], ensure_ascii=False, indent=2)
        response = self.chain.invoke({
            "industry_name": industry_name,
            "companies_data_json": companies_data_json
        })
        return self._parse_response(response, "IndustryCriticalEventsAgent")

class IndustryGrowthPointsAgent(IndustryAnalysisAgent):
    """Агент для выявления лидеров и точек роста в отрасли."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["industry_name", "companies_data_json"],
            template='''
            Ты - отраслевой аналитик. Проанализируй предоставленные JSON-данные по компаниям в отрасли '{industry_name}'.
            Твоя задача - выявить лидеров и точки роста в отрасли.

            Точки роста и лидеры это:
            - Компании, показывающие самый высокий рост выручки или прибыли.
            - Лидеры отрасли по производительности (выручка на одного сотрудника).
            - Компании с наибольшей рентабельностью.

            Для каждого найденного факта, сформулируй краткий и ясный вывод в одну строку.
            Например: "ООО 'Лидер' показывает самый высокий рост выручки в отрасли (+35% за год)." или "ПАО 'Эффективность' - лидер по производительности труда с показателем 5 млн руб./чел."
            
            Если лидеров или явных точек роста не найдено, верни пустой JSON массив.
            Твой ответ должен быть ТОЛЬКО JSON массивом строк.

            Данные по компаниям отрасли:
            {companies_data_json}

            Результат анализа (JSON массив строк):
            '''
        )
        self.chain = self.prompt | self.llm

    def analyze(self, industry_name: str, companies: List[CompanyData]) -> List[str]:
        companies_data_json = json.dumps([c.dict(by_alias=True) for c in companies], ensure_ascii=False, indent=2)
        response = self.chain.invoke({
            "industry_name": industry_name,
            "companies_data_json": companies_data_json
        })
        return self._parse_response(response, "IndustryGrowthPointsAgent")

class IndustryAttentionZonesAgent(IndustryAnalysisAgent):
    """Агент для выявления зон внимания в отрасли."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["industry_name", "companies_data_json"],
            template='''
            Ты - отраслевой аналитик. Проанализируй предоставленные JSON-данные по компаниям в отрасли '{industry_name}'.
            Твоя задача - выявить общие для отрасли зоны внимания.

            Зоны внимания это:
            - Аномально высокая или низкая налоговая нагрузка (отношение суммы налогов к выручке) по сравнению с другими отраслями (если есть данные).
            - Общее снижение рентабельности в отрасли.

            Для каждой найденной зоны внимания, сформулируй краткий и ясный вывод в одну строку.
            Например: "Средняя налоговая нагрузка в отрасли составляет 25%, что выше среднего по экономике."
            
            Если зон внимания не найдено, верни пустой JSON массив.
            Твой ответ должен быть ТОЛЬКО JSON массивом строк.

            Данные по компаниям отрасли:
            {companies_data_json}

            Результат анализа (JSON массив строк):
            '''
        )
        self.chain = self.prompt | self.llm

    def analyze(self, industry_name: str, companies: List[CompanyData]) -> List[str]:
        companies_data_json = json.dumps([c.dict(by_alias=True) for c in companies], ensure_ascii=False, indent=2)
        response = self.chain.invoke({
            "industry_name": industry_name,
            "companies_data_json": companies_data_json
        })
        return self._parse_response(response, "IndustryAttentionZonesAgent")

class IndustryInterestingFactsAgent(IndustryAnalysisAgent):
    """Агент для выявления интересных фактов об отрасли."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["industry_name", "companies_data_json"],
            template='''
            Ты - отраслевой аналитик. Проанализируй предоставленные JSON-данные по компаниям в отрасли '{industry_name}'.
            Твоя задача - выявить интересные факты и структурные особенности отрасли.

            Интересные факты это:
            - Концентрация рынка: какую долю выручки формируют топ-3, топ-5, или топ-10 игроков.
            - Сравнение средних зарплат в отрасли с другими отраслями (если есть данные).

            Для каждого найденного факта, сформулируй краткий и ясный вывод в одну строку.
            Например: "Топ-3 компании в отрасли формируют более 75% от общего оборота." или "Средняя зарплата в отрасли на 15% выше, чем в среднем по экономике."
            
            Если интересных фактов не найдено, верни пустой JSON массив.
            Твой ответ должен быть ТОЛЬКО JSON массивом строк.

            Данные по компаниям отрасли:
            {companies_data_json}

            Результат анализа (JSON массив строк):
            '''
        )
        self.chain = self.prompt | self.llm

    def analyze(self, industry_name: str, companies: List[CompanyData]) -> List[str]:
        companies_data_json = json.dumps([c.dict(by_alias=True) for c in companies], ensure_ascii=False, indent=2)
        response = self.chain.invoke({
            "industry_name": industry_name,
            "companies_data_json": companies_data_json
        })
        return self._parse_response(response, "IndustryInterestingFactsAgent")