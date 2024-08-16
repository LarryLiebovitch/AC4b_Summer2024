import jieba
import re
from wordcloud import WordCloud
import json
import matplotlib.pyplot as plt


def draw_wdCloud(data):
    # Retrieve English stop words
    stopwords = []
    file = open('utils/stopword.txt', 'r')
    while True:
        line = file.readline()
        stopwords.append(line.replace('\n', ''))
        if not line:
            break
    file.close()

    articles = []
    for i in data:
        pieces = re.sub('[^A-Za-z0-9]+', ' ', i.lower())
        cut = list(jieba.cut(pieces))
        for j in range(len(cut)):
            if cut[j] in stopwords:
                cut[j] = ''
        para = [x.strip() for x in list(cut) if x != '' and x != ' ']
        articles += para

    word_freq = {}
    for word in articles:
        word_freq[word] = word_freq.get(word, 0) + 1

    wordcloud = WordCloud(background_color="white", contour_color="steelblue", contour_width=3)

    wordcloud.generate_from_frequencies(frequencies=word_freq)

    # Display the generated image:
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title('Word Cloud for Non-Peaceful Articles', fontsize=20, color='black')
    plt.xticks([])
    plt.yticks([])
    plt.savefig('NonPeaceWordCloud.png', format='png', dpi=300, bbox_inches="tight", pad_inches=0.1)  # Saves the figure in the current directory with 300 DPI

    return wordcloud

data = json.load(open("data/database_20240627180000.json", "r"))
peace_articles = []
non_articles = []
for d in data:
    if d["country"] in ["Bangladesh", "Kenya", "Nigeria", "Tanzania"]:
        non_articles.append(d["text"])
    else:
        peace_articles.append(d["text"])

draw_wdCloud(non_articles)
