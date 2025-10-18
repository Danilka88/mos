from langchain_core.prompts import PromptTemplate
from typing import List
import json

from api.agents.base import BaseAnalysisAgent
from api.models import CompanyData

class TaxAnalysisAgent(BaseAnalysisAgent):
    """Базовый класс для агентов анализа налоговой нагрузки."""
    def analyze(self, companies: List[CompanyData]) -> List[str]:
        """
        Анализирует данные по налоговой нагрузке и возвращает список инсайтов.
        """
        raise NotImplementedError

class TaxCriticalEventsAgent(TaxAnalysisAgent):
    """Агент для выявления критических событий в налоговой нагрузке."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - налоговый аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить критические события, связанные с налогами.

            Критические события:
            - Рост общей налоговой нагрузки (сумма налогов / выручка) более чем на 30% за год.

            Для каждого найденного события сформулируй краткий и ясный вывод в одну строку.
            Например: "Общая налоговая нагрузка компании 'X' выросла на 40% в 2023 году."
            
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
        return self._parse_response(response, "TaxCriticalEventsAgent")

class TaxGrowthPointsAgent(TaxAnalysisAgent):
    """Агент для выявления точек роста в налогообложении."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - налоговый аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить признаки налоговой оптимизации.

            Точки роста (оптимизация):
            - Снижение налоговой нагрузки (сумма налогов / выручка) при росте или стабильности выручки и прибыли.

            Для каждого найденного факта сформулируй краткий и ясный вывод в одну строку.
            Например: "Компания 'Y' снизила налоговую нагрузку на 5% при росте прибыли на 15%, что может говорить об успешной оптимизации."
            
            Если признаков оптимизации не найдено, верни пустой JSON массив.
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
        return self._parse_response(response, "TaxGrowthPointsAgent")

class TaxAttentionZonesAgent(TaxAnalysisAgent):
    """Агент для выявления зон внимания в налоговой нагрузке."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - налоговый аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить зоны внимания в структуре налогов.

            Зоны внимания:
            - Рост доли НДФЛ в общей сумме налогов при одновременном снижении или стагнации Фонда оплаты труда (ФОТ).

            Для каждой найденной зоны внимания сформулируй краткий и ясный вывод в одну строку.
            Например: "У компании 'Z' доля НДФЛ в налогах выросла, а ФОТ снизился, что требует дополнительного анализа."
            
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
        return self._parse_response(response, "TaxAttentionZonesAgent")

class TaxInterestingFactsAgent(TaxAnalysisAgent):
    """Агент для выявления интересных фактов о налоговой нагрузке."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - налоговый аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить интересные факты, сравнивая налоговую нагрузку компаний.

            Интересные факты:
            - Налог на прибыль компании значительно ниже или выше среднего по отрасли.
            - Аномально высокая или низкая доля определенного налога (на имущество, землю, транспорт) в общей структуре налогов компании по сравнению с другими.

            Для каждого найденного факта сформулируй краткий и ясный вывод в одну строку.
            Например: "Налог на прибыль компании 'A' составляет 10% от прибыли, что на 5% ниже среднего по отрасли."
            
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
        return self._parse_response(response, "TaxInterestingFactsAgent")