import json


def convert_country(country):
    if any([i in country for i in ["United Kingdom", "UK", "England", "Britain"]]):
        return "United Kingdom"
    elif country in ["Australia", "Canada", "Ireland", "New Zealand", "Singapore", "Bangladesh", "Kenya", "Nigeria", "Tanzania"]:
        return country
    return None


if __name__ == "__main__":
    time_stamp = "20240701000000"
    with open(f"data/{time_stamp}_info.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    database = []
    for d in data:
        country = convert_country(d["country"])
        if country:
            d["country"] = country
            database.append(d)
    print(len(database))
    with open(f"data/database_{time_stamp}.json", "w", encoding="utf-8") as f:
        json.dump(database, f, indent=4)
