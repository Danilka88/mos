/**
 * @file CompanyComparisonChart.tsx
 * @description Компонент для отображения круговой диаграммы, сравнивающей компании по определенному показателю.
 */
import React from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { CompanyData } from '../types';

interface CompanyComparisonChartProps {
  data: CompanyData[];          // Полный набор данных по компаниям
  year: number;                 // Год, за который проводится сравнение
  metric: 'revenue' | 'profit'; // Метрика для сравнения ('выручка' или 'прибыль')
  title: string;                // Заголовок карточки
}

// Предопределенные цвета для секторов диаграммы для визуального разнообразия
const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#AF19FF'];

export const CompanyComparisonChart: React.FC<CompanyComparisonChartProps> = ({ data, year, metric, title }) => {
  // Подготавливаем данные для диаграммы:
  // 1. Извлекаем для каждой компании финансовые данные за нужный год.
  // 2. Создаем массив объектов с именем компании и значением выбранной метрики.
  // 3. Фильтруем компании с нулевым или отрицательным значением, чтобы они не портили диаграмму.
  const chartData = data.map(company => ({
    name: company.name,
    value: company.financials.find(f => f.year === year)?.[metric] || 0
  })).filter(d => d.value > 0);

  return (
    <div className="bg-gray-800 p-4 sm:p-6 rounded-xl shadow-lg border border-gray-700 hover:border-blue-500 transition-all duration-300">
      <h3 className="text-lg font-semibold text-white mb-4">{title}</h3>
      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%" // Центр по X
              cy="50%" // Центр по Y
              labelLine={false} // Не показывать линии к меткам
              outerRadius={80} // Внешний радиус
              fill="#8884d8"
              dataKey="value" // Ключ данных для значения сектора
              nameKey="name"  // Ключ данных для имени сектора (отображается в тултипе)
            >
              {/* Применяем цвета к каждому сектору циклически, чтобы они не повторялись */}
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            {/* Тултип для отображения деталей при наведении */}
            <Tooltip
              contentStyle={{ backgroundColor: '#1A202C', border: '1px solid #4A5568' }}
              labelStyle={{ color: '#E2E8F0' }}
            />
            {/* Легенда для сопоставления цветов и названий компаний */}
             <Legend wrapperStyle={{ color: '#E2E8F0', paddingTop: '20px' }}/>
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};