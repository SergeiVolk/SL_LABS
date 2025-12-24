import requests
from bs4 import BeautifulSoup
import csv
import time

base_url = "https://worldathletics.org/records/toplists/throws/{discipline}/outdoor/{gender}/senior/{year}"

disciplines = {
    "shot-put": "Толкание ядра",
    "discus-throw": "Метание диска", 
    "javelin-throw": "Метание копья",
    "hammer-throw": "Метание молота"
}

genders = ["men", "women"]
years = range(2001, 2025)

results = []
count = 0

for discipline in disciplines:
    for gender in genders:
        for year in years:
            count += 1
            print(f"Страница {count}: {disciplines[discipline]}, {gender}, {year}")
            
            url = base_url.format(discipline=discipline, gender=gender, year=year)
            
            try:
                response = requests.get(url, timeout=10)
                
                if response.status_code != 200:
                    continue
                    
                soup = BeautifulSoup(response.content, 'html.parser')
                table = soup.find("table")
                
                if not table:
                    continue
                
                rows = table.find_all("tr")
                
                first_row = rows[1]
                cells = first_row.find_all("td")
                
                if len(cells) >= 4:
                    result = cells[0].get_text(strip=True)
                    athlete = cells[1].get_text(strip=True)
                    country = cells[5].get_text(strip=True)
                    date = cells[3].get_text(strip=True)
                    
                    results.append([
                        year, 
                        disciplines[discipline], 
                        gender,
                        athlete, 
                        country, 
                        result, 
                        date
                    ])

                print(results[-1])
                with open("top_results.csv", "w", newline="" ) as f:
                     writer = csv.writer(f, delimiter=';')
                     writer.writerow(["Год", "Дисциплина", "Пол", "Дата", "Страна", "Результат", "Спортсмен"])
                     writer.writerows(results)

                time.sleep(1)
                
            except:
                continue
