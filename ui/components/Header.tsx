/**
 * @file Header.tsx
 * @description Компонент заголовка и навигации приложения.
 */
import React from 'react';

// Определяем все возможные страницы для навигации
type Page = 'dashboard' | 'insights' | 'companies' | 'companyDetail' | 'industryAnalysis';
// Определяем страницы, на которые можно перейти напрямую из хедера
type SettablePage = 'dashboard' | 'insights' | 'companies' | 'industryAnalysis';

/**
 * @interface HeaderProps
 * @description Свойства, принимаемые компонентом Header.
 * @param page - Текущая активная страница. Включает 'companyDetail' для корректной подсветки вкладок.
 * @param setPage - Функция обратного вызова для изменения текущей страницы в родительском компоненте App.
 */
interface HeaderProps {
    page: Page;
    setPage: (page: SettablePage) => void;
}

/**
 * Компонент Header отображает заголовок приложения и кнопки для навигации
 * между основными разделами: дашборд, компании, анализ по отраслям и все события.
 * @param props - Свойства компонента, включая текущую страницу и функцию для ее смены.
 */
export const Header: React.FC<HeaderProps> = ({ page, setPage }) => {
    // Для кнопок "Компании" и "Детализация компании" активной должна быть одна и та же вкладка "Компании".
    const isCompaniesActive = page === 'companies' || page === 'companyDetail';

    return (
        <header className="py-4">
            <div className="text-center">
                 <h1 className="text-3xl sm:text-4xl font-bold text-white tracking-tight">
                    Индустриальные данные Москвы
                </h1>
                <p className="mt-2 text-lg text-blue-300">
                    Аналитическая панель с автоматическим выявлением аномалий на базе ИИ
                </p>
            </div>
            {/* Навигационное меню */}
             <nav className="mt-6 flex flex-wrap justify-center gap-2 sm:space-x-4">
                <button 
                    onClick={() => setPage('dashboard')}
                    // Динамически применяем стили в зависимости от активной страницы
                    className={`px-3 sm:px-4 py-2 rounded-md text-sm font-medium transition-colors ${page === 'dashboard' ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-700'}`}
                    aria-current={page === 'dashboard' ? 'page' : undefined}
                >
                    Главный дашборд
                </button>
                 <button 
                    onClick={() => setPage('companies')}
                    className={`px-3 sm:px-4 py-2 rounded-md text-sm font-medium transition-colors ${isCompaniesActive ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-700'}`}
                    aria-current={isCompaniesActive ? 'page' : undefined}
                >
                    Компании
                </button>
                <button 
                    onClick={() => setPage('industryAnalysis')}
                    className={`px-3 sm:px-4 py-2 rounded-md text-sm font-medium transition-colors ${page === 'industryAnalysis' ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-700'}`}
                    aria-current={page === 'industryAnalysis' ? 'page' : undefined}
                >
                    Анализ по отраслям
                </button>
                <button 
                    onClick={() => setPage('insights')}
                    className={`px-3 sm:px-4 py-2 rounded-md text-sm font-medium transition-colors ${page === 'insights' ? 'bg-blue-600 text-white' : 'text-gray-300 hover:bg-gray-700'}`}
                     aria-current={page === 'insights' ? 'page' : undefined}
                >
                    Все события
                </button>
            </nav>
        </header>
    );
};