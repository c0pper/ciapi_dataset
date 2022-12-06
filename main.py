import json
from pathlib import Path
import pandas as pd

folder = Path("json")


def get_all_categories(json_folder: Path):
    all_cats = []
    for f in json_folder.glob("*"):
        j = json.load(open(f, encoding="UTF8"))
        for c in j["RESPONSE"]["CATEGORIZATION"]:
            domain_field = c["DOMAIN"]

            if isinstance(domain_field, list):
                for d in domain_field:
                    cat_name = d.get("NAME").split("/")[-1].replace(" ", "_").replace(",", "")
                    all_cats.append(cat_name.lower()+"_score")
                    # all_cats.append(cat_name.lower()+"_frequency")

            elif isinstance(domain_field, dict):
                cat_name = domain_field.get("NAME").split("/")[-1].replace(" ", "_").replace(",", "").lower()
                all_cats.append(cat_name.lower()+"_score")
                # all_cats.append(cat_name.lower()+"_frequency")
    return sorted(set(all_cats))


def get_file_domain_list(f: Path):
    domain_list = []

    j = json.load(open(f, encoding="UTF8"))
    text = j["RESPONSE"]["DOCUMENT"]

    for c in j["RESPONSE"]["CATEGORIZATION"]:
        domain_field = c["DOMAIN"]

        if isinstance(domain_field, list):
            for d in domain_field:
                domain = {
                        "NAME": d.get("NAME").split("/")[-1].replace(" ", "_").replace(",", "").lower(),
                        "SCORE": d.get("SCORE"),
                        # "FREQUENCY": d.get("FREQUENCY"),
                        "TEXT": text,
                    }
                domain_list.append(domain)

        elif isinstance(domain_field, dict):
            domain = {
                    "NAME": domain_field.get("NAME").split("/")[-1].replace(" ", "_").replace(",", "").lower(),
                    "SCORE": domain_field.get("SCORE"),
                    # "FREQUENCY": domain_field.get("FREQUENCY"),
                    "TEXT": text,
                }
            domain_list.append(domain)

    # print(f.name)
    # print(domain_list)
    # print("---")
    return domain_list


if __name__ == "__main__":
    all_cats = get_all_categories(folder)
    df_list = []

    for f in folder.glob("*"):
        text = {"text": ""}
        all_cats_dict_initial = dict.fromkeys(all_cats, 0)
        all_cats_dict = {**text, **all_cats_dict_initial}
        print(f.name)

        file_domains_list = get_file_domain_list(f)
        for d in file_domains_list:
            score_label = d["NAME"]+"_score"
            # print(score_label)
            all_cats_dict["text"] = d["TEXT"]
            all_cats_dict[score_label] = d["SCORE"]
            print(score_label, all_cats_dict.get(score_label))
        print(all_cats_dict)
        df_list.append(all_cats_dict)

    df = pd.DataFrame(data=df_list)
    print(df.to_csv("df_ciapi_score.csv", index=False))