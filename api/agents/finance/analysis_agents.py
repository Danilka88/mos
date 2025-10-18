from langchain_core.prompts import PromptTemplate
from typing import List
import json

from api.agents.base import BaseAnalysisAgent
from api.models import CompanyData

class FinanceAnalysisAgent(BaseAnalysisAgent):
    """Базовый класс для агентов финансового анализа (инвестиции и экспорт)."""
    def analyze(self, companies: List[CompanyData]) -> List[str]:
        """
        Анализирует данные по инвестициям и экспорту и возвращает список инсайтов.
        """
        raise NotImplementedError

class FinanceCriticalEventsAgent(FinanceAnalysisAgent):
    """Агент для выявления критических событий в инвестициях и экспорте."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - финансовый аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить критические события, связанные с инвестициями и экспортом.

            Критические события:
            - Резкое падение или полное прекращение экспортных поставок у компании.
            - Значительное снижение объема инвестиций в основной капитал.

            Для каждого найденного события сформулируй краткий и ясный вывод в одну строку.
            Например: "Экспорт компании 'X' упал на 90% в 2023 году."
            
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
        return self._parse_response(response, "FinanceCriticalEventsAgent")

class FinanceGrowthPointsAgent(FinanceAnalysisAgent):
    """Агент для выявления точек роста в инвестициях и экспорте."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - финансовый аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить точки роста, связанные с инвестициями и экспортом.

            Точки роста:
            - Выход компании на новые экспортные рынки (появление новых стран в списке 'Перечень государств куда экспортируется продукция').
            - Значительный рост объема экспорта или инвестиций.

            Для каждого найденного факта сформулируй краткий и ясный вывод в одну строку.
            Например: "Компания 'Y' вышла на новый рынок: в списке экспортных направлений появилась 'Бразилия'."
            
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
        return self._parse_response(response, "FinanceGrowthPointsAgent")

class FinanceAttentionZonesAgent(FinanceAnalysisAgent):
    """Агент для выявления зон внимания в инвестициях и экспорте."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - финансовый аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить зоны внимания, связанные с экспортом.

            Зоны внимания:
            - Зависимость экспорта компании от одного-двух ключевых импортёров (малое количество стран в списке 'Перечень государств куда экспортируется продукция').

            Для каждой найденной зоны внимания сформулируй краткий и ясный вывод в одну строку.
            Например: "Экспорт компании 'Z' сильно зависит от одного рынка ('Казахстан')."
            
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
        return self._parse_response(response, "FinanceAttentionZonesAgent")

class FinanceInterestingFactsAgent(FinanceAnalysisAgent):
    """Агент для выявления интересных фактов об инвестициях и экспорте."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - финансовый аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить интересные факты, связанные с экспортом.

            Интересные факты:
            - Компании с очень широкой географией экспорта (более 10 стран).
            - Компании, экспортирующие в редкие или экзотические страны.

            Для каждого найденного факта сформулируй краткий и ясный вывод в одну строку.
            Например: "Компания 'A' является лидером по диверсификации экспорта, поставляя продукцию в более чем 15 стран."
            
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
        return self._parse_response(response, "FinanceInterestingFactsAgent")