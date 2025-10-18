/**
 * @file IndustryAnalysisPage.tsx
 * @description Страница для глубокого сравнительного анализа компаний в разрезе отраслей.
 * Группирует компании и для каждой отрасли отображает самодостаточный аналитический блок (`IndustryDetailCard`).
 */
import React, { useMemo } from 'react';
import { CompanyData } from '../types';
import { IndustryDetailCard } from '../components/IndustryDetailCard';

interface IndustryAnalysisPageProps {
    companies: CompanyData[];
}

export const IndustryAnalysisPage: React.FC<IndustryAnalysisPageProps> = ({ companies }) => {

    /**
     * Группирует массив компаний по полю `industry`.
     * `useMemo` используется для кэширования результата, чтобы группировка не выполнялась
     * при каждом рендере, а только при изменении исходного массива `companies`.
     */
    const companiesByIndustry = useMemo(() => {
        return companies.reduce((acc, company) => {
            const industry = company.industry;
            if (!acc[industry]) {
                acc[industry] = [];
            }
            acc[industry].push(company);
            return acc;
        }, {} as { [key: string]: CompanyData[] });
    }, [companies]);

    // Определяем порядок отраслей для более логичного и последовательного отображения на странице.
    const industryOrder = [
        'Пищевая промышленность',
        'Тяжелая промышленность',
        'IT и Электроника',
        'Фармацевтика',
        'Потребительские товары'
    ];
    
    // Фильтруем и сортируем отрасли в соответствии с `industryOrder`.
    const sortedIndustries = industryOrder.filter(industry => companiesByIndustry[industry]);

    return (
        <div className="py-8">
            <div className="text-center mb-10">
                <h1 className="text-4xl font-bold text-white">Анализ по отраслям</h1>
                <p className="text-lg text-gray-400 mt-2">Сравнительный анализ компаний внутри каждого сектора</p>
            </div>

            <div className="space-y-12">
                {sortedIndustries.map(industryName => (
                    // Для каждой отрасли рендерим отдельную карточку с детальным анализом.
                    <IndustryDetailCard
                        key={industryName}
                        industryName={industryName}
                        companies={companiesByIndustry[industryName]}
                    />
                ))}
            </div>
        </div>
    );
};