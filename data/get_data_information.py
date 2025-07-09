########## ########## ########## ##########

import os
import statistics

########## ########## ########## ##########

BASE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
BEFORE_REFINE_DIRECTORY = os.path.join(BASE_DIRECTORY, "before_refine")

# Distribute : 0 ~ 50, 51 ~ 100, ... , 251 ~ 300, 300 +
BUCKET_SIZE = 50
MAX_BUCKET = 300

def get_data_information_url_length(file_path) :
    lengths = []

    with open(file_path, 'r', encoding='utf-8') as file :
        for line in file :
            url = line.strip()

            if url :
                lengths.append(len(url))

    information = {
        "count": len(lengths),
        "min_length": min(lengths) if lengths else 0,
        "max_length": max(lengths) if lengths else 0,
        "avg_length": round(sum(lengths) / len(lengths), 2) if lengths else 0.0,
        "med_length": statistics.median(lengths) if lengths else 0,
        "length_distribute": {}
    }

    distribute = {}

    for length in lengths :
        if length > MAX_BUCKET :
            bucket = f"{MAX_BUCKET} +"

        else :
            start = (length // BUCKET_SIZE) * BUCKET_SIZE
            end = start + BUCKET_SIZE

            bucket = f"{start + 1} ~ {end}"

        distribute[bucket] = distribute.get(bucket, 0) + 1

    information["length_distribute"] = dict(sorted(distribute.items()))

    return information

def main() :
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(" [ Get - Data Information ] Length ...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    file_list = sorted(f for f in os.listdir(BEFORE_REFINE_DIRECTORY) if f.endswith(".txt"))

    result = {}

    for filename in file_list :
        file_path = os.path.join(BEFORE_REFINE_DIRECTORY, filename)

        print(f"[ + ] File: {filename}")

        result[filename] = get_data_information_url_length(file_path)

    for filename, information in result.items() :
        print(f"\n[ File: {filename} ]")
        print(f" - Count       : {information['count']}")
        print(f" - Min Length  : {information['min_length']}")
        print(f" - Max Length  : {information['max_length']}")
        print(f" - Avg Length  : {information['avg_length']}")
        print(f" - Med Length  : {information['med_length']}")
        print(" - Distribute  : ")

        for bucket, count in information["length_distribute"].items() :
            print(f"   · {bucket} : {count}")

# Main
if __name__ == "__main__":
    main()