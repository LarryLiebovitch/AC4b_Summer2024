import json
import os


all_data = []
folder = "data"
for file in os.listdir(folder):
    if file.startswith("database"):
        file_dir = os.path.join(folder, file)
        with open(file_dir, "r") as f:
            data = json.load(f)
        all_data += data
country_list = list(set([i["country"] for i in all_data]))

result_dict = {}
for d in all_data:
    country = d["country"]
    result_dict[country] = result_dict.get(country, []) + [d["embed"]]

for d, v in result_dict.items():
    print(d, len(v))

with open(f"{folder}/database.json", "w") as f:
    json.dump(result_dict, f, indent=4)
