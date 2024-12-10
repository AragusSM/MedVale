import requests
import os
import pandas as pd

# Replace with your API key and Custom Search Engine ID
API_KEY = "AIzaSyCN5x8RPAaujuTxVF_I0buWwjywMDCfqbA"
CX = "74cb130fa1945489c"

table = pd.read_csv("micro_nodes.csv")
terms = table["Name"]
ids = table["Id"]
ids = ids.iloc[297:579].tolist()
search_terms = terms.iloc[297:579].tolist()


# Directory to save downloaded images
output_dir = "google_cc_images"
os.makedirs(output_dir, exist_ok=True)

# Number of images per search term
num_images = 1


def search_and_download_images(query, identity):
    print(f"Searching for: {query}")
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": query,
        "searchType": "image",
        "rights": "cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial",
        "num": num_images,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json()
        for idx, item in enumerate(results.get("items", [])):
            image_url = item["link"]
            try:
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    file_path = os.path.join(output_dir, f"{identity}.jpg")
                    with open(file_path, "wb") as file:
                        file.write(image_response.content)
                    print(f"Downloaded: {file_path}")
            except Exception as e:
                print(f"Failed to download image: {e}")
    else:
        print(f"Error: {response.status_code}, {response.text}")


# Download images for each search term
for i in range(len(search_terms)):
    term = search_terms[i]
    identity = ids[i]
    search_and_download_images(term, identity)
