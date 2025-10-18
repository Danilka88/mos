from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict, Any
import json
from collections import defaultdict
from langchain_core.prompts import PromptTemplate

# Импортируем новые модели и загрузчик данных
from api.models import CompanyData, AnalysisInsights
from api.data_loader import get_mock_company_data

# Импортируем оркестратор и агентов для анализа
from api.orchestrator import AnalysisOrchestrator
from api.agents.industry.analysis_agents import IndustryCriticalEventsAgent, IndustryGrowthPointsAgent, IndustryAttentionZonesAgent, IndustryInterestingFactsAgent

app = FastAPI(
    title="MOS Industry Analysis API",
    description="API для анализа промышленных данных Москвы с использованием ИИ-агентов.",
    version="1.0.0"
)

# --- Загрузка данных при старте приложения ---
# Данные загружаются один раз и хранятся в памяти для быстрого доступа
all_companies: List[CompanyData] = get_mock_company_data()
companies_by_inn: Dict[str, CompanyData] = {c.inn: c for c in all_companies}
companies_by_industry: Dict[str, List[CompanyData]] = defaultdict(list)
for company in all_companies:
    companies_by_industry[company.industry].append(company)

# --- Инициализация оркестраторов и агентов ---
orchestrator = AnalysisOrchestrator()
industry_analysis_agents = {
    "critical": IndustryCriticalEventsAgent(),
    "positive": IndustryGrowthPointsAgent(),
    "warning": IndustryAttentionZonesAgent(),
    "info": IndustryInterestingFactsAgent(),
}

# === API Эндпоинты для UI ===

@app.get("/api/companies", response_model=List[CompanyData], tags=["UI Endpoints"])
async def get_all_companies():
    """
    Возвращает список всех компаний с их финансовыми данными.
    Используется на странице со списком всех компаний.
    """
    return all_companies

@app.get("/api/companies/{inn}", response_model=CompanyData, tags=["UI Endpoints"])
async def get_company_by_inn(inn: str):
    """
    Возвращает детальную информацию по одной компании по её ИНН.
    Используется на странице детализации компании.
    """
    company = companies_by_inn.get(inn)
    if not company:
        raise HTTPException(status_code=404, detail="Компания с таким ИНН не найдена")
    return company

@app.get("/api/companies/{inn}/analysis", response_model=AnalysisInsights, tags=["UI Endpoints"])
async def get_company_analysis(inn: str):
    """
    Запускает анализ для одной конкретной компании и возвращает инсайты.
    Используется на странице детализации компании.
    """
    company = companies_by_inn.get(inn)
    if not company:
        raise HTTPException(status_code=404, detail="Компания с таким ИНН не найдена")

    analysis_results = orchestrator.run_analysis(company)
    
    # Приводим результат к модели AnalysisInsights
    return AnalysisInsights(
        critical=analysis_results.get("critical_events", []),
        positive=analysis_results.get("growth_points", []),
        warning=analysis_results.get("attention_zones", []),
        info=analysis_results.get("interesting_facts", [])
    )

@app.get("/api/insights/dashboard", response_model=Dict[str, List[str]], tags=["UI Endpoints"])
async def get_dashboard_insights(mode: str = Query("company", enum=["company", "industry"])):
    """
    Возвращает агрегированные инсайты для главного дашборда.
    Поддерживает два режима: `company` и `industry`.
    """
    all_insights: Dict[str, List[str]] = defaultdict(list)

    if mode == "company":
        # Запускаем анализ для каждой компании и агрегируем инсайты
        for company in all_companies:
            company_insights = orchestrator.run_analysis(company)
            for insight_type, insights_list in company_insights.items():
                all_insights[insight_type].extend(insights_list)
    elif mode == "industry":
        # Запускаем анализ для каждой отрасли и агрегируем инсайты
        for industry_name, companies_in_industry in companies_by_industry.items():
            for insight_type, agent in industry_analysis_agents.items():
                insights = agent.analyze(industry_name, companies_in_industry)
                all_insights[insight_type].extend(insights)

    return all_insights

@app.get("/api/insights/industry/{industry_name}", response_model=AnalysisInsights, tags=["UI Endpoints"])
async def get_industry_analysis(industry_name: str):
    """
    Возвращает детальный анализ по конкретной отрасли.
    """
    companies_in_industry = companies_by_industry.get(industry_name)
    if not companies_in_industry:
        raise HTTPException(status_code=404, detail=f"Отрасль '{industry_name}' не найдена")

    analysis_results = {}
    for key, agent in industry_analysis_agents.items():
        analysis_results[key] = agent.analyze(industry_name, companies_in_industry)

    return AnalysisInsights(
        critical=analysis_results.get("critical", []),
        positive=analysis_results.get("positive", []),
        warning=analysis_results.get("warning", []),
        info=analysis_results.get("info", [])
    )

# === Старый эндпоинт для обработки текста (сохранен для совместимости) ===
@app.post("/process_text/")
async def process_text(payload: Dict[str, str]):
    input_text = payload.get("text")
    if not input_text:
        raise HTTPException(status_code=400, detail="Отсутствует поле 'text' во входных данных")

    inn = payload.get("inn")
    if not inn:
        # Попытка извлечь ИНН из текста с помощью LLM (простой промпт)
        inn_prompt = PromptTemplate(
            input_variables=["text"],
            template='''
            Извлеки ИНН из следующего текста. ИНН - это 10 или 12-значное число. 
            Если ИНН не найден, верни 'null'.
            Текст: {text}
            ИНН:
            '''
        )
        # Используем LLM одного из агентов
        inn_chain = inn_prompt | orchestrator.extraction_agents["revenue"].llm 
        extracted_inn = inn_chain.invoke({"text": input_text}).strip()
        if extracted_inn and extracted_inn.lower() != 'null':
            inn = extracted_inn
        else:
            raise HTTPException(status_code=400, detail="ИНН не найден во входных данных или тексте")

    # Обработка текста мультиагентной системой
    # ALL_HEADERS больше не используется напрямую, так как агенты извлечения данных
    # теперь сами определяют, какие поля извлекать.
    # Однако, для совместимости с сигнатурой process_text_with_agents, передадим пустой список.
    extracted_flat_data = orchestrator.process_text_with_agents(input_text, [])

    # Преобразование плоских данных вложенную структуру CompanyData
    processed_company_data = orchestrator.transform_to_nested(extracted_flat_data)

    # Запуск аналитических агентов
    analysis_results = orchestrator.run_analysis(processed_company_data)

    # Сохранение JSON-файла (логика сохранена из старой версии)
    # OUTPUT_DIR и BASE_HEADERS_PATH больше не нужны здесь, но оставлены для контекста
    # В реальном приложении это должно быть перенесено в отдельный сервис или базу данных
    output_file_path = f"data/web_output/{inn}.json"
    
    final_data_to_save = {
        "data": processed_company_data.dict(by_alias=True, exclude_none=True),
        "analysis": analysis_results
    }

    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(final_data_to_save, f, ensure_ascii=False, indent=4)

    return {
        "message": "Данные успешно обработаны, проанализированы и сохранены", 
        "inn": inn, 
        "file_path": str(output_file_path), 
        "data": processed_company_data.dict(by_alias=True, exclude_none=True),
        "analysis": analysis_results
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
