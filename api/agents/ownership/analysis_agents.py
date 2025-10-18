from langchain_core.prompts import PromptTemplate
from typing import List
import json

from api.agents.base import BaseAnalysisAgent
from api.models import CompanyData

class OwnershipAnalysisAgent(BaseAnalysisAgent):
    """Базовый класс для агентов анализа структуры владения."""
    def analyze(self, companies: List[CompanyData]) -> List[str]:
        """
        Анализирует данные по структуре владения компаний и возвращает список инсайтов.
        """
        raise NotImplementedError

class OwnershipCriticalEventsAgent(OwnershipAnalysisAgent):
    """Агент для выявления критических событий в структуре владения."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - корпоративный аналитик. Проанализируй предоставленные JSON-данные по компаниям и их связям.
            Твоя задача - выявить критические события, связанные со структурой владения, используя поля 'Головная организация' и финансовые показатели.

            Критические события:
            - Признаки банкротства или серьезных финансовых проблем у материнской компании (например, отрицательная чистая прибыль, большое падение выручки).

            Для каждого найденного события сформулируй краткий и ясный вывод в одну строку.
            Например: "Головная компания 'X' для компании 'Y' имеет признаки банкротства (отрицательные чистые активы)."
            
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
        return self._parse_response(response, "OwnershipCriticalEventsAgent")

class OwnershipGrowthPointsAgent(OwnershipAnalysisAgent):
    """Агент для выявления точек роста в структуре владения."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - корпоративный аналитик. Проанализируй предоставленные JSON-данные по компаниям и их связям.
            Твоя задача - выявить точки роста, связанные с интеграцией внутри холдинга.

            Точки роста:
            - Производственная или технологическая интеграция между дочерней и головной компаниями.
            - Положительное влияние сильной материнской компании на дочернюю.

            Для каждого найденного факта сформулируй краткий и ясный вывод в одну строку.
            Например: "Наблюдается производственная интеграция между 'Y' и ее головной компанией 'X'."
            
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
        return self._parse_response(response, "OwnershipGrowthPointsAgent")

class OwnershipAttentionZonesAgent(OwnershipAnalysisAgent):
    """Агент для выявления зон внимания в структуре владения."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - корпоративный аналитик. Проанализируй предоставленные JSON-данные по компаниям и их связям.
            Твоя задача - выявить зоны внимания, связанные со структурой владения.

            Зоны внимания:
            - Высокая финансовая или операционная зависимость дочерней компании от головной.
            - Сложная или непрозрачная структура владения.

            Для каждой найденной зоны внимания сформулируй краткий и ясный вывод в одну строку.
            Например: "Компания 'Y' полностью финансово зависит от своей материнской компании 'X'."
            
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
        return self._parse_response(response, "OwnershipAttentionZonesAgent")

class OwnershipInterestingFactsAgent(OwnershipAnalysisAgent):
    """Агент для выявления интересных фактов о структуре владения."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - корпоративный аналитик. Проанализируй предоставленные JSON-данные по компаниям и их связям.
            Твоя задача - выявить интересные факты, связанные со структурой владения.

            Интересные факты:
            - Наличие транснациональных структур владения (головная компания зарегистрирована в другой стране).
            - Вхождение компании в крупный известный холдинг.

            Для каждого найденного факта сформулируй краткий и ясный вывод в одну строку.
            Например: "Компания 'A' является частью транснационального холдинга с материнской компанией 'B' (Германия)."
            
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
        return self._parse_response(response, "OwnershipInterestingFactsAgent")