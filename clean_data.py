import os.path
import csv
import json
from collections import Counter


NUMBER_OF_TOP_ENTRIES = 10

INPUT_FILE = "./data/survey_results_public.csv"
OUTPUT_FILE = "./data/survey_results_public_cleaned.json"

def ensure_file(file_path):
    if not os.path.isfile(file_path):
        system.exit(f"Expected file '{file_path}' but was not found...")

if __name__ == "__main__":
    ensure_file(INPUT_FILE)

    all_languages_have_worked_with = []
    all_languages_want_to_work_with = []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            elements = row["LanguageHaveWorkedWith"].split(";")
            elements = [element for element in elements if element != "NA"]
            all_languages_have_worked_with += elements

            elements = row["LanguageWantToWorkWith"].split(";")
            elements = [element for element in elements if element != "NA"]
            all_languages_want_to_work_with += elements

    # Languages People have worked with
    all_languages_have_worked_with_counter = Counter(all_languages_have_worked_with)

    # Languages People want to work with
    all_languages_want_to_work_with_counter = Counter(all_languages_want_to_work_with)

    # Create dictionary to write out as json
    languagesPeopleHaveWorkedWith = []
    for language, count in all_languages_have_worked_with_counter.most_common(NUMBER_OF_TOP_ENTRIES):
        entry = {"language": language, "count": count}
        languagesPeopleHaveWorkedWith.append(entry)

    languagesPeopleWantToWorkWith = []
    for language, count in all_languages_want_to_work_with_counter.most_common(NUMBER_OF_TOP_ENTRIES):
        entry = {"language": language, "count": count}
        languagesPeopleWantToWorkWith.append(entry)

    output_file_content = {
        "languagesPeopleHaveWorkedWith": languagesPeopleHaveWorkedWith,
        "languagesPeopleWantToWorkWith": languagesPeopleWantToWorkWith
    }

    # Write to json
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output_file_content, f, indent=4)
