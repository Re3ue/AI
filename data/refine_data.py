########## ########## ########## ##########

import os

########## ########## ########## ##########

BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

BEFORE_REFINE_DIRECTORY = os.path.join(BASE_DIRECTORY, "before_refine")
AFTER_REFINE_DIRECTORY = os.path.join(BASE_DIRECTORY, "after_refine")

os.makedirs(AFTER_REFINE_DIRECTORY, exist_ok=True)

REFINE_LIST = [
    "phishing_link_active.txt",
    "phishing_link_inactive.txt",
    "phishing_ink_today.txt",
]

MIN_LENGTH = 10
MAX_LENGTH = 60

def refine_data_phishing() :
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(" [ Refine - Data ] Phishing ...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    for filename in REFINE_LIST :
        input_path = os.path.join(BEFORE_REFINE_DIRECTORY, filename)
        output_path = os.path.join(AFTER_REFINE_DIRECTORY, filename)

        if not os.path.isfile(input_path) :
            print(f"[ - ] Fail - Fail to Find File : {filename}")
            
            continue

        before_refine_urls = []

        with open(input_path, "r", encoding="utf-8") as file :
            for line in file :
                line = line.strip()

                if line :
                    before_refine_urls.append(line)

        after_refine_urls = []

        for url in before_refine_urls :
            if MIN_LENGTH <= len(url) <= MAX_LENGTH :
                after_refine_urls.append(url)

        with open(output_path, "w", encoding="utf-8") as file :
            file.write("\n".join(after_refine_urls))

        ratio = round((len(after_refine_urls) / len(before_refine_urls)) * 100, 2)

        print(f"[ + ] Success : {filename} => After - {len(after_refine_urls)} / Before - {len(before_refine_urls)} ( {ratio}% )")

########## ########## ########## ##########

if __name__ == "__main__":
    refine_data_phishing()