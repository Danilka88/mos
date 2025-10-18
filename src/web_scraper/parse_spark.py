import requests
from bs4 import BeautifulSoup
import json
import sys
from pathlib import Path

def parse_spark_regions(url, output_json_path):
    """
    Парсит HTML-страницу Spark-Interfax, извлекает ссылки и названия регионов
    из таблицы и сохраняет их в JSON-файл.

    Args:
        url (str): URL страницы для парсинга.
        output_json_path (str): Путь к выходному JSON-файлу.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке страницы: {e}")
        sys.exit(1)

    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим таблицу по классу
    table = soup.find('table', class_='table table-num collapsed full-width js-regions-list')

    if not table:
        print("Ошибка: Таблица с указанным классом не найдена.")
        sys.exit(1)

    regions_data = []
    # Находим все <td>, содержащие <a>
    for td in table.find_all('td'):
        link = td.find('a')
        if link and 'href' in link.attrs:
            name = link.get_text(strip=True)
            href = link['href']
            # Добавляем полный URL, если ссылка относительная
            if not href.startswith('http'):
                href = requests.compat.urljoin(url, href)
            regions_data.append({"name": name, "url": href})

    # Сохраняем данные в JSON-файл
    output_file = Path(output_json_path)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(regions_data, f, indent=4, ensure_ascii=False)

    print(f"Данные успешно извлечены и сохранены в {output_file}.")
    print(f"Найдено {len(regions_data)} регионов.")

if __name__ == "__main__":
    # Использование скрипта:
    # python parse_spark.py <URL> <путь_к_json_файлу>
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Использование: python parse_spark.py <URL> [путь_к_json_файлу]")
        sys.exit(1)

    target_url = sys.argv[1]
    output_json_file = Path("data/web_output") / "spark_regions.json"
    if len(sys.argv) == 3:
        output_json_file = Path(sys.argv[2])
    
    parse_spark_regions(target_url, output_json_file)
