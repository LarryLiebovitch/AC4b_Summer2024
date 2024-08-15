import os
import requests
import gzip
import shutil
from bs4 import BeautifulSoup
from tqdm import tqdm
import json


def download_file(file_tmstp):
    url = f"http://data.gdeltproject.org/gdeltv3/gsg_docembed/{file_tmstp}.gsg.docembed.json.gz"
    folder = "data"
    if not os.path.exists(folder):
        os.mkdir(folder)
    zip_path = os.path.join(folder, f"{file_tmstp}.gz")
    file_path = os.path.join(folder, f"{file_tmstp}.json")
    # Perform the download
    response = requests.get(url)
    # Save the file locally
    with open(zip_path, 'wb') as f:
        f.write(response.content)
    with gzip.open(zip_path, 'rb') as f_in:
        with open(file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(zip_path)
    return file_path


def crawl_articles(f_path):
    url_list = []
    with open(f_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Parse each line as a separate JSON object
            row_data = json.loads(line.strip())
            url_list.append({"url": row_data["url"], "embed": row_data["docembed"]})
    # http request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'
    }
    article_list = []
    for row in tqdm(url_list):
        try:
            url = row["url"]
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                text_output = soup.get_text(separator=" ", strip=True)
                article_list.append({"url": url, "text": text_output, "embed": row["embed"]})
        except:
            pass
    return article_list


if __name__ == "__main__":
    time_stamp = "20240701000000"
    file_path = download_file(time_stamp)
    # article_dict = crawl_articles(file_path)
    # with open("data/" + time_stamp + f"_article.json", 'w', encoding='utf-8') as f:
    #     json.dump(article_dict, f, indent=4)
