/**
 * @file TaxBreakdownChart.tsx
 * @description Компонент для отображения диаграммы, показывающей разбивку по видам налогов за определенный год.
 */
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { CompanyData } from '../types';

interface TaxBreakdownChartProps {
  data: CompanyData[];
  year: number;
  title: string;
}

export const TaxBreakdownChart: React.FC<TaxBreakdownChartProps> = ({ data, year, title }) => {
  // 1. Агрегируем (суммируем) данные по каждому виду налога со всех компаний за указанный год.
  const taxData = {
    profitTax: 0,
    propertyTax: 0,
    personalIncomeTax: 0,
  };

  data.forEach(company => {
    const yearData = company.financials.find(f => f.year === year);
    if (yearData) {
      taxData.profitTax += yearData.profitTax;
      taxData.propertyTax += yearData.propertyTax;
      taxData.personalIncomeTax += yearData.personalIncomeTax;
    }
  });

  // 2. Преобразуем агрегированные данные в формат, который понимает библиотека `recharts`.
  const chartData = [
    { name: 'Налог на прибыль', value: taxData.profitTax },
    { name: 'Налог на имущество', value: taxData.propertyTax },
    { name: 'НДФЛ', value: taxData.personalIncomeTax },
  ];

  // 3. Функция форматирования чисел для оси X (тысячи -> K, миллионы -> M) для лучшей читаемости.
  const formatNumber = (tickItem: number) => {
    if (tickItem >= 1000000) return `${(tickItem / 1000000).toFixed(1)}M`;
    if (tickItem >= 1000) return `${(tickItem / 1000).toFixed(0)}K`;
    return tickItem.toString();
  };

  return (
    <div className="bg-gray-800 p-4 sm:p-6 rounded-xl shadow-lg border border-gray-700 hover:border-blue-500 transition-all duration-300">
      <h3 className="text-lg font-semibold text-white mb-4">{title}</h3>
      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          {/* Используем горизонтальный BarChart (`layout="vertical"`) для лучшей читаемости названий налогов. */}
          <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 20, left: 50, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#4A5568" />
            <XAxis type="number" stroke="#A0AEC0" tickFormatter={formatNumber} />
            <YAxis type="category" dataKey="name" stroke="#A0AEC0" width={120} />
            <Tooltip
              contentStyle={{ backgroundColor: '#1A202C', border: '1px solid #4A5568' }}
              labelStyle={{ color: '#E2E8F0' }}
            />
            <Bar dataKey="value" name="Сумма (тыс. руб.)" fill="#82ca9d" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};