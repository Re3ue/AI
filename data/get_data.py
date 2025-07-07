########## ########## ########## ##########

import os
import requests
from urllib.parse import urlparse

########## ########## ########## ##########

BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

BEFORE_REFINE_DIRECTORY = os.path.join(BASE_DIRECTORY, "before_refine")

os.makedirs(BEFORE_REFINE_DIRECTORY, exist_ok=True)

GET_DATA_LIST = [
    {
        "url" : "https://raw.githubusercontent.com/Phishing-Database/Phishing.Database/refs/heads/master/phishing-links-ACTIVE.txt",
        "link_file_name" : "phishing_link_active.txt",
    },
    {
        "url" : "https://raw.githubusercontent.com/Phishing-Database/Phishing.Database/refs/heads/master/phishing-links-INACTIVE.txt",
        "link_file_name" : "phishing_link_inactive.txt",
    },
    {
        "url" : "https://raw.githubusercontent.com/Phishing-Database/Phishing.Database/refs/heads/master/phishing-links-NEW-today.txt",
        "link_file_name" : "phishing_ink_today.txt",
    },
]

def get_data_phishing() :
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(" [ Get - Data ] Phishing ...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    for item in GET_DATA_LIST :

        print(f"[ + ] Work : {item['url']}")

        response = requests.get(item["url"])
        url_list = response.text.strip().splitlines()

        link_file_path = os.path.join(BEFORE_REFINE_DIRECTORY, item["link_file_name"])

        with open(link_file_path, "w", encoding="utf-8") as file :
            file.write("\n".join(url_list))

        print(f"    => Save Link File ( Path ) : {item['link_file_name']}")

# Main
if __name__ == "__main__":
    get_data_phishing()