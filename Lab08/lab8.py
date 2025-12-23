import requests
import json

# Получаем все страны Азии с нужными полями (добавляем flags и cca2)
response = requests.get("https://restcountries.com/v3.1/region/asia?fields=name,capital,area,population,flags,cca2,cca3")
countries = response.json()

# Фильтруем по населению >30 млн
filtered_countries = []
for country in countries:
    population = country.get('population', 0)
    if population > 30_000_000:
        filtered_countries.append({
            'name': country['name']['common'],
            'capital': country.get('capital', ['N/A'])[0],
            'area': country.get('area', 0),
            'population': population,
            'flag_url': country.get('flags', {}).get('png', ''),  # URL флага из API
            'cca2': country.get('cca2', '').lower(),  # Двухбуквенный код
            'cca3': country.get('cca3', '').lower()   # Трехбуквенный код
        })

# Вычисляем плотность населения
for country in filtered_countries:
    if country['area'] > 0:
        country['density'] = country['population'] / country['area']
    else:
        country['density'] = 0

# Сортируем по плотности и берем топ-5
sorted_countries = sorted(filtered_countries, 
                         key=lambda x: x['density'], 
                         reverse=True)
top_5_countries = sorted_countries[:5]

# Сохраняем все данные в JSON файл
with open('results.json', 'w', encoding='utf-8') as f:
    # Добавляем вычисленную плотность в данные для сохранения
    for country in filtered_countries:
        country_data = {
            'name': country['name'],
            'capital': country['capital'],
            'area': country['area'],
            'population': country['population'],
            'density': country['density']
        }
    json.dump(filtered_countries, f, ensure_ascii=False, indent=2)
print("✅ Данные сохранены в results.json")

# Скачиваем флаги для топ-5 стран
print("\n📥 Скачивание флагов:")
for country in top_5_countries:
    # Пробуем несколько источников по порядку
    flag_downloaded = False
    
    # 1. Используем URL флага из API (если есть)
    if country['flag_url']:
        try:
            response = requests.get(country['flag_url'], timeout=5)
            response.raise_for_status()
            
            filename = f"{country['name'].replace(' ', '_')}_flag.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Флаг {country['name']} скачан из API")
            flag_downloaded = True
            
        except:
            pass  # Переходим к следующему источнику
    
    # 2. Пробуем flagcdn с двухбуквенным кодом
    if not flag_downloaded and country['cca2']:
        try:
            flag_url = f"https://flagcdn.com/w320/{country['cca2']}.png"
            response = requests.get(flag_url, timeout=5)
            response.raise_for_status()
            
            filename = f"{country['name'].replace(' ', '_')}_flag.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Флаг {country['name']} скачан с flagcdn")
            flag_downloaded = True
            
        except requests.exceptions.RequestException as e:
            if not flag_downloaded:
                print(f"❌ Флаг {country['name']} не скачан с flagcdn: {e}")
    
    # 3. Альтернативный источник (flagsapi)
    if not flag_downloaded and country['cca2']:
        try:
            flag_url = f"https://flagsapi.com/{country['cca2'].upper()}/flat/64.png"
            response = requests.get(flag_url, timeout=5)
            if response.status_code == 200:
                filename = f"{country['name'].replace(' ', '_')}_flag.png"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Флаг {country['name']} скачан с flagsapi")
                flag_downloaded = True
        except:
            pass
    
    if not flag_downloaded:
        print(f"⚠️ Не удалось скачать флаг для {country['name']}")

# Выводим топ-5
print("\n" + "="*60)
print("🏆 Топ-5 стран по плотности населения:")
print("="*60)
for i, country in enumerate(top_5_countries, 1):
    print(f"{i}. {country['name']}:")
    print(f"   Столица: {country['capital']}")
    print(f"   Население: {country['population']:,} чел.")
    print(f"   Площадь: {country['area']:,} км²")
    print(f"   Плотность: {country['density']:.2f} чел/км²")
    print(f"   Код страны: {country['cca2'].upper()}/{country['cca3'].upper()}")
    print()