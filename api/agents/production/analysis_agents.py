from langchain_core.prompts import PromptTemplate
from typing import List
import json

from api.agents.base import BaseAnalysisAgent
from api.models import CompanyData

class ProductionAnalysisAgent(BaseAnalysisAgent):
    """Базовый класс для агентов анализа производственных мощностей."""
    def analyze(self, companies: List[CompanyData]) -> List[str]:
        """
        Анализирует данные по производственным мощностям и возвращает список инсайтов.
        """
        raise NotImplementedError

class ProductionCriticalEventsAgent(ProductionAnalysisAgent):
    """Агент для выявления критических событий в производственных мощностях."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - промышленный аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить критические события, связанные с производственными мощностями.

            Критические события:
            - Уровень загрузки производственных мощностей ниже 50%.

            Для каждого найденного события сформулируй краткий и ясный вывод в одну строку.
            Например: "Уровень загрузки мощностей компании 'X' составляет всего 45%."
            
            Если критических событий не найдено, верни пустой JSON массив.
            Твой ответ должен быть ТОЛЬКО JSON массивом строк.

            Данные по компаниям:
            {companies_data_json}

            Результат анализа (JSON массив строк):
            '''
        )
        self.chain = self.prompt | self.llm

    def analyze(self, companies: List[CompanyData]) -> List[str]:
        companies_data_json = json.dumps([c.dict(by_alias=True) for c in companies], ensure_ascii=False, indent=2)
        response = self.chain.invoke({"companies_data_json": companies_data_json})
        return self._parse_response(response, "ProductionCriticalEventsAgent")

class ProductionGrowthPointsAgent(ProductionAnalysisAgent):
    """Агент для выявления точек роста в производственных мощностях."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - промышленный аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить точки роста, связанные с производственными мощностями.

            Точки роста:
            - Запуск новой производственной линии (если есть информация в описании).
            - Расширение производственных площадей.

            Для каждого найденного факта сформулируй краткий и ясный вывод в одну строку.
            Например: "Компания 'Y' сообщила о запуске новой производственной линии в 2023 году."
            
            Если точек роста не найдено, верни пустой JSON массив.
            Твой ответ должен быть ТОЛЬКО JSON массивом строк.

            Данные по компаниям:
            {companies_data_json}

            Результат анализа (JSON массив строк):
            '''
        )
        self.chain = self.prompt | self.llm

    def analyze(self, companies: List[CompanyData]) -> List[str]:
        companies_data_json = json.dumps([c.dict(by_alias=True) for c in companies], ensure_ascii=False, indent=2)
        response = self.chain.invoke({"companies_data_json": companies_data_json})
        return self._parse_response(response, "ProductionGrowthPointsAgent")

class ProductionAttentionZonesAgent(ProductionAnalysisAgent):
    """Агент для выявления зон внимания в производственных мощностях."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - промышленный аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить зоны внимания, связанные с производственными мощностями.

            Зоны внимания:
            - Информация об использовании устаревших производственных площадей или технологий.

            Для каждой найденной зоны внимания сформулируй краткий и ясный вывод в одну строку.
            Например: "Производственные площади компании 'Z' не модернизировались с 1980 года."
            
            Если зон внимания не найдено, верни пустой JSON массив.
            Твой ответ должен быть ТОЛЬКО JSON массивом строк.

            Данные по компаниям:
            {companies_data_json}

            Результат анализа (JSON массив строк):
            '''
        )
        self.chain = self.prompt | self.llm

    def analyze(self, companies: List[CompanyData]) -> List[str]:
        companies_data_json = json.dumps([c.dict(by_alias=True) for c in companies], ensure_ascii=False, indent=2)
        response = self.chain.invoke({"companies_data_json": companies_data_json})
        return self._parse_response(response, "ProductionAttentionZonesAgent")

class ProductionInterestingFactsAgent(ProductionAnalysisAgent):
    """Агент для выявления интересных фактов о производственных мощностях."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - промышленный аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить интересные факты, связанные с производимой продукцией.

            Интересные факты:
            - Переход компании на выпуск стандартизированной продукции (на основе поля 'Стандартизированная продукция').
            - Производство уникальной или высокотехнологичной продукции.

            Для каждого найденного факта сформулируй краткий и ясный вывод в одну строку.
            Например: "Компания 'A' перешла на выпуск стандартизированной продукции, что может указывать на новую стратегию."
            
            Если интересных фактов не найдено, верни пустой JSON массив.
            Твой ответ должен быть ТОЛЬКО JSON массивом строк.

            Данные по компаниям:
            {companies_data_json}

            Результат анализа (JSON массив строк):
            '''
        )
        self.chain = self.prompt | self.llm

    def analyze(self, companies: List[CompanyData]) -> List[str]:
        companies_data_json = json.dumps([c.dict(by_alias=True) for c in companies], ensure_ascii=False, indent=2)
        response = self.chain.invoke({"companies_data_json": companies_data_json})
        return self._parse_response(response, "ProductionInterestingFactsAgent")