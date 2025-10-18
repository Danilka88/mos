import sys
from pathlib import Path

# Добавляем корневую директорию проекта в sys.path
# Это позволяет импортировать модули как 'api.main' вместо относительных импортов
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import json

# Импортируем приложение FastAPI и оркестратор
from api.main import app, orchestrator, OUTPUT_DIR, ALL_HEADERS
from api.agents import RevenueAgent, NetProfitAgent, EmployeeCountAgent, MoscowEmployeeCountAgent, PayrollTotalAgent, PayrollMoscowAgent, AvgSalaryTotalAgent, AvgSalaryMoscowAgent, TaxesMoscowNoExciseAgent, ProfitTaxAgent, PropertyTaxAgent, LandTaxAgent, NDFLAgent, TransportTaxAgent, OtherTaxesAgent, ExciseTaxesAgent, InvestmentsMoscowAgent, ExportVolumeAgent, PropertyComplexAgent

client = TestClient(app)

# Тестовые данные
TEST_TEXT = "Выручка за 2020 год составила 15000 тыс. руб., за 2021 - 16000 тыс. руб. Чистая прибыль в 2022 году составила 5000 тыс. руб."
TEST_INN = "1234567890"

@pytest.fixture(autouse=True)
def cleanup_output_dir():
    # Очистка директории вывода перед каждым тестом
    for f in OUTPUT_DIR.glob("*.json"):
        f.unlink()
    yield
    # Очистка после каждого теста
    for f in OUTPUT_DIR.glob("*.json"):
        f.unlink()

# Мокируем LLM для агентов
@pytest.fixture
def mock_llm_chain_run():
    with patch.object(LLMChain, 'run') as mock_run:
        # Дефолтные ответы для разных агентов
        def side_effect_func(**kwargs):
            prompt_template = kwargs['prompt_template']
            if "Выручка предприятия" in prompt_template:
                return json.dumps({
                    "Выручка предприятия, тыс. руб. 2020": 15000.0,
                    "Выручка предприятия, тыс. руб. 2021": 16000.0,
                    "Выручка предприятия, тыс. руб. 2017": None,
                    "Выручка предприятия, тыс. руб. 2018": None,
                    "Выручка предприятия, тыс. руб. 2019": None,
                    "Выручка предприятия, тыс. руб. 2022": None,
                    "Выручка предприятия, тыс. руб. 2023": None,
                    "Выручка предприятия, тыс. руб. 2024": None,
                    "Выручка предприятия, тыс. руб. 2025": None
                })
            elif "Чистая прибыль (убыток)" in prompt_template:
                return json.dumps({
                    "Чистая прибыль (убыток),тыс. руб. 2022": 5000.0,
                    "Чистая прибыль (убыток),тыс. руб. 2017": None,
                    "Чистая прибыль (убыток),тыс. руб. 2018": None,
                    "Чистая прибыль (убыток),тыс. руб. 2019": None,
                    "Чистая прибыль (убыток),тыс. руб. 2020": None,
                    "Чистая прибыль (убыток),тыс. руб. 2021": None,
                    "Чистая прибыль (убыток),тыс. руб. 2023": None,
                    "Чистая прибыль (убыток),тыс. руб. 2024": None,
                    "Чистая прибыль (убыток),тыс. руб. 2025": None
                })
            elif "Извлеки ИНН" in prompt_template:
                return TEST_INN
            return json.dumps({}) # Дефолтный пустой JSON

        mock_run.side_effect = lambda **kwargs: side_effect_func(prompt_template=kwargs['prompt_template'].template, **kwargs)
        yield mock_run

# Тесты для агентов
def test_revenue_agent_extracts_data(mock_llm_chain_run):
    agent = RevenueAgent()
    result = agent.extract_data(TEST_TEXT, ALL_HEADERS)
    assert result["Выручка предприятия, тыс. руб. 2020"] == 15000.0
    assert result["Выручка предприятия, тыс. руб. 2021"] == 16000.0
    assert result["Выручка предприятия, тыс. руб. 2017"] is None

def test_net_profit_agent_extracts_data(mock_llm_chain_run):
    agent = NetProfitAgent()
    result = agent.extract_data(TEST_TEXT, ALL_HEADERS)
    assert result["Чистая прибыль (убыток),тыс. руб. 2022"] == 5000.0
    assert result["Чистая прибыль (убыток),тыс. руб. 2017"] is None

# Тесты для API
def test_process_text_endpoint_success(mock_llm_chain_run):
    response = client.post(
        "/process_text/",
        json={
            "text": TEST_TEXT,
            "inn": TEST_INN # Передаем ИНН явно для упрощения теста
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Данные успешно обработаны и сохранены"
    assert data["inn"] == TEST_INN
    assert Path(data["file_path"]).exists()

    # Проверяем содержимое сохраненного файла
    with open(Path(data["file_path"]), "r", encoding="utf-8") as f:
        saved_data = json.load(f)
    
    assert saved_data["ИНН"] == TEST_INN
    assert saved_data["Выручка предприятия, тыс. руб. 2020"] == 15000.0
    assert saved_data["Чистая прибыль (убыток),тыс. руб. 2022"] == 5000.0

def test_process_text_endpoint_no_text_failure():
    response = client.post(
        "/process_text/",
        json={
            "inn": TEST_INN
        }
    )
    assert response.status_code == 400
    assert "Отсутствует поле 'text' во входных данных" in response.json()["detail"]

def test_process_text_endpoint_inn_extraction_success(mock_llm_chain_run):
    # Мокируем извлечение ИНН из текста
    mock_llm_chain_run.side_effect = lambda **kwargs: (
        TEST_INN if "Извлеки ИНН" in kwargs['prompt_template'].template else 
        json.dumps({"Выручка предприятия, тыс. руб. 2020": 100.0}) if "Выручка предприятия" in kwargs['prompt_template'].template else 
        json.dumps({}) # Дефолтный пустой JSON
    )

    response = client.post(
        "/process_text/",
        json={
            "text": f"Некий текст с ИНН {TEST_INN} и другими данными."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["inn"] == TEST_INN
    assert Path(data["file_path"]).exists()

def test_process_text_endpoint_inn_extraction_failure(mock_llm_chain_run):
    # Мокируем, что ИНН не найден
    mock_llm_chain_run.side_effect = lambda **kwargs: (
        "null" if "Извлеки ИНН" in kwargs['prompt_template'].template else 
        json.dumps({}) # Дефолтный пустой JSON
    )

    response = client.post(
        "/process_text/",
        json={
            "text": "Некий текст без ИНН."
        }
    )
    assert response.status_code == 400
    assert "ИНН не найден во входных данных или тексте" in response.json()["detail"]