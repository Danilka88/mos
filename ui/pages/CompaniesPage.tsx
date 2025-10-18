/**
 * @file CompaniesPage.tsx
 * @description Компонент-страница для отображения списка всех доступных для анализа компаний.
 * Представляет компании в виде сетки интерактивных карточек.
 * Каждая карточка отображает ключевую информацию (название, отрасль, последние фин. показатели)
 * и служит точкой входа на страницу детализации компании.
 */
import React from 'react';
import { CompanyData } from '../types';

interface CompaniesPageProps {
  companies: CompanyData[];
  onSelectCompany: (company: CompanyData) => void;
}

/**
 * Вспомогательная функция для форматирования больших чисел в сокращенный вид (тыс. -> K, млн. -> M).
 * @param num - Число для форматирования.
 * @returns Отформатированная строка.
 */
const formatNumber = (num: number): string => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(0)}K`;
    return num.toString();
};

export const CompaniesPage: React.FC<CompaniesPageProps> = ({ companies, onSelectCompany }) => {
  return (
    <div className="py-8">
      <h2 className="text-3xl font-bold text-white text-center mb-8">Список компаний</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {companies.map(company => {
          // Получаем финансовые данные за последний доступный год.
          const latestFinancials = company.financials[company.financials.length - 1];
          return (
            <div
              key={company.id}
              onClick={() => onSelectCompany(company)}
              className="bg-gray-800 rounded-xl border border-gray-700 p-5 cursor-pointer transition-all duration-300 hover:border-blue-500 hover:shadow-lg hover:-translate-y-1"
              role="button"
              tabIndex={0}
              onKeyPress={(e) => e.key === 'Enter' && onSelectCompany(company)}
              aria-label={`Перейти к деталям компании ${company.name}`}
            >
              <h3 className="text-lg font-bold text-blue-400 truncate" title={company.name}>{company.name}</h3>
              <p className="text-sm text-gray-400 mt-1">{company.industry}</p>
              <div className="mt-4 pt-4 border-t border-gray-700 flex justify-between items-center">
                <div className="text-left">
                    <p className="text-xs text-gray-500">Выручка {latestFinancials.year}</p>
                    <p className="text-md font-semibold text-white">{formatNumber(latestFinancials.revenue)} ₽</p>
                </div>
                 <div className="text-right">
                    <p className="text-xs text-gray-500">Прибыль {latestFinancials.year}</p>
                    <p className={`text-md font-semibold ${latestFinancials.profit > 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {formatNumber(latestFinancials.profit)} ₽
                    </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};