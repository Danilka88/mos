from langchain_core.prompts import PromptTemplate
from typing import List
import json

from api.agents.base import BaseAnalysisAgent
from api.models import CompanyData

class ProductAnalysisAgent(BaseAnalysisAgent):
    """Базовый класс для агентов анализа по видам продукции."""
    def analyze(self, companies: List[CompanyData]) -> List[str]:
        """
        Анализирует данные по продуктам компаний и возвращает список инсайтов.
        """
        raise NotImplementedError

class ProductCriticalEventsAgent(ProductAnalysisAgent):
    """Агент для выявления критических событий, связанных с продукцией."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - продуктовый аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить критические события, связанные с продукцией, используя поля 'Перечень производимой продукции по кодам ОКПД 2' и 'Название (виды производимой продукции)'.

            Критические события:
            - Исчезновение продукта с рынка (если есть информация об этом в описании или новостях).
            - Резкое падение спроса на определенный вид продукции (если есть косвенные данные).

            Для каждого найденного события сформулируй краткий и ясный вывод в одну строку.
            Например: "Компания 'X' прекратила производство продукта с кодом ОКПД2 20.42.15.129 в 2023 году."
            
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
        return self._parse_response(response, "ProductCriticalEventsAgent")

class ProductGrowthPointsAgent(ProductAnalysisAgent):
    """Агент для выявления точек роста, связанных с продукцией."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - продуктовый аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить точки роста, связанные с продукцией.

            Точки роста:
            - Запуск нового успешного продукта, который вошел в топ продаж.
            - Расширение продуктовой линейки.

            Для каждого найденного факта сформулируй краткий и ясный вывод в одну строку.
            Например: "Новый продукт 'Инновация-5' компании 'Y' вошел в топ-3 по продажам в своем сегменте."
            
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
        return self._parse_response(response, "ProductGrowthPointsAgent")

class ProductAttentionZonesAgent(ProductAnalysisAgent):
    """Агент для выявления зон внимания, связанных с продукцией."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - продуктовый аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить зоны внимания, связанные с продукцией.

            Зоны внимания:
            - Продуктовые сегменты с предположительно высокой себестоимостью (например, низкая рентабельность компании при фокусе на этом сегменте).
            - Устаревшие продукты или технологии.

            Для каждой найденной зоны внимания сформулируй краткий и ясный вывод в одну строку.
            Например: "Сегмент продукции 'W' у компании 'Z' имеет низкую рентабельность, что может говорить о высокой себестоимости."
            
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
        return self._parse_response(response, "ProductAttentionZonesAgent")

class ProductInterestingFactsAgent(ProductAnalysisAgent):
    """Агент для выявления интересных фактов о продукции."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["companies_data_json"],
            template='''
            Ты - продуктовый аналитик. Проанализируй предоставленные JSON-данные по компаниям.
            Твоя задача - выявить интересные факты, связанные с продукцией.

            Интересные факты:
            - Экспорт редкого или уникального товара (на основе полей, связанных с экспортом и продукцией).
            - Производство продукции по уникальному коду ОКПД2.

            Для каждого найденного факта сформулируй краткий и ясный вывод в одну строку.
            Например: "Компания 'A' является единственным экспортером продукта 'Суперсплав-X' в регионе."
            
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
        return self._parse_response(response, "ProductInterestingFactsAgent")