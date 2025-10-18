import requests
from bs4 import BeautifulSoup
import json
import sys
from pathlib import Path
import re
import time
import random

# Список User-Agent для имитации разных браузеров
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/110.0.1587.63",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/110.0",
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def fetch_html(url):
    """Загружает HTML-содержимое с указанного URL с случайным User-Agent и задержкой."""
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'DNT': '1', # Do Not Track
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    # Случайная задержка перед запросом
    time.sleep(random.uniform(2, 5)) # Задержка от 2 до 5 секунд

    try:
        response = requests.get(url, headers=headers, timeout=10) # Таймаут 10 секунд
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.text
    except requests.exceptions.Timeout:
        print(f"Ошибка: Таймаут при загрузке страницы {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке страницы {url}: {e}")
        return None

def extract_region_code(url):
    """Извлекает код региона из URL."""
    match = re.search(r'/city/(\d+)', url)
    if match:
        return match.group(1)
    return None

def parse_company_page(company_url):
    """Парсит страницу компании и извлекает ИНН, ОГРН, ОКПО."""
    html_content = fetch_html(company_url)
    if not html_content:
        return {}

    soup = BeautifulSoup(html_content, 'html.parser')
    company_details = {}

    # Пример извлечения ИНН, ОГРН, ОКПО из ul.horizontal-list
    ul_list = soup.find('ul', class_='horizontal-list')
    if ul_list:
        for li in ul_list.find_all('li'):
            text = li.get_text(strip=True)
            if text.startswith('ИНН'):
                company_details['inn'] = text.replace('ИНН ', '')
            elif text.startswith('ОГРН'):
                company_details['ogrn'] = text.replace('ОГРН ', '')
            elif text.startswith('ОКПО'):
                company_details['okpo'] = text.replace('ОКПО ', '')
    return company_details

def parse_spark_companies(regions_json_path, output_json_path):
    """
    Парсит страницы рейтинга компаний для каждого региона и извлекает данные о компаниях.
    """
    regions_file = Path(regions_json_path)
    if not regions_file.exists():
        print(f'Ошибка: Файл {regions_file} не найден.')
        sys.exit(1)

    with open(regions_file, 'r', encoding='utf-8') as f:
        regions_data = json.load(f)

    all_companies_data = []

    for region in regions_data:
        region_name = region['name']
        region_url = region['url']
        region_code = extract_region_code(region_url)

        if not region_code:
            print(f"Не удалось извлечь код региона из URL: {region_url}. Пропускаем.")
            continue

        # Формируем URL для первой страницы рейтинга компаний
        rating_url = f"https://spark-interfax.ru/statistics/rating/{region_code}"
        print(f"Парсинг компаний для региона: {region_name} ({rating_url})")

        html_content = fetch_html(rating_url)
        if not html_content:
            print(f"  Не удалось загрузить страницу рейтинга для {region_name}. Пропускаем регион.")
            continue

        soup = BeautifulSoup(html_content, 'html.parser')

        # Находим все ссылки на компании
        company_links = soup.find_all('a', class_='card-list__wrapper-link')

        if not company_links:
            print(f"  Компании не найдены на странице рейтинга для {region_name}.")
            continue

        for link in company_links:
            company_full_url = requests.compat.urljoin(rating_url, link['href'])
            company_name_tag = link.find('h3', class_='card-list__company-name')
            company_name = company_name_tag.get_text(strip=True) if company_name_tag else "Название не найдено"

            company_info = {
                "region_name": region_name,
                "company_name": company_name,
                "company_url": company_full_url,
            }
            
            # Если нужно парсить каждую страницу компании для ИНН, ОГРН, ОКПО
            # company_details = parse_company_page(company_full_url)
            # company_info.update(company_details)

            all_companies_data.append(company_info)
        
        # Случайная задержка между запросами к регионам
        time.sleep(random.uniform(3, 7)) # Задержка от 3 до 7 секунд

    # Сохраняем все собранные данные в JSON-файл
    output_file = Path(output_json_path)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_companies_data, f, indent=4, ensure_ascii=False)

    print(f"\nВсе данные о компаниях успешно извлечены и сохранены в {output_file}.")
    print(f"Всего найдено {len(all_companies_data)} компаний.")

if __name__ == "__main__":
    # Использование скрипта:
    # python src/web_scraper/parse_spark_companies.py [путь_к_regions_json] [путь_к_output_json]
    regions_input_path = Path("data/web_output") / "spark_regions.json"
    companies_output_path = Path("data/web_output") / "spark_companies.json"

    if len(sys.argv) > 1:
        regions_input_path = Path(sys.argv[1])
    if len(sys.argv) > 2:
        companies_output_path = Path(sys.argv[2])

    parse_spark_companies(regions_input_path, companies_output_path)
