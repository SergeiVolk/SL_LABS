import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://worldathletics.org/records/toplists/sprints/{distance}/all/{gender}/senior/{year}"

distances = ["60-metres", "100-metres", "200-metres", "400-metres"]
genders = ["men", "women"]
years = range(2001, 2025)

with open("top_results.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        f"{'Год':<6}"  
        f"{'Пол':<7}" 
        f"{'Дисциплина':<12}" 
        f"{'Имя':<35}"
        f"{'Страна':<8}"  
        f"{'Результат':<11}" 
        f"{'Дата':<12}"
    ])

    for year in years:
        for gender in genders:
            for distance in distances:
                url = BASE_URL.format(distance = distance, gender = gender, year = year)
                print(f"Обрабатываю: {year}, {gender}, {distance}")
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                table = soup.find('table', class_='records-table')
                if table:
                    tbody = table.find('tbody')
                    first_tr = tbody.find('tr')

                    mark_cell = first_tr.find('td', {'data-th': 'Mark'})
                    competitor_cell = first_tr.find('td', {'data-th': 'Competitor'})
                    nat_cell = first_tr.find('td', {'data-th': 'Nat'})
                    date_cell = first_tr.find('td', {'data-th': 'Date'})

                    time = mark_cell.text.strip()
                    name = competitor_cell.text.strip()
                    country = nat_cell.text.strip()
                    date = date_cell.text.strip()

                    writer.writerow([
                        f"{year:<6}"  
                        f"{gender:<7}" 
                        f"{distance:<12}"
                        f"{name:<35}"
                        f"{country:<8}"
                        f"{time:<11}"
                        f"{date:<12}"
                    ])

print("Файл top_results.csv создан")