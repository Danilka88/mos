/**
 * @file Pagination.tsx
 * @description Переиспользуемый компонент для навигации по страницам.
 */
import React from 'react';

// Интерфейс для свойств компонента
interface PaginationProps {
  currentPage: number;        // Текущая активная страница
  totalPages: number;         // Общее количество страниц
  onPageChange: (page: number) => void; // Функция обратного вызова при смене страницы
}

export const Pagination: React.FC<PaginationProps> = ({ currentPage, totalPages, onPageChange }) => {
  // Если страница всего одна (или меньше), компонент не отображается
  if (totalPages <= 1) return null;

  // Обработчик перехода на предыдущую страницу
  const handlePrev = () => {
    if (currentPage > 1) {
      onPageChange(currentPage - 1);
    }
  };

  // Обработчик перехода на следующую страницу
  const handleNext = () => {
    if (currentPage < totalPages) {
      onPageChange(currentPage + 1);
    }
  };

  return (
    <div className="flex justify-center items-center space-x-4 mt-8">
      <button
        onClick={handlePrev}
        disabled={currentPage === 1} // Кнопка "Назад" неактивна на первой странице
        className="px-4 py-2 bg-gray-700 text-white rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-600"
      >
        Назад
      </button>
      <span className="text-gray-300">
        Страница {currentPage} из {totalPages}
      </span>
      <button
        onClick={handleNext}
        disabled={currentPage === totalPages} // Кнопка "Вперед" неактивна на последней странице
        className="px-4 py-2 bg-gray-700 text-white rounded-md disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-600"
      >
        Вперед
      </button>
    </div>
  );
};
