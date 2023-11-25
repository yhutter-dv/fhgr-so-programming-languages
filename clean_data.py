import os.path
import csv
import json
from collections import Counter


if __name__ == "__main__":
    input_file = "./data/survey_results_public.csv"
    output_file = "./data/survey_results_public_cleaned.json"
    if not os.path.isfile(input_file):
        print(f"Expected input file {input_file} not found")
        exit(1)

    all_languages_have_worked_with = []
    all_languages_want_to_work_with = []

    all_misc_tech_have_worked_with = []
    all_misc_tech_want_to_work_with = []

    all_webframeworks_have_worked_with = []
    all_webframeworks_want_to_work_with = []

    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            elements = row["LanguageHaveWorkedWith"].split(";")
            elements = [element for element in elements if element != "NA"]
            all_languages_have_worked_with += elements

            elements = row["LanguageWantToWorkWith"].split(";")
            elements = [element for element in elements if element != "NA"]
            all_languages_want_to_work_with += elements

            elements = row["MiscTechHaveWorkedWith"].split(";")
            elements = [element for element in elements if element != "NA"]
            all_misc_tech_have_worked_with += elements

            elements = row["MiscTechWantToWorkWith"].split(";")
            elements = [element for element in elements if element != "NA"]
            all_misc_tech_want_to_work_with += elements

            elements = row["WebframeHaveWorkedWith"].split(";")
            elements = [element for element in elements if element != "NA"]
            all_webframeworks_have_worked_with += elements

            elements = row["WebframeWantToWorkWith"].split(";")
            elements = [element for element in elements if element != "NA"]
            all_webframeworks_want_to_work_with += elements

    # Languages People have worked with
    all_languages_have_worked_with_counter = Counter(
        all_languages_have_worked_with)

    # Languages People want to work with
    all_languages_want_to_work_with_counter = Counter(
        all_languages_want_to_work_with)

    # Other Technologies People have worked with"
    all_misc_tech_have_worked_with_counter = Counter(
        all_misc_tech_have_worked_with)

    # Other Technologies People want to work with
    all_misc_tech_want_to_work_with_counter = Counter(
        all_misc_tech_want_to_work_with)

    # Web Frameworks People have worked with
    all_webframeworks_have_worked_with_counter = Counter(
        all_webframeworks_have_worked_with)

    # Web Frameworks People want to work with
    all_webframeworks_want_to_work_with_counter = Counter(
        all_webframeworks_want_to_work_with)

    # Create dictionary to write out as json and compute percentage values
    # Only do this for the top 10...

    languagesPeopleHaveWorkedWith = []
    total_elements = sum(all_languages_have_worked_with_counter.values())
    for language, count in all_languages_have_worked_with_counter.most_common(10):
        entry = {"language": language, "count": count,
                 "percentage": (count / total_elements * 100.0)}
        languagesPeopleHaveWorkedWith.append(entry)

    languagesPeopleWantToWorkWith = []
    total_elements = sum(all_languages_want_to_work_with_counter.values())
    for language, count in all_languages_want_to_work_with_counter.most_common(10):
        entry = {"language": language, "count": count,
                 "percentage": (count / total_elements * 100.0)}
        languagesPeopleWantToWorkWith.append(entry)

    webframeworksPeopleHaveWorkedWith = []
    total_elements = sum(all_webframeworks_have_worked_with_counter.values())
    for webframework, count in all_webframeworks_have_worked_with_counter.most_common(10):
        entry = {"webframework": webframework, "count": count,
                 "percentage": (count / total_elements * 100.0)}
        webframeworksPeopleHaveWorkedWith.append(entry)

    webframeworksPeopleWantToWorkWith = []
    total_elements = sum(all_webframeworks_want_to_work_with_counter.values())
    for webframework, count in all_webframeworks_want_to_work_with_counter.most_common(10):
        entry = {"webframework": webframework, "count": count,
                 "percentage": (count / total_elements * 100.0)}
        webframeworksPeopleWantToWorkWith.append(entry)

    otherFrameworksPeopleHaveWorkedWith = []
    total_elements = sum(all_misc_tech_have_worked_with_counter.values())
    for framework, count in all_misc_tech_have_worked_with_counter.most_common(10):
        entry = {"framework": framework, "count": count,
                 "percentage": (count / total_elements * 100.0)}
        otherFrameworksPeopleHaveWorkedWith.append(entry)

    otherFrameworksPeopleWantToWorkWith = []
    total_elements = sum(all_misc_tech_want_to_work_with_counter.values())
    for framework, count in all_misc_tech_want_to_work_with_counter.most_common(10):
        entry = {"framework": framework, "count": count,
                 "percentage": (count / total_elements * 100.0)}
        otherFrameworksPeopleWantToWorkWith.append(entry)

    output_file_content = {
        "languagesPeopleHaveWorkedWith": languagesPeopleHaveWorkedWith,
        "languagesPeopleWantToWorkWith": languagesPeopleWantToWorkWith,
        "webFrameworksPeopleHaveWorkedWith": webframeworksPeopleHaveWorkedWith,
        "webFrameworksPeopleWantToWorkWith": webframeworksPeopleWantToWorkWith,
        "otherFrameworksPeopleHaveWorkedWith": otherFrameworksPeopleHaveWorkedWith,
        "otherFrameworksPeopleWantToWorkWith": otherFrameworksPeopleWantToWorkWith
    }

    # Write to json
    with open(output_file, "w") as f:
        json.dump(output_file_content, f, indent=4)
