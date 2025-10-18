import random
from typing import List
from api.models import CompanyData, YearlyData


def generate_yearly_data(start_year: int, end_year: int, base_revenue: float, base_profit: float, base_employees: int, company_name: str) -> List[YearlyData]:
    data: List[YearlyData] = []
    for year in range(start_year, end_year + 1):
        growth_factor = 1 + (random.uniform(-0.05, 0.2))

        revenue = round((base_revenue * growth_factor) * (1 + (year - start_year) * (random.uniform(0.05, 0.1))))
        profit = round((base_profit * growth_factor) * (1 + (year - start_year) * (random.uniform(0.03, 0.15))))
        employees = round((base_employees * (1 + random.uniform(-0.02, 0.05))) * (1 + (year - start_year) * 0.02))

        if year >= 2024 and "Москвич" in company_name:
            revenue *= 2.5
            profit *= 1.5
            employees *= 1.8
        if year == 2025 and "КРАСНЫЙ ОКТЯБРЬ" in company_name:
            profit = round(profit * 0.4)
        if year == 2024 and "Микрон" in company_name:
            profit = round(profit * 1.8)
            revenue = round(revenue * 1.5)

        payroll = round(employees * (90 + random.uniform(0, 40)) * 12)
        personal_income_tax = round(payroll * 0.13)
        profit_tax = round(profit * 0.2) if profit > 0 else 0
        property_tax = round(revenue * 0.01)
        taxes = personal_income_tax + profit_tax + property_tax

        data.append(YearlyData(
            year=year,
            revenue=revenue,
            profit=profit,
            employees=employees,
            taxes=taxes,
            payroll=payroll,
            profitTax=profit_tax,
            propertyTax=property_tax,
            personalIncomeTax=personal_income_tax
        ))
    return data

companies_list = [
  { "name": 'ООО "РУ КМЗ"', "inn": '7721840520', "industry": 'Тяжелая промышленность', "activity": 'Производство металлоконструкций', "r": 600000, "p": 55000, "e": 300 },
  { "name": 'АО "ОМПК"', "inn": '7715034360', "industry": 'Пищевая промышленность', "activity": 'Мясопереработка', "r": 2500000, "p": 180000, "e": 1500 },
  { "name": 'АО "ВБД"', "inn": '7713085659', "industry": 'Пищевая промышленность', "activity": 'Производство молочной продукции', "r": 4000000, "p": 320000, "e": 2200 },
  { "name": 'АО "ГАЗПРОМНЕФТЬ - МНПЗ"', "inn": '7723006328', "industry": 'Тяжелая промышленность', "activity": 'Нефтепереработка', "r": 25000000, "p": 2000000, "e": 4000 },
  { "name": 'ООО "ДОБРОЛЕК"', "inn": '7724774770', "industry": 'Фармацевтика', "activity": 'Производство дженериков', "r": 900000, "p": 150000, "e": 450 },
  { "name": 'АО "Микрон"', "inn": '7735007358', "industry": 'IT и Электроника', "activity": 'Производство микроэлектроники', "r": 1800000, "p": 250000, "e": 1200 },
  { "name": 'АО "КОНДИТЕРСКИЙ КОНЦЕРН БАБАЕВСКИЙ"', "inn": '7708029391', "industry": 'Пищевая промышленность', "activity": 'Производство кондитерских изделий', "r": 1500000, "p": 130000, "e": 1100 },
  { "name": 'АО МАЗ "МОСКВИЧ"', "inn": '7709259743', "industry": 'Тяжелая промышленность', "activity": 'Автомобилестроение', "r": 500000, "p": -50000, "e": 800 },
  { "name": 'ООО "НПП "ИТЭЛМА"', "inn": '7724685256', "industry": 'IT и Электроника', "activity": 'Разработка ПО и электроники для автопрома', "r": 1200000, "p": 200000, "e": 600 },
  { "name": 'АО "ЧМПЗ"', "inn": '7718013714', "industry": 'Пищевая промышленность', "activity": 'Мясопереработка', "r": 1900000, "p": 160000, "e": 1300 },
  { "name": 'АО "ФАБЕРЛИК"', "inn": '5001026970', "industry": 'Потребительские товары', "activity": 'Производство косметики', "r": 2200000, "p": 250000, "e": 900 },
  { "name": 'ООО "НПП "НЕФТЕХИМИЯ"', "inn": '7723332561', "industry": 'Тяжелая промышленность', "activity": 'Химическое производство', "r": 1300000, "p": 110000, "e": 550 },
  { "name": 'ООО "МУЛТОН ПАРТНЕРС"', "inn": '7701215046', "industry": 'Пищевая промышленность', "activity": 'Производство соков и напитков', "r": 3000000, "p": 280000, "e": 1600 },
  { "name": 'АО "МЭЛ"', "inn": '7718014620', "industry": 'Тяжелая промышленность', "activity": 'Производство лифтового оборудования', "r": 800000, "p": 70000, "e": 700 },
  { "name": 'ОАО "РОТ ФРОНТ"', "inn": '7705033216', "industry": 'Пищевая промышленность', "activity": 'Производство кондитерских изделий', "r": 1700000, "p": 150000, "e": 1250 },
  { "name": 'ЗАО БКК "КОЛОМЕНСКИЙ"', "inn": '7724766868', "industry": 'Пищевая промышленность', "activity": 'Хлебобулочное производство', "r": 1100000, "p": 90000, "e": 1400 },
  { "name": 'ООО "ХЛЕБНЫЙ ДОМ"', "inn": '7810356819', "industry": 'Пищевая промышленность', "activity": 'Хлебобулочное производство', "r": 950000, "p": 80000, "e": 1300 },
  { "name": 'ООО "БИФОРКОМ ТЕК"', "inn": '7728313442', "industry": 'IT и Электроника', "activity": 'Производство телеком-оборудования', "r": 700000, "p": 120000, "e": 250 },
  { "name": 'ООО "НПО ПРОМЕТ"', "inn": '7751009218', "industry": 'Тяжелая промышленность', "activity": 'Производство сейфов и металлической мебели', "r": 1000000, "p": 95000, "e": 850 },
  { "name": 'ПАО "КРАСНЫЙ ОКТЯБРЬ"', "inn": '7706043263', "industry": 'Пищевая промышленность', "activity": 'Производство кондитерских изделий', "r": 2100000, "p": 190000, "e": 1450 },
]

def get_mock_company_data() -> List[CompanyData]:
    """
    Основная функция, которая возвращает полный набор демонстрационных данных по всем компаниям.
    """
    START_YEAR = 2023
    END_YEAR = 2025

    return [
        CompanyData(
            id=index + 1,
            name=company["name"],
            inn=company["inn"],
            industry=company["industry"],
            activityType=company["activity"],
            financials=generate_yearly_data(START_YEAR, END_YEAR, company["r"], company["p"], company["e"], company["name"])
        )
        for index, company in enumerate(companies_list)
    ]
