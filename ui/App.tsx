/**
 * @file App.tsx
 * @description Главный компонент приложения. Управляет состоянием, загрузкой данных, навигацией между страницами (дашборд, список компаний, детализация, анализ по отраслям) и взаимодействием с ИИ-сервисом.
 */

import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { Header } from './components/Header';
import { DashboardCard } from './components/DashboardCard';
import { InsightCard } from './components/AnomalyCard';
import { getMockCompanyData } from './services/mockDataService';
import { CompanyData, YearlyData, InsightType, AnalysisMode } from './types';
import { generateInsight } from './services/geminiService';
import { AllInsightsPage } from './pages/AllInsightsPage';
import { CompaniesPage } from './pages/CompaniesPage';
import { CompanyDetailPage } from './pages/CompanyDetailPage';
import { IndustryAnalysisPage } from './pages/IndustryAnalysisPage'; // Импорт новой страницы
import { CompanyComparisonChart } from './components/CompanyComparisonChart';
import { TaxBreakdownChart } from './components/TaxBreakdownChart';
import { ViewToggle } from './components/ViewToggle';

// Определяем типы для навигации между страницами.
type Page = 'dashboard' | 'insights' | 'companies' | 'companyDetail' | 'industryAnalysis';

/**
 * =================================================================================
 * ИИ-АГЕНТ #1: Анализ на уровне отдельных компаний (для дашборда).
 * Находит наиболее яркие аномалии по всему пулу компаний.
 * =================================================================================
 */
const fetchCompanyInsightList = async (type: InsightType, data: CompanyData[]): Promise<string[]> => {
    // Упрощаем данные для экономии токенов в реальном API
    const summarizedData = data.map(c => ({
        name: c.name,
        financials: c.financials.map(f => ({ year: f.year, profit: f.profit, revenue: f.revenue, employees: f.employees }))
    }));
    const jsonData = JSON.stringify(summarizedData);

    let instruction = '';
    switch(type) {
        case 'critical': instruction = `Найди 10-15 САМЫХ КРИТИЧНЫХ аномалий или тенденций В ОТДЕЛЬНЫХ КОМПАНИЯХ, требующих НЕМЕДЛЕННОГО внимания. Пример заголовка: "Резкое падение прибыли у ПАО 'ФармСинтез' в 2024г".`; break;
        case 'warning': instruction = `Выяви 10-15 потенциальных РИСКОВ или негативных тенденций В КОНКРЕТНЫХ КОМПАНИЯХ, которые еще не стали критическими. Пример заголовка: "Замедление роста выручки у ООО 'ТехноСталь'".`; break;
        case 'positive': instruction = `Найди 10-15 САМЫХ ПОЗИТИВНЫХ достижений ИЛИ ВЫДАЮЩИХСЯ КОМПАНИЙ. Пример заголовка: "НПО 'Квант' - лидер по росту выручки на сотрудника".`; break;
        case 'info': instruction = `Предоставь 10-15 ИНТЕРЕСНЫХ, не очевидных наблюдений ИЛИ СРАВНЕНИЙ МЕЖДУ КОМПАНИЯМИ. Пример заголовка: "АО 'МосЭнергоПром' показывает самую стабильную рентабельность".`; break;
    }
    const prompt = `Проанализируй финансовые данные по нескольким промышленным компаниям Москвы: ${jsonData}. ${instruction} Верни результат в виде JSON-массива строк, где каждая строка - это краткий, емкий заголовок для одного ключевого вывода. Не добавляй нумерацию или маркеры.`;
    
    try {
        const result = await generateInsight(prompt);
        const cleanedResult = result.replace(/```json|```/g, '').trim();
        const parsedResult = JSON.parse(cleanedResult);
        return Array.isArray(parsedResult) ? parsedResult : [];
    } catch (e) {
        console.error(`Ошибка при получении инсайтов по компаниям типа '${type}':`, e);
        return [`Ошибка анализа данных (компании) для категории: ${type}`];
    }
};

/**
 * =================================================================================
 * ИИ-АГЕНТ #2: Анализ на уровне отраслей (макро-уровень).
 * Агрегирует данные и ищет тенденции в отраслях в целом.
 * =================================================================================
 */
const fetchIndustryInsightList = async (type: InsightType, data: CompanyData[]): Promise<string[]> => {
    // Упрощаем данные
    const summarizedData = data.map(c => ({
        name: c.name,
        industry: c.industry,
        financials: c.financials.map(f => ({ year: f.year, profit: f.profit, revenue: f.revenue, employees: f.employees }))
    }));
    const jsonData = JSON.stringify(summarizedData);
    
    let instruction = '';
    switch(type) {
        case 'critical': instruction = `Найди 5-7 САМЫХ КРИТИЧНЫХ проблем или негативных трендов НА УРОВНЕ ОТРАСЛЕЙ. Пример заголовка: "Стагнация выручки в тяжелой промышленности в 2025 году".`; break;
        case 'warning': instruction = `Выяви 5-7 потенциальных РИСКОВ или негативных тенденций НА УРОВНЕ ОТРАСЛЕЙ. Пример заголовка: "Снижение рентабельности в пищевой промышленности".`; break;
        case 'positive': instruction = `Найди 5-7 САМЫХ ПОЗИТИВНЫХ трендов или лидирующих ОТРАСЛЕЙ. Пример заголовка: "Фармацевтика показывает самый высокий темп роста прибыли".`; break;
        case 'info': instruction = `Предоставь 5-7 ИНТЕРЕСНЫХ СРАВНЕНИЙ МЕЖДУ ОТРАСЛЯМИ. Пример заголовка: "Высокотехнологичное производство лидирует по выручке на сотрудника".`; break;
    }

    const prompt = `На основе данных по компаниям: ${jsonData}. Сначала агрегируй данные (суммируй выручку, прибыль, сотрудников) по каждой отрасли за каждый год. Затем проанализируй эти агрегированные данные по отраслям. ${instruction} Верни результат в виде JSON-массива строк. Каждая строка - краткий заголовок для одного вывода по отрасли.`;

    try {
        const result = await generateInsight(prompt);
        const cleanedResult = result.replace(/```json|```/g, '').trim();
        const parsedResult = JSON.parse(cleanedResult);
        return Array.isArray(parsedResult) ? parsedResult : [];
    } catch (e) {
        console.error(`Ошибка при получении инсайтов по отраслям типа '${type}':`, e);
        return [`Ошибка анализа данных (отрасли) для категории: ${type}`];
    }
}
// =================================================================================
// ИИ-АГЕНТ #3: Анализ ОДНОЙ компании (для страницы детализации). Находится в `geminiService.ts`.
// ИИ-АГЕНТ #4: СРАВНИТЕЛЬНЫЙ анализ компаний ВНУТРИ ОДНОЙ ОТРАСЛИ (для страницы анализа по отраслям). Находится в `geminiService.ts`.
// =================================================================================


/**
 * Компонент главной страницы (дашборда).
 */
const Dashboard: React.FC<{
    companies: CompanyData[],
    insights: { [key in InsightType]: string[] },
    insightsLoading: boolean,
    onViewAll: (type: InsightType) => void,
    analysisMode: AnalysisMode,
    setAnalysisMode: (mode: AnalysisMode) => void,
}> = ({ companies, insights, insightsLoading, onViewAll, analysisMode, setAnalysisMode }) => {
    
    // Агрегирует данные по всем компаниям для построения общих графиков.
    const aggregateYearlyData = useCallback((dataKey: keyof YearlyData) => {
        const yearlyTotals: { [year: string]: number } = {};
        companies.forEach(company => {
            company.financials.forEach(fin => {
                if (!yearlyTotals[fin.year]) yearlyTotals[fin.year] = 0;
                yearlyTotals[fin.year] += fin[dataKey] as number;
            });
        });
        return Object.keys(yearlyTotals).map(year => ({ year, value: yearlyTotals[year] })).sort((a, b) => parseInt(a.year) - parseInt(b.year));
    }, [companies]);

    // Рассчитывает среднюю зарплату по всем компаниям по годам.
    const calculateAverageSalary = useCallback(() => {
        const yearlyTotals: { [year: string]: { payroll: number, employees: number } } = {};
        companies.forEach(company => {
            company.financials.forEach(fin => {
                if (!yearlyTotals[fin.year]) yearlyTotals[fin.year] = { payroll: 0, employees: 0 };
                yearlyTotals[fin.year].payroll += fin.payroll;
                yearlyTotals[fin.year].employees += fin.employees;
            });
        });
        return Object.keys(yearlyTotals).map(year => ({
            year,
            value: yearlyTotals[year].employees > 0 ? Math.round(yearlyTotals[year].payroll / yearlyTotals[year].employees) : 0
        })).sort((a, b) => parseInt(a.year) - parseInt(b.year));
    }, [companies]);

    const revenueByYear = useMemo(() => aggregateYearlyData('revenue'), [companies, aggregateYearlyData]);
    const profitByYear = useMemo(() => aggregateYearlyData('profit'), [companies, aggregateYearlyData]);
    const salaryByYear = useMemo(() => calculateAverageSalary(), [companies, calculateAverageSalary]);
    
    return (
        <main className="mt-8">
            <ViewToggle mode={analysisMode} setMode={setAnalysisMode} />
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
                <InsightCard title="Критические события" type="critical" insights={insights.critical} isLoading={insightsLoading} error={null} fullData={companies} onViewAll={onViewAll} />
                <InsightCard title="Точки роста" type="positive" insights={insights.positive} isLoading={insightsLoading} error={null} fullData={companies} onViewAll={onViewAll} />
                <InsightCard title="Зоны внимания" type="warning" insights={insights.warning} isLoading={insightsLoading} error={null} fullData={companies} onViewAll={onViewAll} />
                <InsightCard title="Интересные факты" type="info" insights={insights.info} isLoading={insightsLoading} error={null} fullData={companies} onViewAll={onViewAll} />
            </div>

            <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
                <DashboardCard title="Общая выручка по годам (тыс. руб.)" data={revenueByYear} dataKey="value" xAxisKey="year" metricName="общая выручка" chartType="bar" />
                <DashboardCard title="Общая чистая прибыль по годам (тыс. руб.)" data={profitByYear} dataKey="value" xAxisKey="year" metricName="общая чистая прибыль" chartType="bar" />
                <DashboardCard title="Средняя зарплата по годам (тыс. руб.)" data={salaryByYear} dataKey="value" xAxisKey="year" metricName="средняя зарплата" chartType="line" />
                <TaxBreakdownChart data={companies} year={2025} title="Структура налогов за 2025 г. (тыс. руб.)" />
                <CompanyComparisonChart data={companies} year={2025} metric="revenue" title="Вклад компаний в общую выручку за 2025 г." />
            </div>
        </main>
    )
};

/**
 * Корневой компонент приложения.
 */
const App: React.FC = () => {
    // Управление навигацией
    const [page, setPage] = useState<Page>('dashboard');
    // Хранение данных выбранной компании для страницы детализации
    const [selectedCompany, setSelectedCompany] = useState<CompanyData | null>(null);
    // Для страницы "Все события", чтобы открывалась нужная вкладка
    const [initialInsightTab, setInitialInsightTab] = useState<InsightType>('critical');
    
    // Хранение всех данных о компаниях
    const [companies, setCompanies] = useState<CompanyData[]>([]);
    
    // Режим анализа (по компаниям / по отраслям)
    const [analysisMode, setAnalysisMode] = useState<AnalysisMode>('company');
    
    // Хранение результатов от ИИ-агентов
    const [companyInsights, setCompanyInsights] = useState<{ [key in InsightType]: string[] }>({ critical: [], warning: [], positive: [], info: [] });
    const [industryInsights, setIndustryInsights] = useState<{ [key in InsightType]: string[] }>({ critical: [], warning: [], positive: [], info: [] });

    // Управление состоянием загрузки
    const [loading, setLoading] = useState<boolean>(true); // Первоначальная загрузка данных
    const [insightsLoading, setInsightsLoading] = useState<boolean>(true); // Загрузка инсайтов от ИИ

    // Основной эффект для загрузки всех данных при старте приложения
    useEffect(() => {
        const loadData = async () => {
            setLoading(true);
            const companyData = getMockCompanyData();
            setCompanies(companyData);
            setLoading(false); 

            setInsightsLoading(true);
            // Параллельно запрашиваем все типы инсайтов для обоих режимов анализа
            const [
                companyCritical, companyPositive, companyWarning, companyInfo,
                industryCritical, industryPositive, industryWarning, industryInfo
            ] = await Promise.all([
                fetchCompanyInsightList('critical', companyData),
                fetchCompanyInsightList('positive', companyData),
                fetchCompanyInsightList('warning', companyData),
                fetchCompanyInsightList('info', companyData),
                fetchIndustryInsightList('critical', companyData),
                fetchIndustryInsightList('positive', companyData),
                fetchIndustryInsightList('warning', companyData),
                fetchIndustryInsightList('info', companyData),
            ]);
            setCompanyInsights({ critical: companyCritical, positive: companyPositive, warning: companyWarning, info: companyInfo });
            setIndustryInsights({ critical: industryCritical, positive: industryPositive, warning: industryWarning, info: industryInfo });
            setInsightsLoading(false);
        };
        loadData();
    }, []);

    // Обработчик для перехода на страницу "Все события"
    const handleViewAll = (type: InsightType) => {
        setInitialInsightTab(type);
        setPage('insights');
    };
    
    // Обработчик для выбора компании из списка
    const handleSelectCompany = (company: CompanyData) => {
        setSelectedCompany(company);
        setPage('companyDetail');
    };

    // Обработчик для возврата со страницы детализации к списку компаний
    const handleBackToCompanies = () => {
        setSelectedCompany(null);
        setPage('companies');
    };
    
    // "Маршрутизатор" - рендерит нужную страницу в зависимости от состояния `page`
    const renderContent = () => {
        switch (page) {
            case 'dashboard':
                const activeInsights = analysisMode === 'company' ? companyInsights : industryInsights;
                return <Dashboard 
                    companies={companies}
                    insights={activeInsights}
                    insightsLoading={insightsLoading}
                    onViewAll={handleViewAll}
                    analysisMode={analysisMode}
                    setAnalysisMode={setAnalysisMode}
                />;
            case 'insights':
                return <AllInsightsPage 
                    companyInsights={companyInsights}
                    industryInsights={industryInsights}
                    onBack={() => setPage('dashboard')}
                    initialTab={initialInsightTab}
                    initialMode={analysisMode}
                />;
            case 'companies':
                return <CompaniesPage 
                    companies={companies}
                    onSelectCompany={handleSelectCompany}
                />;
            case 'companyDetail':
                return selectedCompany ? 
                    <CompanyDetailPage 
                        company={selectedCompany} 
                        onBack={handleBackToCompanies} 
                    /> : null;
            case 'industryAnalysis': // Новый маршрут
                return <IndustryAnalysisPage companies={companies} />;
            default:
                return null;
        }
    };

    // Отображение прелоадера во время первоначальной загрузки данных
    if (loading) {
        return (
            <div className="flex items-center justify-center h-screen bg-gray-900 text-white">
                <svg className="animate-spin -ml-1 mr-3 h-10 w-10 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span className="text-xl">Загрузка данных...</span>
            </div>
        );
    }
    
    return (
        <div className="min-h-screen bg-gray-900 text-gray-200">
             <div className="container mx-auto px-4">
                <Header page={page} setPage={setPage} />
                {renderContent()}
            </div>
        </div>
    );
};

export default App;