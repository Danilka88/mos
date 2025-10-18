/**
 * @file CompanyDetailPage.tsx
 * @description Страница с детальной информацией и аналитикой по одной выбранной компании.
 * Отображает:
 * - Ключевые метрики за последний год.
 * - График динамики выручки и прибыли по годам.
 * - Результаты анализа от специального ИИ-агента (#3), сгенерированные для этой компании.
 */
import React, { useState, useEffect } from 'react';
import { CompanyData, InsightType } from '../types';
import { fetchSingleCompanyInsights } from '../services/geminiService';
import { ComposedChart, Bar, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface CompanyDetailPageProps {
  company: CompanyData;
  onBack: () => void;
}

// Конфигурация для стилизации и заголовков карточек инсайтов
const insightConfig: { [key in InsightType]: { title: string; borderColor: string; textColor: string; } } = {
    critical: { title: 'Критические события', borderColor: 'border-red-500/80', textColor: 'text-red-400' },
    positive: { title: 'Точки роста', borderColor: 'border-green-500/80', textColor: 'text-green-400' },
    warning: { title: 'Зоны внимания', borderColor: 'border-yellow-500/80', textColor: 'text-yellow-400' },
    info: { title: 'Интересные факты', borderColor: 'border-blue-500/80', textColor: 'text-blue-400' },
};
// Определяем порядок отображения карточек
const insightOrder: InsightType[] = ['critical', 'positive', 'warning', 'info'];

// Вспомогательные функции для форматирования чисел
const formatNumber = (num: number): string => {
    if (num === 0) return '0';
    return new Intl.NumberFormat('ru-RU').format(num);
};
const formatForAxis = (tickItem: number) => {
    if (tickItem >= 1000000) return `${(tickItem / 1000000).toFixed(1)}M`;
    if (tickItem >= 1000) return `${(tickItem / 1000).toFixed(0)}K`;
    return tickItem.toString();
};

export const CompanyDetailPage: React.FC<CompanyDetailPageProps> = ({ company, onBack }) => {
  // Состояние для хранения инсайтов, сгенерированных ИИ для этой компании
  const [insights, setInsights] = useState<{ [key in InsightType]: string[] } | null>(null);
  // Состояние для управления загрузкой инсайтов
  const [loading, setLoading] = useState(true);

  // Эффект для загрузки аналитики при монтировании компонента или смене компании
  useEffect(() => {
    const loadInsights = async () => {
      setLoading(true);
      // Вызываем специальный "ИИ-агент" для анализа одной компании
      const result = await fetchSingleCompanyInsights(company);
      setInsights(result);
      setLoading(false);
    };
    loadInsights();
  }, [company]); // Перезапускаем эффект, если изменился объект `company`
  
  const latestFin = company.financials[company.financials.length - 1];
  const chartData = company.financials.map(f => ({ ...f, year: f.year.toString() }));

  return (
    <div className="py-8">
      <button onClick={onBack} className="mb-6 text-blue-400 hover:text-blue-300">&larr; Назад к списку компаний</button>
      
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white">{company.name}</h1>
        <p className="text-gray-400 mt-2">ИНН: {company.inn} &bull; {company.industry}</p>
      </div>

      {/* Блок с ключевыми метриками */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8">
          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
              <p className="text-sm text-gray-400">Выручка за {latestFin.year} г.</p>
              <p className="text-3xl font-bold text-white mt-1">{formatNumber(latestFin.revenue)} тыс. ₽</p>
          </div>
          <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
              <p className="text-sm text-gray-400">Чистая прибыль за {latestFin.year} г.</p>
              <p className={`text-3xl font-bold mt-1 ${latestFin.profit >= 0 ? 'text-green-400' : 'text-red-400'}`}>{formatNumber(latestFin.profit)} тыс. ₽</p>
          </div>
           <div className="bg-gray-800 p-6 rounded-xl border border-gray-700">
              <p className="text-sm text-gray-400">Сотрудники ({latestFin.year} г.)</p>
              <p className="text-3xl font-bold text-white mt-1">{formatNumber(latestFin.employees)} чел.</p>
          </div>
      </div>
      
      {/* График финансовых показателей */}
      <div className="bg-gray-800 p-6 rounded-xl border border-gray-700 mb-8">
        <h3 className="text-lg font-semibold text-white mb-4">Финансовые показатели по годам (тыс. руб.)</h3>
        <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
                {/* ComposedChart позволяет комбинировать столбцы и линии на одном графике */}
                <ComposedChart data={chartData} margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#4A5568" />
                    <XAxis dataKey="year" stroke="#A0AEC0" />
                    <YAxis yAxisId="left" stroke="#3B82F6" tickFormatter={formatForAxis} label={{ value: 'Выручка', angle: -90, position: 'insideLeft', fill: '#A0AEC0' }} />
                    <YAxis yAxisId="right" orientation="right" stroke="#22C55E" tickFormatter={formatForAxis} label={{ value: 'Прибыль', angle: 90, position: 'insideRight', fill: '#A0AEC0' }} />
                    <Tooltip contentStyle={{ backgroundColor: '#1A202C', border: '1px solid #4A5568' }} />
                    <Legend wrapperStyle={{ color: '#E2E8F0' }}/>
                    <Bar yAxisId="left" dataKey="revenue" name="Выручка" fill="#3B82F6" />
                    <Line yAxisId="right" type="monotone" dataKey="profit" name="Прибыль" stroke="#22C55E" strokeWidth={2} />
                </ComposedChart>
            </ResponsiveContainer>
        </div>
      </div>
      
      {/* Блок с аналитикой от ИИ */}
      <div className="text-center mb-6">
         <h2 className="text-3xl font-bold text-white">Аналитика от ИИ</h2>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {insightOrder.map(type => (
          <div key={type} className={`bg-gray-800/50 p-6 rounded-xl border-2 ${insightConfig[type].borderColor}`}>
            <h3 className={`text-xl font-bold mb-4 ${insightConfig[type].textColor}`}>{insightConfig[type].title}</h3>
            {loading ? (
              // Скелетон загрузки на время получения данных от ИИ
              <div className="animate-pulse space-y-3 pt-2">
                <div className="h-4 bg-gray-700 rounded w-full"></div>
                <div className="h-4 bg-gray-700 rounded w-5/6"></div>
              </div>
            ) : (
              // Отображение списка инсайтов
              <ul className="space-y-3 list-disc list-inside">
                {insights && insights[type].map((item, index) => (
                  <li key={index} className="text-gray-200">{item}</li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};