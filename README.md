# AC4b_Summer2024

There are three folders in this repository: database, prediction, and data_diz.

## database folder
* `file_loader.py`: download dataset from the database based on timestamp (optional: get original articles).
* `country_recog.py`: detect the country which the article is about.
* `country_filter.py`: get articles from pre-defined country list.
* `database_merge.py`: merge datasets of different timestamps into one signle file.

## prediction folder
* `classification.py`: classify an article based on its embedding and cosine similarity with other articles.
* `evaluation.py`: evaluate the accuracy rate of classification.

## data_viz folder
* `draw_word_cloud.py`: draw the wordcloud of online articles based on word frequency.
* `line_graph.py`: draw the changes of the number of articles at different timepoints.
* `t-sne.py`: perform dimension reduction on embeddings of articles.
