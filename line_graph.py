import os
import requests
import gzip
import shutil
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
    url_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Parse each line as a separate JSON object
            row_data = json.loads(line.strip())
            url_list.append({"url": row_data["url"], "embed": row_data["docembed"]})
    os.remove(zip_path)
    os.remove(file_path)
    return len(url_list)


if __name__ == "__main__":
    len_list = []
    time_stamp = 20240627000000
    for i in range(24):
        num = download_file(time_stamp)
        time_stamp += 10000
        len_list.append(num)
    print(len_list)
