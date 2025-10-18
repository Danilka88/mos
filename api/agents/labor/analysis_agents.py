from langchain_core.prompts import PromptTemplate
from typing import List
import json

from api.agents.base import BaseAnalysisAgent
from api.models import CompanyData

class LaborAnalysisAgent(BaseAnalysisAgent):
    """Базовый класс для агентов-аналитиков по трудовым ресурсам."""
    def analyze(self, companies: List[CompanyData]) -> List[str]:
        """
        Анализирует данные по трудовым ресурсам компаний и возвращает список инсайтов.
        """
        raise NotImplementedError

class LaborCriticalEventsAgent(LaborAnalysisAgent):
    """Агент для выявления критических событий в трудовых ресурсах."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - HR-аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить критические события, связанные с трудовыми ресурсами.

            Критические события:
            - Значительное снижение среднесписочной численности сотрудников в компании или в целом по группе компаний.

            Для каждого найденного события сформулируй краткий и ясный вывод в одну строку.
            Например: "В компании X наблюдается сокращение персонала на 20% за последний год."
            
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
        return self._parse_response(response, "LaborCriticalEventsAgent")

class LaborGrowthPointsAgent(LaborAnalysisAgent):
    """Агент для выявления точек роста в трудовых ресурсах."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - HR-аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить точки роста, связанные с трудовыми ресурсами.

            Точки роста:
            - Рост производительности труда (отношение Выручки к Среднесписочной численности).
            - Определение компаний-лидеров по производительности труда.

            Для каждого найденного факта сформулируй краткий и ясный вывод в одну строку.
            Например: "Компания Y лидирует по росту производительности труда (+25%)."
            
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
        return self._parse_response(response, "LaborGrowthPointsAgent")

class LaborAttentionZonesAgent(LaborAnalysisAgent):
    """Агент для выявления зон внимания в трудовых ресурсах."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - HR-аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить зоны внимания, связанные с трудовыми ресурсами.

            Зоны внимания:
            - Рост Фонда оплаты труда (ФОТ) без соответствующего увеличения выручки.
            - Снижение средней зарплаты в компании или отрасли.

            Для каждой найденной зоны внимания сформулируй краткий и ясный вывод в одну строку.
            Например: "В компании Z ФОТ вырос на 15%, в то время как выручка осталась на прежнем уровне."
            
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
        return self._parse_response(response, "LaborAttentionZonesAgent")

class LaborInterestingFactsAgent(LaborAnalysisAgent):
    """Агент для выявления интересных фактов о трудовых ресурсах."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - HR-аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить интересные факты, связанные с трудовыми ресурсами.

            Интересные факты:
            - Компания или отрасль с самой высокой средней зарплатой.
            - Компания с самым большим штатом сотрудников.

            Для каждого найденного факта сформулируй краткий и ясный вывод в одну строку.
            Например: "Компания A предлагает самую высокую среднюю зарплату в отрасли, превышающую средний показатель на 40%."
            
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
        return self._parse_response(response, "LaborInterestingFactsAgent")