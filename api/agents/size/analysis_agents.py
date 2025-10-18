from langchain_core.prompts import PromptTemplate
from typing import List
import json

from api.agents.base import BaseAnalysisAgent
from api.models import CompanyData

class SizeAnalysisAgent(BaseAnalysisAgent):
    """Базовый класс для агентов-аналитиков по размеру предприятий."""
    def analyze(self, companies: List[CompanyData]) -> List[str]:
        """
        Анализирует данные по компаниям, сгруппированным по размеру, и возвращает список инсайтов.
        """
        raise NotImplementedError

class SizeCriticalEventsAgent(SizeAnalysisAgent):
    """Агент для выявления критических событий в разрезе размера предприятий."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - макроэкономический аналитик. Проанализируй предоставленные JSON-данные по компаниям. 
            Твоя задача - выявить критические события, сгруппировав компании по размеру (микро, малые, средние, крупные) на основе полей 'Размер предприятия (по выручке)' и 'Размер предприятия (по численности)'.

            Критические события:
            - Группа предприятий (например, 'микро') показывает общее снижение рентабельности.
            - В одной из групп наблюдается массовое сокращение персонала.

            Для каждого найденного события, сформулируй краткий и ясный вывод в одну строку.
            Например: "Микропредприятия показывают снижение средней рентабельности на 5% в 2023 году."
            
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
        return self._parse_response(response, "SizeCriticalEventsAgent")

class SizeGrowthPointsAgent(SizeAnalysisAgent):
    """Агент для выявления точек роста в разрезе размера предприятий."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - макроэкономический аналитик. Проанализируй предоставленные JSON-данные по компаниям. 
            Твоя задача - выявить точки роста, сгруппировав компании по размеру (микро, малые, средние, крупные).

            Точки роста:
            - Какая-то из групп предприятий (например, 'малые') показывает опережающий рост экспорта.
            - В какой-то из групп наблюдается самый быстрый рост выручки.

            Для каждого найденного факта, сформулируй краткий и ясный вывод в одну строку.
            Например: "Малые предприятия демонстрируют самый быстрый рост экспорта, в среднем +30% за год."
            
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
        return self._parse_response(response, "SizeGrowthPointsAgent")

class SizeAttentionZonesAgent(SizeAnalysisAgent):
    """Агент для выявления зон внимания в разрезе размера предприятий."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - макроэкономический аналитик. Проанализируй предоставленные JSON-данные по компаниям. 
            Твоя задача - выявить зоны внимания, сгруппировав компании по размеру (микро, малые, средние, крупные).

            Зоны внимания:
            - Снижение производительности труда (выручка на сотрудника) в одной из групп.
            - Рост налоговой нагрузки в одной из групп опережает рост их выручки.

            Для каждой найденной зоны внимания, сформулируй краткий и ясный вывод в одну строку.
            Например: "Средние предприятия показывают снижение производительности труда на 10%."
            
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
        return self._parse_response(response, "SizeAttentionZonesAgent")

class SizeInterestingFactsAgent(SizeAnalysisAgent):
    """Агент для выявления интересных фактов в разрезе размера предприятий."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - макроэкономический аналитик. Проанализируй предоставленные JSON-данные по компаниям. 
            Твоя задача - выявить интересные факты, сгруппировав компании по размеру (микро, малые, средние, крупные).

            Интересные факты:
            - Вклад каждой группы в общие налоговые поступления.
            - Доля каждой группы в общей выручке.

            Для каждого найденного факта, сформулируй краткий и ясный вывод в одну строку.
            Например: "Крупные компании обеспечивают 80% всех налоговых поступлений среди проанализированных предприятий."
            
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
        return self._parse_response(response, "SizeInterestingFactsAgent")