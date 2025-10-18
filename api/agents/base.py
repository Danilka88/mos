from langchain_ollama import OllamaLLM
from typing import List
import json

class BaseAnalysisAgent:
    """Общий базовый класс для всех агентов-аналитиков."""
    def __init__(self, ollama_model: str = "gemma3:4b"):
        self.llm = OllamaLLM(model=ollama_model)

    def _parse_response(self, response: str, agent_name: str) -> List[str]:
        """
        Парсит JSON-ответ от LLM, извлекая список инсайтов.
        Обрабатывает случаи, когда JSON обернут в markdown.
        """
        try:
            # LLM может вернуть markdown с JSON внутри
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.strip().replace("`", "").strip()

            insights = json.loads(response)
            if isinstance(insights, list) and all(isinstance(item, str) for item in insights):
                return insights
            else:
                print(f"Ошибка формата от {agent_name}: ожидался список строк, получен {type(insights)}. Ответ: {response}")
                return []
        except (json.JSONDecodeError, IndexError) as e:
            print(f"Ошибка декодирования JSON от {agent_name}: {response}. Ошибка: {e}")
            return []
