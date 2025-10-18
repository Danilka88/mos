from langchain_core.prompts import PromptTemplate
from typing import List
import json

from api.agents.base import BaseAnalysisAgent
from api.models import CompanyData

class GeoAnalysisAgent(BaseAnalysisAgent):
    """Базовый класс для агентов-аналитиков по географическому признаку."""
    def analyze(self, companies: List[CompanyData]) -> List[str]:
        """
        Анализирует данные по компаниям в географическом разрезе и возвращает список инсайтов.
        """
        raise NotImplementedError

class GeoCriticalEventsAgent(GeoAnalysisAgent):
    """Агент для выявления критических событий в географическом разрезе."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - гео-аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить критические события в географическом разрезе (Округ, Район).

            Критические события:
            - Округ или район с наибольшим падением инвестиций.
            - Район с наибольшим сокращением рабочих мест.

            Для каждого найденного события сформулируй краткий и ясный вывод в одну строку.
            Например: "В районе 'Печатники' наблюдается наибольшее падение инвестиций в основной капитал (-25%)."
            
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
        return self._parse_response(response, "GeoCriticalEventsAgent")

class GeoGrowthPointsAgent(GeoAnalysisAgent):
    """Агент для выявления точек роста в географическом разрезе."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - гео-аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить точки роста в географическом разрезе.

            Точки роста:
            - Формирование новых промышленных кластеров (концентрация предприятий одной отрасли в одном районе).
            - Районы, привлекающие наибольший объем инвестиций.

            Для каждого найденного факта сформулируй краткий и ясный вывод в одну строку.
            Например: "В районе 'Южное Бутово' формируется новый кластер предприятий отрасли 'IT'."
            
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
        return self._parse_response(response, "GeoGrowthPointsAgent")

class GeoAttentionZonesAgent(GeoAnalysisAgent):
    """Агент для выявления зон внимания в географическом разрезе."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - гео-аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить зоны внимания в географическом разрезе.

            Зоны внимания:
            - Районы или округа с низкой средней загрузкой производственных мощностей.
            - Неравномерное распределение предприятий по округам.

            Для каждой найденной зоны внимания сформулируй краткий и ясный вывод в одну строку.
            Например: "Предприятия в районе 'Капотня' имеют среднюю загрузку мощностей всего 30%."
            
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
        return self._parse_response(response, "GeoAttentionZonesAgent")

class GeoInterestingFactsAgent(GeoAnalysisAgent):
    """Агент для выявления интересных фактов в географическом разрезе."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - гео-аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить интересные факты в географическом разрезе.

            Интересные факты:
            - Концентрация экспортно-ориентированных предприятий в определенном округе.
            - Район с наибольшим количеством рабочих мест.

            Для каждого найденного факта сформулируй краткий и ясный вывод в одну строку.
            Например: "В 'Юго-Восточном' округе сконцентрировано 50% всех экспортных предприятий из выборки."
            
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
        return self._parse_response(response, "GeoInterestingFactsAgent")