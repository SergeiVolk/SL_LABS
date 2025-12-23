import json

with open("4.json", "r", encoding="utf-8") as f:
    data = json.load(f)

apps = data["applications"]



def find_apps_by_version(apps, version):
    return [app for app in apps if app["version"] == version]

def calculate_avg_users_per_app(apps):
    total_users = sum(app["users"] for app in apps)
    return total_users / len(apps)

def find_apps_by_category(apps, category):
    return [app for app in apps if app["category"].lower() == category.lower()]

def save_filtered_to_json(filtered, filename="out.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)


print("Среднее количество пользователей:", calculate_avg_users_per_app(apps))

print("Приложения категории 'Games':")
games = find_apps_by_category(apps, "Games")
for g in games:
    print(g["name"], g["users"])

save_filtered_to_json(games, "out.json")
