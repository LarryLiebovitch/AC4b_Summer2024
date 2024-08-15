import json
from openai import OpenAI
from tqdm import tqdm


# Set up the OpenAI API client
openai_client = OpenAI(
    api_key="<api-key-here>"
)


prompt = """Determine which country the given article is describing about:
article:
{article}
If it is uncertain, return None, otherwise, return the country name. Only return the country name in English or None.
"""


def llm_respond(message):
    chat_rcds = [
        {"role": "user", "content": message}
    ]
    chat_completion = openai_client.chat.completions.create(
        messages=chat_rcds,
        model="gpt-3.5-turbo",
        temperature=0,
    )
    resp = chat_completion
    resp_text = resp.choices[0].message.content
    return resp_text


if __name__ == "__main__":
    time_stamp = "20240701000000"

    with open(f"data/{time_stamp}_article.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    result = []
    for d in tqdm(data):
        try:
            url = d["url"]
            text = d["text"][:1000]
            country = llm_respond(prompt.format(article=text))
            if country != "None":
                d["country"] = country
                result.append(d)
        except:
            continue

    with open(f"data/{time_stamp}_info.json", "w", encoding="utf-8") as file:
        json.dump(result, file, indent=4)
