import json
import os
import requests
import gzip
import shutil
import random
import numpy as np


def load_dataset(min_num):
    with open("data/database.json", "r") as f:
        data = json.load(f)

    loaded_data = {}
    for cty, embeds in data.items():
        if len(embeds) >= min_num:
            loaded_data[cty] = random.sample(embeds, min_num)
    return loaded_data


def load_test(file_tmstp, num):
    url = f"http://data.gdeltproject.org/gdeltv3/gsg_docembed/{file_tmstp}.gsg.docembed.json.gz"
    zip_path = f"{file_tmstp}.gz"
    file_path = f"{file_tmstp}.json"
    # Perform the download
    response = requests.get(url)
    # Save the file locally
    with open(zip_path, 'wb') as f:
        f.write(response.content)
    with gzip.open(zip_path, 'rb') as f_in:
        with open(file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    # read the data
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Parse each line as a separate JSON object
            row_data = json.loads(line.strip())
            data.append(row_data["docembed"])
    os.remove(zip_path)
    os.remove(file_path)
    return random.sample(data, num)


def cosine_similarity(vec1, vec2):
    # Convert lists to numpy arrays if necessary
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    # Compute the dot product of the vectors
    dot_product = np.dot(vec1, vec2)
    # Compute the norm (magnitude) of the vectors
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    # Compute the cosine similarity
    cosine_sim = dot_product / (norm_vec1 * norm_vec2)
    return cosine_sim


def doc_similarity(d_embed, articles_embed):
    score = 0
    for a_embed in articles_embed:
        new_score = cosine_similarity(d_embed, a_embed)
        score = max(score, new_score)
    return score


if __name__ == "__main__":
    timestamp = "20240710000000"
    min_num = 40
    test_num = 100
    database = load_dataset(min_num)
    data = load_test(timestamp, test_num)

    peace_num = 0
    for d in data:
        score_dict = {}
        for loc, articles in database.items():
            similar_score = doc_similarity(d, articles)
            score_dict[loc] = similar_score
        opt_loc = max(score_dict, key=score_dict.get)
        if opt_loc not in ["Bangladesh", "Kenya", "Nigeria", "Tanzania"]:
            peace_num += 1
    print("The proportion of peaceful articles is: {}".format(peace_num/test_num))

