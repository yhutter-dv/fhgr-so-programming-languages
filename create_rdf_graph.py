import os
import json
from rdflib import Graph, Namespace, BNode, Literal

from queries import *

def create_graph():
    g = Graph()

    # Define namespaces.
    # List of RDF Namespaces can be found here: https://www.mediawiki.org/wiki/Wikibase/Indexing/RDF_Dump_Format#Predicates
    namespaces = {
        "default": Namespace("http://www.fhgr.ch/ke-e/yhutter/so-programming-languages"),
        "wd": Namespace("http://www.wikidata.org/entity/"),
        "wdt": Namespace("http://www.wikidata.org/prop/direct/"),
    }

    # Bind all namespaces so that they do not need to be defined via PREFIX in queries...
    for name, ns in namespaces.items():
        g.bind(name, ns)

    return g

def get_programming_language_subjects(programming_languages):
    # Store a list with the found subject and the associated label
    # e.g http://www.wikidata.org/entity/Q2005 => JavaScript
    programming_language_subjects = dict()
    for language in programming_languages:
        query = PROGRAMMING_LANGUAGE_QUERY.replace("%programming_language%", language.lower())
        result = g.query(query)
        number_of_results = len(result)
        if number_of_results == 0:
            print(f"No result found for {language}, skipping...")
            continue
        elif number_of_results == 1:
            print(f"Found exactly one match for {language}")
            for query_language, query_label in result:
                programming_language_subjects[query_label.strip()] = query_language
        else:
            # There have been multiple results choose the one that matches the language exactly.
            print(f"Found multiple matches for {language}, trying to find the one that matches the description the closest.")
            found_match = False
            for query_language, query_label in result:
                print(query_language, query_label)
                # Do a simple match exactly by name and pick that one
                if query_label.strip() == language:
                    print(f"Found matching language {query_language} => {query_label}")
                    programming_language_subjects[query_label] = query_language
                    found_match = True
                    break

            if not found_match:
                print(f"No matching language was found for {language}, skipping...")    
    return programming_language_subjects

def get_programming_language_use_case_subjects(programming_language_subject):
    query = PROGRAMMING_LANGUAGE_USE_CASES_QUERY.replace("%programming_language_subject%", str(subject))
    result = g.query(query)
    use_case_subjects = {}
    for use_case, label in result:
        use_case_subjects[label.strip()] = use_case
    return use_case_subjects

def get_programming_language_paradigm_subjects(programming_language_subject):
    query = PROGRAMMING_LANGUAGE_PARADIGM_QUERY.replace("%programming_language_subject%", str(subject))
    result = g.query(query)
    paradigm_subjects = {}
    for paradigm, label in result:
        paradigm_subjects[label.strip()] = paradigm
    return paradigm_subjects

def get_programming_language_influenced_by_subjects(programming_language_subject):
    query = PROGRAMMING_LANGUAGE_INFLUENCED_BY_QUERY.replace("%programming_language_subject%", str(subject))
    result = g.query(query)
    influenced_by_subjects = {}
    for influenced_by, label in result:
        influenced_by_subjects[label.strip()] = influenced_by
    return influenced_by_subjects
    

if __name__ == "__main__":
    input_file = "./data/survey_results_public_cleaned.json"
    if not os.path.isfile(input_file):
        print(f"Expected file '{input_file}' was not found...")
        exit(1)

    with open(input_file, "r") as f:
        survey_results = json.load(f)

    # Extract languages which people have worked with.
    languages_people_have_worked_with = [
        entry["language"].strip() for entry in survey_results["languagesPeopleHaveWorkedWith"]]

    # Preprocess languages (e.g remove '/', character and split into two)
    preprocessed_languages_people_have_worked_with = []
    for language in languages_people_have_worked_with:
        preprocessed_languages_people_have_worked_with += language.split('/')

    g = create_graph()

    # Get actual programming language subjects
    # programming_language_subjects = get_programming_language_subjects(preprocessed_languages_people_have_worked_with)
    programming_language_subjects = get_programming_language_subjects(["Python"])
    print("Found the following subjects")
    for label, subject in programming_language_subjects.items():
        print(f"{label} => {subject}")

    # Query for detail information using the found subjects
    for programming_language_label, programming_language_subject in programming_language_subjects.items():
        
        # Use cases
        use_case_subjects = get_programming_language_use_case_subjects(programming_language_subject)
        print(f"Found the following use cases for language {programming_language_label}")
        for use_case_label, use_case_subject in use_case_subjects.items():
            print(f"{use_case_label} => {use_case_subject}")

        # Programming Paradigm
        paradigm_subjects = get_programming_language_paradigm_subjects(programming_language_subject)
        print(f"Found the following paradigms for language {programming_language_label}")
        for paradigm_label, paradigm_subject in paradigm_subjects.items():
            print(f"{paradigm_label} => {paradigm_subject}")

        # Influenced by
        influenced_by_subjects = get_programming_language_influenced_by_subjects(programming_language_subject)
        print(f"Found the following influences for language {programming_language_label}")
        for influenced_by_label, influenced_by_subject in influenced_by_subjects.items():
            print(f"{influenced_by_label} => {influenced_by_subject}")



