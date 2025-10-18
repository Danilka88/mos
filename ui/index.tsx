/**
 * @file index.tsx
 * @description Точка входа в React-приложение. Отвечает за рендеринг корневого компонента в DOM.
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Находим корневой HTML-элемент, в который будет вмонтировано приложение.
const rootElement = document.getElementById('root');
if (!rootElement) {
  // Если элемент не найден, выбрасываем ошибку, так как приложение не сможет запуститься.
  throw new Error("Не удалось найти корневой элемент для монтирования приложения");
}

// Создаем корневой узел рендеринга React 18.
const root = ReactDOM.createRoot(rootElement);

// Рендерим главный компонент приложения — App.
// App.tsx является главным "оркестратором", управляющим состоянием, данными и навигацией.
// React.StrictMode — это инструмент для выявления потенциальных проблем в приложении.
// Он активирует дополнительные проверки и предупреждения для своих потомков.
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);