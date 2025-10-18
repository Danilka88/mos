/**
 * @file IndustryDetailCard.tsx
 * @description Компонент-карточка для детального анализа одной конкретной отрасли.
 * Включает в себя:
 * - Сводную информацию.
 * - Сравнительные графики компаний внутри отрасли (лидеры по выручке, отклонение от средней рентабельности).
 * - Сводную таблицу данных.
 * - Аналитические выводы от специализированного ИИ-агента (#4).
 */
import React, { useEffect, useState, useMemo } from 'react';
import { CompanyData, InsightType, YearlyData } from '../types';
import { fetchIndustrySpecificInsights } from '../services/geminiService';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from 'recharts';

// Определяем интерфейс для свойств компонента
interface IndustryDetailCardProps {
    industryName: string;
    companies: CompanyData[];
}

// Конфигурация для стилизации карточек инсайтов
const insightConfig: { [key in InsightType]: { title: string; borderColor: string; textColor: string; } } = {
    critical: { title: 'Критические события', borderColor: 'border-red-500/80', textColor: 'text-red-400' },
    positive: { title: 'Точки роста', borderColor: 'border-green-500/80', textColor: 'text-green-400' },
    warning: { title: 'Зоны внимания', borderColor: 'border-yellow-500/80', textColor: 'text-yellow-400' },
    info: { title: 'Интересные факты', borderColor: 'border-blue-500/80', textColor: 'text-blue-400' },
};
const insightOrder: InsightType[] = ['critical', 'positive', 'warning', 'info'];

// Вспомогательные функции для форматирования
const formatNumber = (num: number): string => new Intl.NumberFormat('ru-RU').format(num);
const formatForAxis = (tickItem: number) => {
    if (Math.abs(tickItem) >= 1000000) return `${(tickItem / 1000000).toFixed(1)}M`;
    if (Math.abs(tickItem) >= 1000) return `${(tickItem / 1000).toFixed(0)}K`;
    return tickItem.toString();
};

export const IndustryDetailCard: React.FC<IndustryDetailCardProps> = ({ industryName, companies }) => {
    const [insights, setInsights] = useState<{ [key in InsightType]: string[] } | null>(null);
    const [loading, setLoading] = useState(true);

    // Загружаем инсайты от ИИ-агента #4 при монтировании компонента или смене данных
    useEffect(() => {
        const loadInsights = async () => {
            setLoading(true);
            const result = await fetchIndustrySpecificInsights(companies);
            setInsights(result);
            setLoading(false);
        };
        loadInsights();
    }, [companies]);

    // --- Расчеты и подготовка данных для графиков ---
    // Мемоизируем вычисление последнего отчетного года
    const latestYear = useMemo(() => {
        if (companies.length === 0) return new Date().getFullYear();
        return Math.max(...companies[0].financials.map(f => f.year));
    }, [companies]);
    
    // Мемоизируем подготовку данных для сравнительного графика по выручке
    const revenueComparisonData = useMemo(() => {
        return companies
            .map(c => ({
                name: c.name.substring(0, 25) + (c.name.length > 25 ? '...' : ''), // Обрезаем длинные названия
                value: c.financials.find(f => f.year === latestYear)?.revenue ?? 0,
            }))
            .sort((a, b) => b.value - a.value); // Сортируем по убыванию, чтобы лидеры были сверху
    }, [companies, latestYear]);

    // Мемоизируем подготовку данных для графика отклонения рентабельности от средней по отрасли
    const profitabilityData = useMemo(() => {
        // 1. Рассчитываем рентабельность для каждой компании
        const companyProfitability = companies.map(c => {
            const latestFin = c.financials.find(f => f.year === latestYear);
            const profitability = (latestFin && latestFin.revenue > 0) ? (latestFin.profit / latestFin.revenue) * 100 : 0;
            return { name: c.name.substring(0, 25) + (c.name.length > 25 ? '...' : ''), value: profitability };
        });

        // 2. Находим среднюю рентабельность по отрасли
        const totalProfitability = companyProfitability.reduce((sum, item) => sum + item.value, 0);
        const averageProfitability = companyProfitability.length > 0 ? totalProfitability / companyProfitability.length : 0;

        // 3. Считаем отклонение рентабельности каждой компании от среднего значения
        return companyProfitability.map(item => ({
            ...item,
            deviation: item.value - averageProfitability 
        })).sort((a,b) => b.deviation - a.deviation); // Сортируем, чтобы лучшие были сверху
    }, [companies, latestYear]);

    // Если в отрасли нет компаний, не рендерим карточку
    if (companies.length === 0) return null;

    return (
        <section className="bg-gray-800/50 border border-gray-700 rounded-2xl p-6 sm:p-8" aria-labelledby={`industry-title-${industryName.replace(/\s/g, '-')}`}>
            <h2 id={`industry-title-${industryName.replace(/\s/g, '-')}`} className="text-3xl font-bold text-blue-300 mb-2">{industryName}</h2>
            <p className="text-gray-400 mb-6">Количество компаний в выборке: {companies.length}</p>

            {/* Блок с графиками и таблицей */}
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 mb-8">
                {/* График №1: Лидеры отрасли по выручке */}
                <div className="bg-gray-800 p-4 rounded-xl border border-gray-700 min-h-[300px]">
                     <h3 className="text-lg font-semibold text-white mb-4">Лидеры по выручке, {latestYear} г. (тыс. руб)</h3>
                     <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={revenueComparisonData} layout="vertical" margin={{ top: 5, right: 20, left: 50, bottom: 5 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#4A5568" />
                            <XAxis type="number" stroke="#A0AEC0" tickFormatter={formatForAxis} />
                            <YAxis type="category" dataKey="name" stroke="#A0AEC0" width={150} />
                            <Tooltip contentStyle={{ backgroundColor: '#1A202C', border: '1px solid #4A5568' }} formatter={(value:number) => `${formatNumber(value)} тыс. руб`} />
                            <Bar dataKey="value" name="Выручка" fill="#3B82F6" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
                
                {/* График №2: Отклонение рентабельности от средней */}
                <div className="bg-gray-800 p-4 rounded-xl border border-gray-700 min-h-[300px]">
                    <h3 className="text-lg font-semibold text-white mb-4">Рентабельность vs Средняя по отрасли, %</h3>
                     <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={profitabilityData} layout="vertical" margin={{ top: 5, right: 20, left: 50, bottom: 5 }}>
                             <CartesianGrid strokeDasharray="3 3" stroke="#4A5568" />
                             <XAxis type="number" stroke="#A0AEC0" domain={['auto', 'auto']} tickFormatter={(v) => `${v.toFixed(1)}%`} />
                             <YAxis type="category" dataKey="name" stroke="#A0AEC0" width={150} />
                             <Tooltip contentStyle={{ backgroundColor: '#1A202C', border: '1px solid #4A5568' }} formatter={(value:number) => `${value.toFixed(2)}%`} />
                             {/* Линия отсчета (среднее значение) */}
                             <ReferenceLine x={0} stroke="#A0AEC0" strokeDasharray="2 2" />
                             <Bar dataKey="deviation" name="Отклонение от среднего">
                                {/* Динамическая раскраска столбцов: зеленый для >0, красный для <0 */}
                                {profitabilityData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={entry.deviation >= 0 ? '#22C55E' : '#EF4444'} />
                                ))}
                             </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>

                {/* Таблица с данными */}
                <div className="bg-gray-800 p-4 rounded-xl border border-gray-700 xl:col-span-2">
                     <h3 className="text-lg font-semibold text-white mb-4">Сводные данные, {latestYear} г. (тыс. руб)</h3>
                     <div className="overflow-x-auto">
                        <table className="w-full text-sm text-left text-gray-300">
                             <thead className="text-xs text-gray-400 uppercase bg-gray-700/50">
                                <tr>
                                    <th scope="col" className="px-4 py-3">Компания</th>
                                    <th scope="col" className="px-4 py-3 text-right">Выручка</th>
                                    <th scope="col" className="px-4 py-3 text-right">Прибыль</th>
                                    <th scope="col" className="px-4 py-3 text-right">Сотрудники</th>
                                </tr>
                             </thead>
                             <tbody>
                                {companies.map(c => {
                                    const fin = c.financials.find(f => f.year === latestYear) as YearlyData;
                                    return (
                                        <tr key={c.id} className="border-b border-gray-700 hover:bg-gray-700/30">
                                            <td className="px-4 py-2 font-medium text-white truncate max-w-xs">{c.name}</td>
                                            <td className="px-4 py-2 text-right">{formatNumber(fin.revenue)}</td>
                                            <td className={`px-4 py-2 text-right font-semibold ${fin.profit >= 0 ? 'text-green-400' : 'text-red-400'}`}>{formatNumber(fin.profit)}</td>
                                            <td className="px-4 py-2 text-right">{formatNumber(fin.employees)}</td>
                                        </tr>
                                    );
                                })}
                             </tbody>
                        </table>
                     </div>
                </div>
            </div>

            {/* Блок с аналитикой от ИИ */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {insightOrder.map(type => (
                    <div key={type} className={`bg-gray-800/50 p-6 rounded-xl border-2 ${insightConfig[type].borderColor}`}>
                        <h4 className={`text-xl font-bold mb-4 ${insightConfig[type].textColor}`}>{insightConfig[type].title}</h4>
                        {loading ? (
                            <div className="animate-pulse space-y-3 pt-2">
                                <div className="h-4 bg-gray-700 rounded w-full"></div>
                                <div className="h-4 bg-gray-700 rounded w-5/6"></div>
                            </div>
                        ) : (
                            <ul className="space-y-3 list-disc list-inside">
                                {insights && insights[type].map((item, index) => (
                                <li key={index} className="text-gray-200">{item}</li>
                                ))}
                            </ul>
                        )}
                    </div>
                ))}
            </div>
        </section>
    );
};