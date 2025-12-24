import requests
import json

url = "https://restcountries.com/v3.1/region/europe"
response = requests.get(url)
data = response.json()

results = []

for country in data:
    name = country.get("name", {}).get("common")
    
    capital_data = country.get("capital")
    if capital_data:
        capital = capital_data[0]

    
    area = country.get("area", 0)
    population = country.get("population", 0)
    
    currencies = country.get("currencies", {})
    currency_names = []
    
    if currencies:
        for currency_code in currencies:
            currency_name = currencies[currency_code].get("name")
            if currency_name:
                currency_names.append(currency_name)

    
    if area > 150000 and "Euro" not in currency_names:
        density = 0
        if area > 0:
            density = population / area
        
        country_info = {
            "name": name,
            "capital": capital,
            "area": area,
            "population": population,
            "currency": ", ".join(currency_names),
            "density": density,
            "flag_url": country.get("flags", {}).get("png", "")
        }
        
        results.append(country_info)

with open("results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

results.sort(key=lambda x: x["density"], reverse=True)
top3 = results[:3]

print("Топ-3 страны по плотности населения:")
for country in top3:
    print(f"{country['name']} - {country['density']:.2f}")

for country in top3:
    flag_url = country["flag_url"]
    if flag_url:
        filename = f"{country['name'].replace(' ', '_')}.png"
        flag_response = requests.get(flag_url)
        
        with open(filename, "wb") as f:
            f.write(flag_response.content)