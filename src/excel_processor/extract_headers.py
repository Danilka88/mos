import pandas as pd
import json
import sys
from pathlib import Path

def extract_excel_headers_to_json(excel_file_path, json_file_path):
    """
    Извлекает заголовки из Excel-файла и сохраняет их в JSON-файл.

    Args:
        excel_file_path (str): Путь к входному Excel-файлу.
        json_file_path (str): Путь к выходному JSON-файлу.
    """
    excel_file = Path(excel_file_path)
    if not excel_file.exists():
        print(f'Ошибка: Файл {excel_file} не найден.')
        sys.exit(1)

    # Читаем только заголовки (первую строку)
    df = pd.read_excel(excel_file, nrows=0)
    headers = df.columns.tolist()

    # Преобразуем список заголовков в JSON
    headers_json = json.dumps(headers, indent=4, ensure_ascii=False)

    # Записываем JSON в файл
    json_file = Path(json_file_path)
    with open(json_file, 'w', encoding='utf-8') as f:
        f.write(headers_json)
    print(f'Заголовки из файла {excel_file} успешно преобразованы в {json_file}.')

if __name__ == "__main__":
    # Использование скрипта:
    # python extract_headers.py base.xlsx base_headers.json
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Использование: python extract_headers.py <путь_к_excel_файлу> [путь_к_json_файлу]")
        sys.exit(1)

    excel_input_path = sys.argv[1]
    json_output_path = Path("data/excel_output") / "base_headers.json"
    if len(sys.argv) == 3:
        json_output_path = Path(sys.argv[2])
    
    extract_excel_headers_to_json(excel_input_path, json_output_path)
