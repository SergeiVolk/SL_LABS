import csv

cars = []
with open("4.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=",")
    for row in reader:
        cars.append(row)
        for key, value in row.items():
            print(f"{key} → {value}")
        print("-" * 40)



def find_min_max_price_car(data):
    min_car = min(data, key=lambda x: int(x["Price"]))
    max_car = max(data, key=lambda x: int(x["Price"]))
    return min_car, max_car

def count_sold_cars(data):
    return sum(1 for car in data if car["Sold"].lower() == "yes")

def calculate_avg_engine_volume(data):
    volumes = [float(car["Engine_Volume"]) for car in data]
    return sum(volumes) / len(volumes)

def count_cars_by_color(data):
    colors = {}
    for car in data:
        color = car["Color"]
        colors[color] = colors.get(color, 0) + 1
    return colors


min_car, max_car = find_min_max_price_car(cars)
print(f"Самый дешёвый: {min_car['Model']} ({min_car['Price']})")
print(f"Самый дорогой: {max_car['Model']} ({max_car['Price']})")
print(f"Продано автомобилей: {count_sold_cars(cars)}")
print(f"Средний объём двигателя: {calculate_avg_engine_volume(cars):.2f}")
print("Количество по цветам:", count_cars_by_color(cars))
