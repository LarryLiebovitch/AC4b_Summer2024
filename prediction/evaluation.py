import json
import random
import numpy as np


def load_dataset(min_num):
    with open("data/database.json", "r") as f:
        data = json.load(f)

    loaded_data = {}
    for cty, embeds in data.items():
        if len(embeds) >= min_num:
            loaded_data[cty] = random.sample(embeds, min_num)
    print(loaded_data.keys())
    return loaded_data


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
    min_num = 40
    database = load_dataset(min_num)
    with open("data/database_20240628120000.json", "r") as f:
        data = json.load(f)
    score = 0
    for d_item in data:
        score_dict = {}
        d = d_item["embed"]
        country = d_item["country"]
        for loc, articles in database.items():
            similar_score = doc_similarity(d, articles)
            score_dict[loc] = similar_score
        opt_loc = max(score_dict, key=score_dict.get)
        if opt_loc not in ["Bangladesh", "Kenya", "Nigeria", "Tanzania"]:
            pred = True
        else:
            pred = False
        if country not in ["Bangladesh", "Kenya", "Nigeria", "Tanzania"]:
            label = True
        else:
            label = False
        if pred == label:
            score += 1
    print("The accuracy rate is: {}".format(score/len(data)))
