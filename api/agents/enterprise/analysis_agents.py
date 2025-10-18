from langchain_core.prompts import PromptTemplate
from typing import List
import json

from api.agents.base import BaseAnalysisAgent
from api.models import CompanyData

class CriticalEventsAgent(BaseAnalysisAgent):
    """Агент для выявления критических событий."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["company_name", "company_data_json"],
            template='''
            Ты - финансовый аналитик. Проанализируй финансовые показатели компании "{company_name}".
            Твоя задача - выявить только критические события.

            Критические события это:
            - Появление убытков (чистая прибыль < 0) после периода прибыльности.
            - Рост убытков по сравнению с предыдущим годом.
            - Значительное падение годовой выручки (более чем на 20% по сравнению с предыдущим годом).
            - Значительное сокращение персонала (более чем на 15% за год).

            Проанализируй предоставленные JSON данные.
            Для каждого найденного критического события, сформулируй краткий и ясный вывод в одну строку.
            Например: "Резкое падение выручки в 2023 году на 30%." или "Появление убытков в 2024 году в размере -500 тыс. руб."
            
            Если критических событий не найдено, верни пустой JSON массив.
            Твой ответ должен быть ТОЛЬКО JSON массивом строк. Не добавляй никаких пояснений до или после JSON.

            Данные компании:
            {company_data_json}

            Результат анализа (JSON массив строк):
            '''
        )
        self.chain = self.prompt | self.llm

    def analyze(self, company: CompanyData) -> List[str]:
        company_data_json = company.json(by_alias=True, indent=2, ensure_ascii=False)
        response = self.chain.invoke({
            "company_name": company.name,
            "company_data_json": company_data_json
        })
        return self._parse_response(response, "CriticalEventsAgent")

class GrowthPointsAgent(BaseAnalysisAgent):
    """Агент для выявления точек роста."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["company_name", "company_data_json"],
            template='''
            Ты - финансовый аналитик. Проанализируй финансовые показатели компании "{company_name}".
            Твоя задача - выявить только точки роста.

            Точки роста это:
            - Значительный рост рентабельности по чистой прибыли (отношение чистой прибыли к выручке).
            - Устойчивый рост выручки на протяжении нескольких лет.
            - Рост объема экспорта.
            - Рост инвестиций.

            Проанализируй предоставленные JSON данные.
            Для каждой найденной точки роста, сформулируй краткий и ясный вывод в одну строку.
            Например: "Рост рентабельности по чистой прибыли до 15% в 2023 году." или "Стабильный рост выручки в среднем на 10% в год последние 3 года."
            
            Если точек роста не найдено, верни пустой JSON массив.
            Твой ответ должен быть ТОЛЬКО JSON массивом строк. Не добавляй никаких пояснений до или после JSON.

            Данные компании:
            {company_data_json}

            Результат анализа (JSON массив строк):
            '''
        )
        self.chain = self.prompt | self.llm

    def analyze(self, company: CompanyData) -> List[str]:
        company_data_json = company.json(by_alias=True, indent=2, ensure_ascii=False)
        response = self.chain.invoke({
            "company_name": company.name,
            "company_data_json": company_data_json
        })
        return self._parse_response(response, "GrowthPointsAgent")

class AttentionZonesAgent(BaseAnalysisAgent):
    """Агент для выявления зон внимания."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["company_name", "company_data_json"],
            template='''
            Ты - финансовый аналитик. Проанализируй финансовые показатели компании "{company_name}".
            Твоя задача - выявить только зоны внимания.

            Зоны внимания это:
            - Снижение рентабельности (затраты растут быстрее выручки).
            - Высокая зависимость от одного заказчика (если есть информация).
            - Рост долговой нагрузки (если есть данные о долгах).
            - Стагнация или незначительный рост ключевых показателей.

            Проанализируй предоставленные JSON данные.
            Для каждой найденной зоны внимания, сформулируй краткий и ясный вывод в одну строку.
            Например: "Снижение рентабельности по чистой прибыли с 10% до 5% за последний год."
            
            Если зон внимания не найдено, верни пустой JSON массив.
            Твой ответ должен быть ТОЛЬКО JSON массивом строк. Не добавляй никаких пояснений до или после JSON.

            Данные компании:
            {company_data_json}

            Результат анализа (JSON массив строк):
            '''
        )
        self.chain = self.prompt | self.llm

    def analyze(self, company: CompanyData) -> List[str]:
        company_data_json = company.json(by_alias=True, indent=2, ensure_ascii=False)
        response = self.chain.invoke({
            "company_name": company.name,
            "company_data_json": company_data_json
        })
        return self._parse_response(response, "AttentionZonesAgent")

class InterestingFactsAgent(BaseAnalysisAgent):
    """Агент для выявления интересных фактов."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["company_name", "company_data_json"],
            template='''
            Ты - финансовый аналитик. Проанализируй финансовые показатели и описание компании "{company_name}".
            Твоя задача - выявить интересные или рекордные факты.

            Интересные факты это:
            - Рекордная выручка или прибыль за всю историю наблюдений в предоставленных данных.
            - Самый высокий рост показателя за один год.
            - Уникальные продукты или услуги (если есть информация в описании).
            - Лидерство в отрасли по какому-либо показателю.

            Проанализируй предоставленные JSON данные.
            Для каждого найденного факта, сформулируй краткий и ясный вывод в одну строку.
            Например: "В 2022 году компания достигла рекордной выручки в 1.2 млрд руб." или "НПО 'Квант' - лидер по росту выручки на сотрудника (+25%)".
            
            Если интересных фактов не найдено, верни пустой JSON массив.
            Твой ответ должен быть ТОЛЬКО JSON массивом строк. Не добавляй никаких пояснений до или после JSON.

            Данные компании:
            {company_data_json}

            Результат анализа (JSON массив строк):
            '''
        )
        self.chain = self.prompt | self.llm

    def analyze(self, company: CompanyData) -> List[str]:
        company_data_json = company.json(by_alias=True, indent=2, ensure_ascii=False)
        response = self.chain.invoke({
            "company_name": company.name,
            "company_data_json": company_data_json
        })
        return self._parse_response(response, "InterestingFactsAgent")
