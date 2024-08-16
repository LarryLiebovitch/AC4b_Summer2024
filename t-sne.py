from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import json
import numpy as np

# Step 1: Generate synthetic high-dimensional data
data = json.load(open("data/database.json", "r"))
data_x = []
data_y = []
for count, embeds in data.items():
    data_x.extend(embeds)
    if count in ["Bangladesh", "Kenya", "Nigeria", "Tanzania"]:
        data_y.extend(["Non-Peaceful"] * len(embeds))
    else:
        data_y.extend(["Peaceful"] * len(embeds))
data_x = np.array(data_x)
data_y = np.array(data_y)


# Step 3: Dimensionality reduction using t-SNE
tsne = TSNE(n_components=2, random_state=42)
data_reduced = tsne.fit_transform(data_x)

# Step 4: Visualization
# Mapping labels to colors
color_map = {'Peaceful': 'blue', 'Non-Peaceful': 'red'}
colors = [color_map[label] for label in data_y]
plt.figure(figsize=(10, 8))
for label, color in color_map.items():
    idx = data_y == label
    plt.scatter(data_reduced[idx, 0], data_reduced[idx, 1], c=color, label=label, alpha=0.5)
plt.title('Distribution of Peaceful and Non-Peaceful Articles')
plt.xlabel('T-SNE Component 1')
plt.ylabel('T-SNE Component 2')
plt.legend(fontsize=14)
plt.savefig('t-sne.png', format='png', dpi=300, bbox_inches="tight",
            pad_inches=0.1)  # Saves the figure in the current directory with 300 DPI
