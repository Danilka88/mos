from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from typing import Dict, Any, List
import json

class DataExtractionAgent:
    def __init__(self, ollama_model: str = "gemma3:4b"):
        self.llm = OllamaLLM(model=ollama_model)

    def extract_data(self, text: str, fields: List[str]) -> Dict[str, Any]:
        raise NotImplementedError

class RevenueAgent(DataExtractionAgent):
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Извлеки из следующего текста значения для выручки предприятия по годам с 2017 по 2025. 
            Если значение не найдено для конкретного года, укажи null. 
            Формат вывода должен быть JSON-объектом, где ключи - это полные названия полей из списка ниже, а значения - извлеченные числа (float).
            Список полей:
            - Выручка предприятия, тыс. руб. 2017
            - Выручка предприятия, тыс. руб. 2018
            - Выручка предприятия, тыс. руб. 2019
            - Выручка предприятия, тыс. руб. 2020
            - Выручка предприятия, тыс. руб. 2021
            - Выручка предприятия, тыс. руб. 2022
            - Выручка предприятия, тыс. руб. 2023
            - Выручка предприятия, тыс. руб. 2024
            - Выручка предприятия, тыс. руб. 2025

            Пример:
            Текст: "Выручка за 2020 год составила 15000 тыс. руб., за 2021 - 16000 тыс. руб."
            Вывод: { "Выручка предприятия, тыс. руб. 2020": 15000.0, "Выручка предприятия, тыс. руб. 2021": 16000.0, "Выручка предприятия, тыс. руб. 2017": null, ... }

            Текст: {text}
            Вывод:
            """
        )
        self.chain = self.prompt | self.llm

    def extract_data(self, text: str, fields: List[str] = None) -> Dict[str, Any]:
        response = self.chain.invoke({"text": text})
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON от RevenueAgent: {response}")
            return {field: None for field in fields if field.startswith("Выручка предприятия")} 

class NetProfitAgent(DataExtractionAgent):
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Извлеки из следующего текста значения для чистой прибыли (убытка) предприятия по годам с 2017 по 2025. 
            Если значение не найдено для конкретного года, укажи null. 
            Формат вывода должен быть JSON-объектом, где ключи - это полные названия полей из списка ниже, а значения - извлеченные числа (float).
            Список полей:
            - Чистая прибыль (убыток),тыс. руб. 2017
            - Чистая прибыль (убыток),тыс. руб. 2018
            - Чистая прибыль (убыток),тыс. руб. 2019
            - Чистая прибыль (убыток),тыс. руб. 2020
            - Чистая прибыль (убыток),тыс. руб. 2021
            - Чистая прибыль (убыток),тыс. руб. 2022
            - Чистая прибыль (убыток),тыс. руб. 2023
            - Чистая прибыль (убыток),тыс. руб. 2024
            - Чистая прибыль (убыток),тыс. руб. 2025

            Пример:
            Текст: "Чистая прибыль в 2022 году составила 5000 тыс. руб., в 2023 - 6000 тыс. руб."
            Вывод: { "Чистая прибыль (убыток),тыс. руб. 2022": 5000.0, "Чистая прибыль (убыток),тыс. руб. 2023": 6000.0, "Чистая прибыль (убыток),тыс. руб. 2017": null, ... }

            Текст: {text}
            Вывод:
            """
        )
        self.chain = self.prompt | self.llm

    def extract_data(self, text: str, fields: List[str] = None) -> Dict[str, Any]:
        response = self.chain.invoke({"text": text})
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON от NetProfitAgent: {response}")
            return {field: None for field in fields if field.startswith("Чистая прибыль (убыток)")} 

class EmployeeCountAgent(DataExtractionAgent):
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Извлеки из следующего текста значения для среднесписочной численности персонала (всего по компании) по годам с 2017 по 2025. 
            Если значение не найдено для конкретного года, укажи null. 
            Формат вывода должен быть JSON-объектом, где ключи - это полные названия полей из списка ниже, а значения - извлеченные целые числа (int).
            Список полей:
            - Среднесписочная численность персонала (всего по компании), чел 2017
            - Среднесписочная численность персонала (всего по компании), чел 2018
            - Среднесписочная численность персонала (всего по компании), чел 2019
            - Среднесписочная численность персонала (всего по компании), чел 2020
            - Среднесписочная численность персонала (всего по компании), чел 2021
            - Среднесписочная численность персонала (всего по компании), чел 2022
            - Среднесписочная численность персонала (всего по компании), чел 2023
            - Среднесписочная численность персонала (всего по компании), чел 2024
            - Среднесписочная численность персонала (всего по компании), чел 2025

            Пример:
            Текст: "В 2019 году работало 120 человек, в 2020 - 130."
            Вывод: { "Среднесписочная численность персонала (всего по компании), чел 2019": 120, "Среднесписочная численность персонала (всего по компании), чел 2020": 130, ... }

            Текст: {text}
            Вывод:
            """
        )
        self.chain = self.prompt | self.llm

    def extract_data(self, text: str, fields: List[str] = None) -> Dict[str, Any]:
        response = self.chain.invoke({"text": text})
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON от EmployeeCountAgent: {response}")
            return {field: None for field in fields if field.startswith("Среднесписочная численность персонала (всего по компании)")} 

class MoscowEmployeeCountAgent(DataExtractionAgent):
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Извлеки из следующего текста значения для среднесписочной численности персонала, работающего в Москве, по годам с 2017 по 2025. 
            Если значение не найдено для конкретного года, укажи null. 
            Формат вывода должен быть JSON-объектом, где ключи - это полные названия полей из списка ниже, а значения - извлеченные целые числа (int).
            Список полей:
            - Среднесписочная численность персонала, работающего в Москве, чел 2017
            - Среднесписочная численность персонала, работающего в Москве, чел 2018
            - Среднесписочная численность персонала, работающего в Москве, чел 2019
            - Среднесписочная численность персонала, работающего в Москве, чел 2020
            - Среднесписочная численность персонала, работающего в Москве, чел 2021
            - Среднесписочная численность персонала, работающего в Москве, чел 2022
            - Среднесписочная численность персонала, работающего в Москве, чел 2023
            - Среднесписочная численность персонала, работающего в Москве, чел 2024
            - Среднесписочная численность персонала, работающего в Москве, чел 2025

            Пример:
            Текст: "В Москве в 2021 году работало 50 человек, в 2022 - 55."
            Вывод: { "Среднесписочная численность персонала, работающего в Москве, чел 2021": 50, "Среднесписочная численность персонала, работающего в Москве, чел 2022": 55, ... }

            Текст: {text}
            Вывод:
            """
        )
        self.chain = self.prompt | self.llm

    def extract_data(self, text: str, fields: List[str] = None) -> Dict[str, Any]:
        response = self.chain.invoke({"text": text})
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON от MoscowEmployeeCountAgent: {response}")
            return {field: None for field in fields if field.startswith("Среднесписочная численность персонала, работающего в Москве")} 

class PayrollTotalAgent(DataExtractionAgent):
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Извлеки из следующего текста значения для фонда оплаты труда всех сотрудников организации по годам с 2017 по 2025. 
            Если значение не найдено для конкретного года, укажи null. 
            Формат вывода должен быть JSON-объектом, где ключи - это полные названия полей из списка ниже, а значения - извлеченные числа (float).
            Список полей:
            - Фонд оплаты труда всех сотрудников организации, тыс. руб 2017
            - Фонд оплаты труда всех сотрудников организации, тыс. руб 2018
            - Фонд оплаты труда всех сотрудников организации, тыс. руб 2019
            - Фонд оплаты труда всех сотрудников организации, тыс. руб 2020
            - Фонд оплаты труда всех сотрудников организации, тыс. руб 2021
            - Фонд оплаты труда всех сотрудников организации, тыс. руб 2022
            - Фонд оплаты труда всех сотрудников организации, тыс. руб 2023
            - Фонд оплаты труда всех сотрудников организации, тыс. руб 2024
            - Фонд оплаты труда всех сотрудников организации, тыс. руб 2025

            Пример:
            Текст: "ФОТ за 2018 год составил 10000 тыс. руб., за 2019 - 11000 тыс. руб."
            Вывод: { "Фонд оплаты труда всех сотрудников организации, тыс. руб 2018": 10000.0, "Фонд оплаты труда всех сотрудников организации, тыс. руб 2019": 11000.0, ... }

            Текст: {text}
            Вывод:
            """
        )
        self.chain = self.prompt | self.llm

    def extract_data(self, text: str, fields: List[str] = None) -> Dict[str, Any]:
        response = self.chain.invoke({"text": text})
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON от PayrollTotalAgent: {response}")
            return {field: None for field in fields if field.startswith("Фонд оплаты труда всех сотрудников организации")} 

class PayrollMoscowAgent(DataExtractionAgent):
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Извлеки из следующего текста значения для фонда оплаты труда сотрудников, работающих в Москве, по годам с 2017 по 2025. 
            Если значение не найдено для конкретного года, укажи null. 
            Формат вывода должен быть JSON-объектом, где ключи - это полные названия полей из списка ниже, а значения - извлеченные числа (float).
            Список полей:
            - Фонд оплаты труда  сотрудников, работающих в Москве, тыс. руб 2017
            - Фонд оплаты труда  сотрудников, работающих в Москве, тыс. руб 2018
            - Фонд оплаты труда  сотрудников, работающих в Москве, тыс. руб 2019
            - Фонд оплаты труда  сотрудников, работающих в Москве, тыс. руб 2020
            - Фонд оплаты труда  сотрудников, работающих в Москве, тыс. руб. 2021
            - Фонд оплаты труда  сотрудников, работающих в Москве, тыс. руб. 2022
            - Фонд оплаты труда  сотрудников, работающих в Москве, тыс. руб. 2023
            - Фонд оплаты труда  сотрудников, работающих в Москве, тыс. руб. 2024
            - Фонд оплаты труда  сотрудников, работающих в Москве, тыс. руб. 2025

            Пример:
            Текст: "ФОТ московских сотрудников за 2020 год составил 7000 тыс. руб., за 2021 - 7500 тыс. руб."
            Вывод: { "Фонд оплаты труда  сотрудников, работающих в Москве, тыс. руб 2020": 7000.0, "Фонд оплаты труда  сотрудников, работающих в Москве, тыс. руб. 2021": 7500.0, ... }

            Текст: {text}
            Вывод:
            """
        )
        self.chain = self.prompt | self.llm

    def extract_data(self, text: str, fields: List[str] = None) -> Dict[str, Any]:
        response = self.chain.invoke({"text": text})
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON от PayrollMoscowAgent: {response}")
            return {field: None for field in fields if field.startswith("Фонд оплаты труда  сотрудников, работающих в Москве")} 

class AvgSalaryTotalAgent(DataExtractionAgent):
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Извлеки из следующего текста значения для средней з.п. всех сотрудников организации по годам с 2017 по 2025. 
            Если значение не найдено для конкретного года, укажи null. 
            Формат вывода должен быть JSON-объектом, где ключи - это полные названия полей из списка ниже, а значения - извлеченные числа (float).
            Список полей:
            - Средняя з.п. всех сотрудников организации,  тыс.руб. 2017
            - Средняя з.п. всех сотрудников организации,  тыс.руб. 2018
            - Средняя з.п. всех сотрудников организации,  тыс.руб. 2019
            - Средняя з.п. всех сотрудников организации,  тыс.руб. 2020
            - Средняя з.п. всех сотрудников организации,  тыс.руб. 2021
            - Средняя з.п. всех сотрудников организации,  тыс.руб. 2022
            - Средняя з.п. всех сотрудников организации,  тыс.руб. 2023
            - Средняя з.п. всех сотрудников организации,  тыс.руб. 2024
            - Средняя з.п. всех сотрудников организации,  тыс.руб. 2025

            Пример:
            Текст: "Средняя зарплата в 2017 году составила 80 тыс. руб., в 2018 - 85 тыс. руб."
            Вывод: { "Средняя з.п. всех сотрудников организации,  тыс.руб. 2017": 80.0, "Средняя з.п. всех сотрудников организации,  тыс.руб. 2018": 85.0, ... }

            Текст: {text}
            Вывод:
            """
        )
        self.chain = self.prompt | self.llm

    def extract_data(self, text: str, fields: List[str] = None) -> Dict[str, Any]:
        response = self.chain.invoke({"text": text})
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON от AvgSalaryTotalAgent: {response}")
            return {field: None for field in fields if field.startswith("Средняя з.п. всех сотрудников организации")} 

class AvgSalaryMoscowAgent(DataExtractionAgent):
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Извлеки из следующего текста значения для средней з.п. сотрудников, работающих в Москве, по годам с 2017 по 2025. 
            Если значение не найдено для конкретного года, укажи null. 
            Формат вывода должен быть JSON-объектом, где ключи - это полные названия полей из списка ниже, а значения - извлеченные числа (float).
            Список полей:
            - Средняя з.п. сотрудников, работающих в Москве,  тыс.руб. 2017
            - Средняя з.п. сотрудников, работающих в Москве,  тыс.руб. 2018
            - Средняя з.п. сотрудников, работающих в Москве,  тыс.руб. 2019
            - Средняя з.п. сотрудников, работающих в Москве,  тыс.руб. 2020
            - Средняя з.п. сотрудников, работающих в Москве,  тыс.руб. 2021
            - Средняя з.п. сотрудников, работающих в Москве,  тыс.руб. 2022
            - Средняя з.п. сотрудников, работающих в Москве,  тыс.руб. 2023
            - Средняя з.п. сотрудников, работающих в Москве,  тыс.руб. 2024
            - Средняя з.п. сотрудников, работающих в Москве,  тыс.руб. 2025

            Пример:
            Текст: "Средняя зарплата московских сотрудников в 2019 году составила 90 тыс. руб., в 2020 - 95 тыс. руб."
            Вывод: { "Средняя з.п. сотрудников, работающих в Москве,  тыс.руб. 2019": 90.0, "Средняя з.п. сотрудников, работающих в Москве,  тыс.руб. 2020": 95.0, ... }

            Текст: {text}
            Вывод:
            """
        )
        self.chain = self.prompt | self.llm

    def extract_data(self, text: str, fields: List[str] = None) -> Dict[str, Any]:
        response = self.chain.invoke({"text": text})
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON от AvgSalaryMoscowAgent: {response}")
            return {field: None for field in fields if field.startswith("Средняя з.п. сотрудников, работающих в Москве")} 

class TaxesMoscowNoExciseAgent(DataExtractionAgent):
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Извлеки из следующего текста значения для налогов, уплаченных в бюджет Москвы (без акцизов) по годам с 2017 по 2025. 
            Если значение не найдено для конкретного года, укажи null. 
            Формат вывода должен быть JSON-объектом, где ключи - это полные названия полей из списка ниже, а значения - извлеченные числа (float).
            Список полей:
            - Налоги, уплаченные в бюджет Москвы (без акцизов), тыс.руб. 2017
            - Налоги, уплаченные в бюджет Москвы (без акцизов), тыс.руб. 2018
            - Налоги, уплаченные в бюджет Москвы (без акцизов), тыс.руб. 2019
            - Налоги, уплаченные в бюджет Москвы (без акцизов), тыс.руб. 2020
            - Налоги, уплаченные в бюджет Москвы (без акцизов), тыс.руб. 2021
            - Налоги, уплаченные в бюджет Москвы (без акцизов), тыс.руб. 2022
            - Налоги, уплаченные в бюджет Москвы (без акцизов), тыс.руб. 2023
            - Налоги, уплаченные в бюджет Москвы (без акцизов), тыс.руб. 2024
            - Налоги, уплаченные в бюджет Москвы (без акцизов), тыс.руб. 2025

            Пример:
            Текст: "Налоги в бюджет Москвы (без акцизов) в 2020 году составили 2000 тыс. руб., в 2021 - 2100 тыс. руб."
            Вывод: { "Налоги, уплаченные в бюджет Москвы (без акцизов), тыс.руб. 2020": 2000.0, "Налоги, уплаченные в бюджет Москвы (без акцизов), тыс.руб. 2021": 2100.0, ... }

            Текст: {text}
            Вывод:
            """
        )
        self.chain = self.prompt | self.llm

    def extract_data(self, text: str, fields: List[str] = None) -> Dict[str, Any]:
        response = self.chain.invoke({"text": text})
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON от TaxesMoscowNoExciseAgent: {response}")
            return {field: None for field in fields if field.startswith("Налоги, уплаченные в бюджет Москвы (без акцизов)")} 

class ProfitTaxAgent(DataExtractionAgent):
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Извлеки из следующего текста значения для налога на прибыль по годам с 2017 по 2025. 
            Если значение не найдено для конкретного года, укажи null. 
            Формат вывода должен быть JSON-объектом, где ключи - это полные названия полей из списка ниже, а значения - извлеченные числа (float).
            Список полей:
            - Налог на прибыль, тыс.руб. 2017
            - Налог на прибыль, тыс.руб. 2018
            - Налог на прибыль, тыс.руб. 2019
            - Налог на прибыль, тыс.руб. 2020
            - Налог на прибыль, тыс.руб. 2021
            - Налог на прибыль, тыс.руб. 2022
            - Налог на прибыль, тыс.руб. 2023
            - Налог на прибыль, тыс.руб. 2024
            - Налог на прибыль, тыс.руб. 2025

            Пример:
            Текст: "Налог на прибыль в 2017 году составил 1000 тыс. руб., в 2018 - 1100 тыс. руб."
            Вывод: { "Налог на прибыль, тыс.руб. 2017": 1000.0, "Налог на прибыль, тыс.руб. 2018": 1100.0, ... }

            Текст: {text}
            Вывод:
            """
        )
        self.chain = self.prompt | self.llm

    def extract_data(self, text: str, fields: List[str] = None) -> Dict[str, Any]:
        response = self.chain.invoke({"text": text})
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON от ProfitTaxAgent: {response}")
            return {field: None for field in fields if field.startswith("Налог на прибыль")} 

class PropertyTaxAgent(DataExtractionAgent):
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Извлеки из следующего текста значения для налога на имущество по годам с 2017 по 2025. 
            Если значение не найдено для конкретного года, укажи null. 
            Формат вывода должен быть JSON-объектом, где ключи - это полные названия полей из списка ниже, а значения - извлеченные числа (float).
            Список полей:
            - Налог на имущество, тыс.руб. 2017
            - Налог на имущество, тыс.руб. 2018
            - Налог на имущество, тыс.руб. 2019
            - Налог на имущество, тыс.руб. 2020
            - Налог на имущество, тыс.руб. 2021
            - Налог на имущество, тыс.руб. 2022
            - Налог на имущество, тыс.руб. 2023
            - Налог на имущество, тыс.руб. 2024
            - Налог на имущество, тыс.руб. 2025

            Пример:
            Текст: "Налог на имущество в 2022 году составил 300 тыс. руб., в 2023 - 320 тыс. руб."
            Вывод: { "Налог на имущество, тыс.руб. 2022": 300.0, "Налог на имущество, тыс.руб. 2023": 320.0, ... }

            Текст: {text}
            Вывод:
            """
        )
        self.chain = self.prompt | self.llm

    def extract_data(self, text: str, fields: List[str] = None) -> Dict[str, Any]:
        response = self.chain.invoke({"text": text})
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON от PropertyTaxAgent: {response}")
            return {field: None for field in fields if field.startswith("Налог на имущество")} 

class LandTaxAgent(DataExtractionAgent):
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Извлеки из следующего текста значения для налога на землю по годам с 2017 по 2025. 
            Если значение не найдено для конкретного года, укажи null. 
            Формат вывода должен быть JSON-объектом, где ключи - это полные названия полей из списка ниже, а значения - извлеченные числа (float).
            Список полей:
            - Налог на землю, тыс.руб. 2017
            - Налог на землю, тыс.руб. 2018
            - Налог на землю, тыс.руб. 2019
            - Налог на землю, тыс.руб. 2020
            - Налог на землю, тыс.руб. 2021
            - Налог на землю, тыс.руб. 2022
            - Налог на землю, тыс.руб. 2023
            - Налог на землю, тыс.руб. 2024
            - Налог на землю, тыс.руб. 2025

            Пример:
            Текст: "Налог на землю в 2019 году составил 150 тыс. руб., в 2020 - 160 тыс. руб."
            Вывод: { "Налог на землю, тыс.руб. 2019": 150.0, "Налог на землю, тыс.руб. 2020": 160.0, ... }

            Текст: {text}
            Вывод:
            """
        )
        self.chain = self.prompt | self.llm

    def extract_data(self, text: str, fields: List[str] = None) -> Dict[str, Any]:
        response = self.chain.invoke({"text": text})
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON от LandTaxAgent: {response}")
            return {field: None for field in fields if field.startswith("Налог на землю")} 

class NDFLAgent(DataExtractionAgent):
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Извлеки из следующего текста значения для НДФЛ по годам с 2017 по 2025. 
            Если значение не найдено для конкретного года, укажи null. 
            Формат вывода должен быть JSON-объектом, где ключи - это полные названия полей из списка ниже, а значения - извлеченные числа (float).
            Список полей:
            - НДФЛ, тыс.руб. 2017
            - НДФЛ, тыс.руб. 2018
            - НДФЛ, тыс.руб. 2019
            - НДФЛ, тыс.руб. 2020
            - НДФЛ, тыс.руб. 2021
            - НДФЛ, тыс.руб. 2022
            - НДФЛ, тыс.руб. 2023
            - НДФЛ, тыс.руб. 2024
            - НДФЛ, тыс.руб. 2025

            Пример:
            Текст: "НДФЛ в 2021 году составил 800 тыс. руб., в 2022 - 850 тыс. руб."
            Вывод: { "НДФЛ, тыс.руб. 2021": 800.0, "НДФЛ, тыс.руб. 2022": 850.0, ... }

            Текст: {text}
            Вывод:
            """
        )
        self.chain = self.prompt | self.llm

    def extract_data(self, text: str, fields: List[str] = None) -> Dict[str, Any]:
        response = self.chain.invoke({"text": text})
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON от NDFLAgent: {response}")
            return {field: None for field in fields if field.startswith("НДФЛ")} 

class TransportTaxAgent(DataExtractionAgent):
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Извлеки из следующего текста значения для транспортного налога по годам с 2017 по 2025. 
            Если значение не найдено для конкретного года, укажи null. 
            Формат вывода должен быть JSON-объектом, где ключи - это полные названия полей из списка ниже, а значения - извлеченные числа (float).
            Список полей:
            - Транспортный налог, тыс.руб. 2017
            - Транспортный налог, тыс.руб. 2018
            - Транспортный налог, тыс.руб. 2019
            - Транспортный налог, тыс.руб. 2020
            - Транспортный налог, тыс.руб. 2021
            - Транспортный налог, тыс.руб. 2022
            - Транспортный налог, тыс.руб. 2023
            - Транспортный налог, тыс.руб. 2024
            - Транспортный налог, тыс.руб. 2025

            Пример:
            Текст: "Транспортный налог в 2018 году составил 50 тыс. руб., в 2019 - 55 тыс. руб."
            Вывод: { "Транспортный налог, тыс.руб. 2018": 50.0, "Транспортный налог, тыс.руб. 2019": 55.0, ... }

            Текст: {text}
            Вывод:
            """
        )
        self.chain = self.prompt | self.llm

    def extract_data(self, text: str, fields: List[str] = None) -> Dict[str, Any]:
        response = self.chain.invoke({"text": text})
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON от TransportTaxAgent: {response}")
            return {field: None for field in fields if field.startswith("Транспортный налог")} 

class OtherTaxesAgent(DataExtractionAgent):
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Извлеки из следующего текста значения для прочих налогов по годам с 2017 по 2025. 
            Если значение не найдено для конкретного года, укажи null. 
            Формат вывода должен быть JSON-объектом, где ключи - это полные названия полей из списка ниже, а значения - извлеченные числа (float).
            Список полей:
            - Прочие налоги 2017
            - Прочие налоги 2018
            - Прочие налоги 2019
            - Прочие налоги 2020
            - Прочие налоги 2021
            - Прочие налоги 2022
            - Прочие налоги 2023
            - Прочие налоги 2024
            - Прочие налоги 2025

            Пример:
            Текст: "Прочие налоги в 2023 году составили 100 тыс. руб., в 2024 - 110 тыс. руб."
            Вывод: { "Прочие налоги 2023": 100.0, "Прочие налоги 2024": 110.0, ... }

            Текст: {text}
            Вывод:
            """
        )
        self.chain = self.prompt | self.llm

    def extract_data(self, text: str, fields: List[str] = None) -> Dict[str, Any]:
        response = self.chain.invoke({"text": text})
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON от OtherTaxesAgent: {response}")
            return {field: None for field in fields if field.startswith("Прочие налоги")} 

class ExciseTaxesAgent(DataExtractionAgent):
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Извлеки из следующего текста значения для акцизов по годам с 2017 по 2025. 
            Если значение не найдено для конкретного года, укажи null. 
            Формат вывода должен быть JSON-объектом, где ключи - это полные названия полей из списка ниже, а значения - извлеченные числа (float).
            Список полей:
            - Акцизы, тыс. руб. 2017
            - Акцизы, тыс. руб. 2018
            - Акцизы, тыс. руб. 2019
            - Акцизы, тыс. руб. 2020
            - Акцизы, тыс. руб. 2021
            - Акцизы, тыс. руб. 2022
            - Акцизы, тыс. руб. 2023
            - Акцизы, тыс. руб. 2024
            - Акцизы, тыс. руб. 2025

            Пример:
            Текст: "Акцизы в 2020 году составили 200 тыс. руб., в 2021 - 210 тыс. руб."
            Вывод: { "Акцизы, тыс. руб. 2020": 200.0, "Акцизы, тыс. руб. 2021": 210.0, ... }

            Текст: {text}
            Вывод:
            """
        )
        self.chain = self.prompt | self.llm

    def extract_data(self, text: str, fields: List[str] = None) -> Dict[str, Any]:
        response = self.chain.invoke({"text": text})
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON от ExciseTaxesAgent: {response}")
            return {field: None for field in fields if field.startswith("Акцизы")} 

class InvestmentsMoscowAgent(DataExtractionAgent):
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Извлеки из следующего текста значения для инвестиций в Москву по годам с 2021 по 2025. 
            Если значение не найдено для конкретного года, укажи null. 
            Формат вывода должен быть JSON-объектом, где ключи - это полные названия полей из списка ниже, а значения - извлеченные числа (float).
            Список полей:
            - Инвестиции в Мск 2021 тыс. руб.
            - Инвестиции в Мск 2022 тыс. руб.
            - Инвестиции в Мск 2023 тыс. руб.
            - Инвестиции в Мск 2024 тыс. руб.
            - Инвестиции в Мск 2025 тыс. руб.

            Пример:
            Текст: "Инвестиции в Москву в 2022 году составили 50000 тыс. руб., в 2023 - 55000 тыс. руб."
            Вывод: { "Инвестиции в Мск 2022 тыс. руб.": 50000.0, "Инвестиции в Мск 2023 тыс. руб.": 55000.0, ... }

            Текст: {text}
            Вывод:
            """
        )
        self.chain = self.prompt | self.llm

    def extract_data(self, text: str, fields: List[str] = None) -> Dict[str, Any]:
        response = self.chain.invoke({"text": text})
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON от InvestmentsMoscowAgent: {response}")
            return {field: None for field in fields if field.startswith("Инвестиции в Мск")} 

class ExportVolumeAgent(DataExtractionAgent):
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Извлеки из следующего текста значения для объема экспорта по годам с 2019 по 2025. 
            Если значение не найдено для конкретного года, укажи null. 
            Формат вывода должен быть JSON-объектом, где ключи - это полные названия полей из списка ниже, а значения - извлеченные числа (float).
            Список полей:
            - Объем экспорта, тыс. руб. 2019
            - Объем экспорта, тыс. руб. 2020
            - Объем экспорта, тыс. руб. 2021
            - Объем экспорта, тыс. руб. 2022
            - Объем экспорта, тыс. руб. 2023
            - Объем экспорта, тыс. руб. 2024
            - Объем экспорта, тыс. руб. 2025

            Пример:
            Текст: "Объем экспорта в 2020 году составил 10000 тыс. руб., в 2021 - 12000 тыс. руб."
            Вывод: { "Объем экспорта, тыс. руб. 2020": 10000.0, "Объем экспорта, тыс. руб. 2021": 12000.0, ... }

            Текст: {text}
            Вывод:
            """
        )
        self.chain = self.prompt | self.llm

    def extract_data(self, text: str, fields: List[str] = None) -> Dict[str, Any]:
        response = self.chain.invoke({"text": text})
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON от ExportVolumeAgent: {response}")
            return {field: None for field in fields if field.startswith("Объем экспорта")} 

class PropertyComplexAgent(DataExtractionAgent):
    def __init__(self, ollama_model: str = "gemma3:4b"):
        super().__init__(ollama_model)
        self.prompt = PromptTemplate(
            input_variables=["text"],
            template="""
            Извлеки из следующего текста значения для имущественно-земельного комплекса. 
            Если значение не найдено для конкретного поля, укажи null. 
            Формат вывода должен быть JSON-объектом, где ключи - это полные названия полей из списка ниже, а значения - извлеченные строки или числа.
            Список полей:
            - Кадастровый номер ЗУ
            - Площадь ЗУ
            - Вид разрешенного использования ЗУ
            - Вид собственности ЗУ
            - Собственник ЗУ
            - Кадастровый номер ОКСа
            - Площадь ОКСов
            - Вид разрешенного использования ОКСов
            - Тип строения и цель использования
            - Вид собственности ОКСов
            - СобственникОКСов
            - Площадь производственных помещений, кв.м.

            Пример:
            Текст: "Кадастровый номер ЗУ: 77:01:0001001:100. Площадь ЗУ: 1500 кв.м. Собственник: ООО 'Ромашка'."
            Вывод: { "Кадастровый номер ЗУ": "77:01:0001001:100", "Площадь ЗУ": "1500 кв.m.", "Собственник ЗУ": "ООО 'Ромашка'", ... }

            Текст: {text}
            Вывод:
            """
        )
        self.chain = self.prompt | self.llm

    def extract_data(self, text: str, fields: List[str] = None) -> Dict[str, Any]:
        response = self.chain.invoke({"text": text})
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            print(f"Ошибка декодирования JSON от PropertyComplexAgent: {response}")
            return {field: None for field in fields if field in [
                "Кадастровый номер ЗУ", "Площадь ЗУ", "Вид разрешенного использования ЗУ",
                "Вид собственности ЗУ", "Собственник ЗУ", "Кадастровый номер ОКСа",
                "Площадь ОКСов", "Вид разрешенного использования ОКСов",
                "Тип строения и цель использования", "Вид собственности ОКСов",
                "СобственникОКСов", "Площадь производственных помещений, кв.м."
            ]}