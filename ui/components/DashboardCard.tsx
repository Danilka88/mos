/**
 * @file DashboardCard.tsx
 * @description Универсальный компонент-карточка для отображения графика и вызова ИИ-аналитики по нему.
 */
import React, { useState, useCallback } from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { generateInsightStream } from '../services/geminiService';

// Интерфейс для свойств компонента
interface DashboardCardProps {
    title: string;                               // Заголовок карточки
    data: { year: string; value: number }[];     // Данные для графика
    dataKey: string;                             // Ключ для значений (ось Y)
    xAxisKey: string;                            // Ключ для оси X
    metricName: string;                          // Название метрики для промпта ИИ
    chartType?: 'bar' | 'line';                  // Тип графика (по умолчанию 'bar')
}

// Вспомогательный SVG-компонент иконки "ИИ"
const SparkleIcon: React.FC<{ className?: string }> = ({ className = "h-5 w-5" }) => (
    <svg xmlns="http://www.w3.org/2000/svg" className={className} fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M4 17v4M2 19h4M17 3v4M15 5h4M16 17v4M14 19h4M12 9.5l.5-1 .5 1 .5 1-.5 1-.5-1-.5-1zM9 12l-1 .5 1 .5 1-.5-1-.5zM15 12l-1 .5 1 .5 1-.5-1-.5zM12 14.5l-.5 1 .5 1 .5-1-.5-1z" />
    </svg>
);

export const DashboardCard: React.FC<DashboardCardProps> = ({ title, data, dataKey, xAxisKey, metricName, chartType = 'bar' }) => {
    // Состояние для хранения текста от ИИ
    const [insight, setInsight] = useState<string>('');
    // Состояние загрузки данных от ИИ
    const [isLoading, setIsLoading] = useState<boolean>(false);
    // Состояние для хранения ошибок
    const [error, setError] = useState<string | null>(null);
    // Состояние видимости модального окна
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);

    /**
     * Обработчик для запроса аналитики от ИИ.
     * Использует `useCallback` для мемоизации функции.
     * Функция использует стриминг для отображения текста по мере его генерации.
     */
    const handleFetchInsight = useCallback(async () => {
        if (!data || data.length === 0) return;
        setIsLoading(true);
        setError(null);
        setInsight('');
        setIsModalOpen(true);
        try {
            // Формируем промпт для ИИ-модели, передавая данные и контекст
            const prompt = `Проанализируй эти агрегированные данные по показателю '${metricName}' для промышленных предприятий Москвы. Данные: ${JSON.stringify(data)}. Выяви наиболее значимую тенденцию или аномалию. Предоставь краткий, лаконичный вывод на русском языке (не более 2-3 предложений), на что должен обратить внимание руководитель.`;
            
            // Получаем стрим ответа от Gemini API
            const stream = await generateInsightStream(prompt);
            setIsLoading(false); // Отключаем скелетон, так как сейчас начнется стриминг

            // Асинхронно итерируемся по частям (chunks) ответа
            let fullText = '';
            for await (const chunk of stream) {
                fullText += chunk.text;
                setInsight(fullText); // Обновляем состояние с каждым новым фрагментом текста
            }

        } catch (err) {
            console.error("Ошибка при генерации инсайта:", err);
            setError("Не удалось получить аналитику от ИИ.");
            setIsLoading(false);
        }
    }, [data, metricName]);


    /**
     * Форматирует числа для оси Y, делая их более читаемыми (например, 1000 -> 1K, 1000000 -> 1M).
     */
    const formatNumber = (tickItem: number) => {
        if (tickItem >= 1000000) {
            return `${(tickItem / 1000000).toFixed(1)}M`;
        }
        if (tickItem >= 1000) {
            return `${(tickItem / 1000).toFixed(0)}K`;
        }
        return tickItem.toString();
    };
    
    // Выбираем компонент графика в зависимости от пропса `chartType`
    const ChartComponent = chartType === 'line' ? LineChart : BarChart;
    const ChartElement = chartType === 'line' 
        ? <Line type="monotone" dataKey={dataKey} name={metricName} stroke="#8884d8" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 8 }} /> 
        : <Bar dataKey={dataKey} name={metricName} fill="#3B82F6" />;

    return (
        <div className="bg-gray-800 p-4 sm:p-6 rounded-xl shadow-lg border border-gray-700 hover:border-blue-500 transition-all duration-300">
            <h3 className="text-lg font-semibold text-white mb-4">{title}</h3>
            <div className="h-64 w-full">
                 <ResponsiveContainer width="100%" height="100%">
                    <ChartComponent
                        data={data}
                        margin={{ top: 5, right: 20, left: 20, bottom: 5 }}
                    >
                        <CartesianGrid strokeDasharray="3 3" stroke="#4A5568" />
                        <XAxis dataKey={xAxisKey} stroke="#A0AEC0" />
                        <YAxis stroke="#A0AEC0" tickFormatter={formatNumber} />
                        <Tooltip 
                            contentStyle={{ backgroundColor: '#1A202C', border: '1px solid #4A5568' }}
                            labelStyle={{ color: '#E2E8F0' }}
                        />
                        <Legend wrapperStyle={{ color: '#E2E8F0' }}/>
                        {ChartElement}
                    </ChartComponent>
                </ResponsiveContainer>
            </div>
             <div className="mt-4 border-t border-gray-700 pt-4 flex justify-end">
                <button
                    onClick={handleFetchInsight}
                    disabled={isLoading && isModalOpen}
                    className="flex items-center justify-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg shadow-md transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    <SparkleIcon className="h-5 w-5 mr-2" />
                    {isLoading && isModalOpen ? 'Анализ...' : 'Аналитика ИИ'}
                </button>
            </div>

            {/* Модальное окно для отображения аналитики */}
            {isModalOpen && (
                <div 
                    className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4" 
                    onClick={() => setIsModalOpen(false)} // Закрытие по клику на фон
                    role="dialog"
                    aria-modal="true"
                    aria-labelledby="ai-insight-title"
                >
                    <div 
                        className="bg-gray-800 border border-gray-700 rounded-xl shadow-2xl p-6 w-full max-w-lg flex flex-col max-h-[90vh]" 
                        onClick={e => e.stopPropagation()} // Предотвращаем закрытие по клику на само окно
                    >
                        {/* "Липкий" заголовок модального окна */}
                        <div className="flex-shrink-0">
                            <div className="flex items-start justify-between">
                                <div className="flex items-center">
                                    <SparkleIcon className="h-6 w-6 text-yellow-400" />
                                    <h4 id="ai-insight-title" className="ml-3 text-lg font-semibold text-yellow-400">Аналитика от ИИ</h4>
                                </div>
                                <button onClick={() => setIsModalOpen(false)} className="text-gray-400 hover:text-white text-2xl leading-none" aria-label="Закрыть модальное окно">&times;</button>
                            </div>
                            <p className='text-gray-400 text-sm mb-4'>Анализ по показателю: <span className='font-semibold text-gray-200'>{metricName}</span></p>
                        </div>

                        {/* Контентная часть с прокруткой */}
                        <div className="mt-4 border-t border-gray-700 pt-4 overflow-y-auto">
                            {/* Скелетон загрузки (показывается очень недолго до начала стрима) */}
                            {isLoading && (
                                <div className="animate-pulse space-y-3 pt-2">
                                    <div className="h-4 bg-gray-700 rounded w-5/6"></div>
                                    <div className="h-4 bg-gray-700 rounded w-full"></div>
                                    <div className="h-4 bg-gray-700 rounded w-3/4"></div>
                                </div>
                            )}
                            {error && <p className="text-red-400 text-md">{error}</p>}
                            {/* Отображение текста от ИИ. `whitespace-pre-wrap` сохраняет переносы строк */}
                            {!isLoading && !error && <p className="text-gray-200 text-lg whitespace-pre-wrap">{insight || ' '}</p>}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};
