/**
 * @file AnomalyCard.tsx
 * @description Этот файл определяет компонент `InsightCard`.
 * Компонент отображает список ключевых выводов (инсайтов) от ИИ-агента определенного типа
 * (критические, позитивные и т.д.) на главном дашборде.
 * Показывает превью из нескольких инсайтов и позволяет перейти к полному списку.
 * Поддерживает drill-down (детализацию) по каждому инсайту в модальном окне.
 */
import React, { useState } from 'react';
import { generateInsightStream } from '../services/geminiService';
import { CompanyData, InsightType } from '../types';

// Блок с SVG-иконками для разных типов инсайтов
const AlertIcon: React.FC = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
    </svg>
);
const WarningIcon: React.FC = () => (
     <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
);
const PositiveIcon: React.FC = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
    </svg>
);
const InfoIcon: React.FC = () => (
   <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
);
const SparkleIcon: React.FC<{ className?: string }> = ({ className = "h-5 w-5" }) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M4 17v4M2 19h4M17 3v4M15 5h4M16 17v4M14 19h4M12 9.5l.5-1 .5 1 .5 1-.5 1-.5-1-.5-1zM9 12l-1 .5 1 .5 1-.5-1-.5zM15 12l-1 .5 1 .5 1-.5-1-.5zM12 14.5l-.5 1 .5 1 .5-1-.5-1z" />
    </svg>
);

interface InsightCardProps {
    title: string;          // Заголовок карточки
    type: InsightType;      // Тип инсайта для стилизации и логики
    insights: string[];     // Массив заголовков инсайтов для отображения
    isLoading: boolean;     // Флаг загрузки списка инсайтов
    error: string | null;   // Сообщение об ошибке
    fullData: CompanyData[];// Полные данные для передачи в ИИ для детализации
    onViewAll: (type: InsightType) => void; // Колбэк для перехода на страницу всех событий
}

// Конфигурационный объект для стилизации карточек в зависимости от их типа
const config: { [key in InsightType]: {
    borderColor: string;
    bgColor: string;
    textColor: string;
    icon: React.FC;
}} = {
    critical: { borderColor: 'border-red-500/50', bgColor: 'bg-red-500/10', textColor: 'text-red-400', icon: AlertIcon },
    warning: { borderColor: 'border-yellow-500/50', bgColor: 'bg-yellow-500/10', textColor: 'text-yellow-400', icon: WarningIcon },
    positive: { borderColor: 'border-green-500/50', bgColor: 'bg-green-500/10', textColor: 'text-green-400', icon: PositiveIcon },
    info: { borderColor: 'border-blue-500/50', bgColor: 'bg-blue-500/10', textColor: 'text-blue-400', icon: InfoIcon },
};

export const InsightCard: React.FC<InsightCardProps> = ({ title, type, insights, isLoading, error, fullData, onViewAll }) => {
    // Состояния для модального окна детализации
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
    const [selectedInsight, setSelectedInsight] = useState<string | null>(null);
    const [detail, setDetail] = useState<string>('');
    const [isDetailLoading, setIsDetailLoading] = useState<boolean>(false);

    const cardConfig = config[type];
    const Icon = cardConfig.icon;

    /**
     * Обрабатывает клик по заголовку инсайта.
     * Открывает модальное окно и запускает запрос к ИИ для получения подробной информации.
     * Это пример "двухэтапного" ИИ-агента: сначала он дает заголовки, потом детали по запросу.
     * @param insight - Текст заголовка, по которому нужна детализация.
     */
    const handleInsightClick = async (insight: string) => {
        setSelectedInsight(insight);
        setIsModalOpen(true);
        setIsDetailLoading(true);
        setDetail('');
        try {
            // Упрощаем данные для экономии токенов
            const summarizedData = fullData.map(c => ({
                name: c.name,
                financials: c.financials.map(f => ({ year: f.year, profit: f.profit, revenue: f.revenue }))
            }));
            // Формируем промпт для детализации
            const detailPrompt = `На основе этих данных: ${JSON.stringify(summarizedData)}. Раскрой подробнее следующий вывод: '${insight}'. Объясни, почему это важно, в 2-3 предложениях на русском языке. Ответ должен быть прямым и сфокусированным на проблеме.`;
            
            // Используем стриминг для получения ответа
            const stream = await generateInsightStream(detailPrompt);
            setIsDetailLoading(false);

            let fullText = '';
            for await (const chunk of stream) {
                fullText += chunk.text;
                setDetail(fullText);
            }
        } catch (err) {
            setDetail("Не удалось загрузить детальную информацию.");
            setIsDetailLoading(false);
        }
    };

    return (
        <div className={`flex flex-col bg-gray-800/50 backdrop-blur-sm p-6 rounded-xl shadow-lg border-2 ${cardConfig.borderColor} h-full`}>
            <div className="flex items-center mb-4">
                <div className={`w-12 h-12 ${cardConfig.bgColor} rounded-full flex items-center justify-center border ${cardConfig.borderColor} ${cardConfig.textColor}`}>
                    <Icon />
                </div>
                <h3 className={`ml-4 text-xl font-bold ${cardConfig.textColor}`}>{title}</h3>
            </div>
            <div className="flex-grow space-y-3">
                {/* Скелетон во время загрузки списка инсайтов */}
                {isLoading && (
                    <div className="animate-pulse space-y-3 pt-2">
                        <div className="h-5 bg-gray-700 rounded w-full"></div>
                        <div className="h-5 bg-gray-700 rounded w-5/6"></div>
                        <div className="h-5 bg-gray-700 rounded w-full"></div>
                    </div>
                )}
                {error && <p className="text-gray-300">{error}</p>}
                {/* Отображаем первые 3 инсайта как кликабельные кнопки */}
                {!isLoading && !error && insights.slice(0, 3).map((insight, index) => (
                    <button 
                        key={index}
                        onClick={() => handleInsightClick(insight)}
                        className="w-full text-left p-3 bg-gray-700/50 hover:bg-gray-700 rounded-md transition-colors duration-200 text-gray-200"
                        aria-label={`Узнать подробнее о: ${insight}`}
                    >
                        {insight}
                    </button>
                ))}
                 {!isLoading && !error && insights.length === 0 && <p className="text-gray-400">Нет событий для отображения.</p>}
            </div>
             <div className="mt-4 border-t border-gray-700 pt-4 flex justify-end">
                <button
                    onClick={() => onViewAll(type)}
                    className="text-sm font-semibold text-blue-400 hover:text-blue-300"
                >
                    Смотреть все &rarr;
                </button>
            </div>
            {/* Модальное окно для детализации */}
            {isModalOpen && (
                 <div 
                    className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4" 
                    onClick={() => setIsModalOpen(false)}
                    role="dialog"
                    aria-modal="true"
                    aria-labelledby="ai-insight-title"
                >
                    <div 
                        className="bg-gray-800 border border-gray-700 rounded-xl shadow-2xl p-6 w-full max-w-lg flex flex-col max-h-[90vh]" 
                        onClick={e => e.stopPropagation()}
                    >
                        <div className="flex-shrink-0">
                             <div className="flex items-start justify-between">
                                <div className="flex items-center">
                                    <SparkleIcon className="h-6 w-6 text-yellow-400" />
                                    <h4 id="ai-insight-title" className="ml-3 text-lg font-semibold text-yellow-400">Расширенная аналитика</h4>
                                </div>
                                <button onClick={() => setIsModalOpen(false)} className="text-gray-400 hover:text-white text-2xl leading-none" aria-label="Закрыть модальное окно">&times;</button>
                            </div>
                            <p className='text-gray-400 text-sm mb-4 mt-2 border-t border-gray-700 pt-4'>
                                <span className='font-semibold text-gray-200'>{selectedInsight}</span>
                            </p>
                        </div>

                        <div className="overflow-y-auto">
                            {/* Скелетон во время загрузки деталей */}
                            {isDetailLoading && (
                                <div className="animate-pulse space-y-3 pt-2">
                                    <div className="h-4 bg-gray-700 rounded w-5/6"></div>
                                    <div className="h-4 bg-gray-700 rounded w-full"></div>
                                    <div className="h-4 bg-gray-700 rounded w-3/4"></div>
                                </div>
                            )}
                            {/* Отображение детальной информации от ИИ */}
                            {!isDetailLoading && <p className="text-gray-200 text-lg whitespace-pre-wrap">{detail || ' '}</p>}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};