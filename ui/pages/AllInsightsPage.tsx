/**
 * @file AllInsightsPage.tsx
 * @description Компонент-страница для отображения полного списка всех инсайтов.
 * Позволяет пользователю просматривать все сгенерированные ИИ выводы с разбивкой по категориям и пагинацией.
 * Поддерживает переключение между режимами анализа (по компаниям и по отраслям).
 */
import React, { useState, useMemo } from 'react';
import { InsightType, AnalysisMode } from '../types';
import { Pagination } from '../components/Pagination';
import { ViewToggle } from '../components/ViewToggle';

interface AllInsightsPageProps {
  companyInsights: { [key in InsightType]: string[] }; // Инсайты по компаниям
  industryInsights: { [key in InsightType]: string[] };// Инсайты по отраслям
  onBack: () => void;                                  // Функция для возврата на дашборд
  initialTab?: InsightType;                            // Вкладка, которая будет активна при открытии
  initialMode?: AnalysisMode;                          // Режим анализа, который будет активен при открытии
}

// Конфигурация вкладок для удобного рендеринга и управления
const TABS: { key: InsightType; label: string }[] = [
  { key: 'critical', label: 'Критические события' },
  { key: 'positive', label: 'Точки роста' },
  { key: 'warning', label: 'Зоны внимания' },
  { key: 'info', label: 'Интересные факты' },
];

// Количество элементов на одной странице пагинации
const ITEMS_PER_PAGE = 10;

export const AllInsightsPage: React.FC<AllInsightsPageProps> = ({ companyInsights, industryInsights, onBack, initialTab = 'critical', initialMode = 'company' }) => {
  // Состояние для отслеживания активной вкладки (критические, позитивные и т.д.)
  const [activeTab, setActiveTab] = useState<InsightType>(initialTab);
  // Состояние для отслеживания текущей страницы пагинации
  const [currentPage, setCurrentPage] = useState(1);
  // Состояние для отслеживания режима анализа ('company' или 'industry')
  const [analysisMode, setAnalysisMode] = useState<AnalysisMode>(initialMode);

  // В зависимости от выбранного режима анализа, подставляем нужный набор инсайтов для текущей вкладки
  const currentInsights = (analysisMode === 'company' ? companyInsights : industryInsights)[activeTab];

  /**
   * Мемоизированный расчет инсайтов для текущей страницы.
   * `useMemo` кэширует результат, и пересчет происходит только если изменился
   * список инсайтов (`currentInsights`) или номер страницы (`currentPage`).
   */
  const paginatedInsights = useMemo(() => {
    const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
    const endIndex = startIndex + ITEMS_PER_PAGE;
    return currentInsights.slice(startIndex, endIndex);
  }, [currentInsights, currentPage]);

  // Расчет общего количества страниц для пагинации
  const totalPages = Math.ceil(currentInsights.length / ITEMS_PER_PAGE);

  /**
   * Обработчик клика по вкладке. Меняет активную вкладку и сбрасывает пагинацию на 1 страницу.
   */
  const handleTabClick = (tab: InsightType) => {
    setActiveTab(tab);
    setCurrentPage(1);
  };

  /**
   * Обработчик смены режима анализа. Также сбрасывает пагинацию.
   */
  const handleModeChange = (mode: AnalysisMode) => {
    setAnalysisMode(mode);
    setCurrentPage(1);
  }

  return (
    <div className="p-4 sm:p-6 lg:p-8">
      {/* Кнопка возврата */}
       <button onClick={onBack} className="mb-6 text-blue-400 hover:text-blue-300">&larr; Назад на дашборд</button>

      {/* Переключатель режимов анализа */}
      <ViewToggle mode={analysisMode} setMode={handleModeChange} />
      
      {/* Навигация по вкладкам */}
      <div className="border-b border-gray-700 mt-6 mb-6">
        <nav className="-mb-px flex space-x-6" aria-label="Tabs">
          {TABS.map(tab => (
            <button
              key={tab.key}
              onClick={() => handleTabClick(tab.key)}
              className={`${
                activeTab === tab.key
                  ? 'border-blue-500 text-blue-400'
                  // Динамические классы для стилизации активной и неактивной вкладки
                  : 'border-transparent text-gray-400 hover:text-gray-200 hover:border-gray-500'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors`}
              aria-current={activeTab === tab.key ? 'page' : undefined}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Список инсайтов для текущей страницы */}
      <div className="space-y-4 min-h-[400px]">
        {paginatedInsights.map((insight, index) => (
          <div key={index} className="bg-gray-800 p-4 rounded-lg border border-gray-700 animate-fade-in">
            <p className="text-gray-200">{insight}</p>
          </div>
        ))}
        {/* Сообщение, если инсайтов в данной категории нет */}
         {paginatedInsights.length === 0 && (
            <div className="flex items-center justify-center h-full text-center py-10 text-gray-500">
                <p>Нет данных для отображения в этой категории.</p>
            </div>
        )}
      </div>

      {/* Компонент пагинации */}
      <Pagination
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={setCurrentPage}
      />
    </div>
  );
};