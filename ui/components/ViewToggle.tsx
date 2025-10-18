/**
 * @file ViewToggle.tsx
 * @description Компонент-переключатель для выбора режима анализа (по компаниям / по отраслям).
 */
import React from 'react';
// FIX: The AnalysisMode type is now imported from the central types file.
import { AnalysisMode } from '../types';

interface ViewToggleProps {
  mode: AnalysisMode;
  setMode: (mode: AnalysisMode) => void;
}

/**
 * Компонент ViewToggle представляет собой стилизованный переключатель (toggle)
 * для выбора одного из двух режимов анализа.
 * @param {ViewToggleProps} props - Свойства компонента.
 * @returns {React.ReactElement} React-компонент.
 */
export const ViewToggle: React.FC<ViewToggleProps> = ({ mode, setMode }) => {
  return (
    <div className="flex justify-center">
        <div className="relative flex w-full max-w-sm p-1 bg-gray-700 rounded-full">
            <span
                className="absolute top-1 bottom-1 transition-all duration-300 ease-in-out bg-blue-600 rounded-full"
                style={{
                    width: 'calc(50% - 4px)', // 50% минус отступы
                    left: mode === 'company' ? '4px' : 'calc(50% + 4px)',
                }}
            />
            <button
                onClick={() => setMode('company')}
                className="relative z-10 w-1/2 py-2 text-sm font-semibold text-center text-white transition-colors duration-300 rounded-full"
            >
                Анализ по компаниям
            </button>
            <button
                onClick={() => setMode('industry')}
                className="relative z-10 w-1/2 py-2 text-sm font-semibold text-center text-white transition-colors duration-300 rounded-full"
            >
                Анализ по отраслям
            </button>
        </div>
    </div>
  );
};
