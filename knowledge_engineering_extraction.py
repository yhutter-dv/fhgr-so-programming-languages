import os
import json

from rdflib import Graph, Namespace, BNode, Literal
from owlready2 import get_ontology
from dotenv import dotenv_values
import requests

from sparql_queries import *

PRODUCTION_MODE = False

BASE_ONTOLOGY_FILE_PATH = "./data/base_ontology.rdf"
OUTPUT_ONTOLOGY_FILE_PATH = "./data/output_ontology.rdf"
DATA_FILE_PATH = "./data/survey_results_public_cleaned.json"
DOTENV_FILE_PATH = ".env-local" if not PRODUCTION_MODE else ".env"
SECRETS = dotenv_values(DOTENV_FILE_PATH)
GITHUB_SEARCH_API = "https://api.github.com/search"

def create_graph():
    g = Graph()

    # Define namespaces.
    # List of RDF Namespaces can be found here: https://www.mediawiki.org/wiki/Wikibase/Indexing/RDF_Dump_Format#Predicates
    namespaces = {
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
    query = PROGRAMMING_LANGUAGE_USE_CASES_QUERY.replace("%programming_language_subject%", str(programming_language_subject))
    result = g.query(query)
    use_case_subjects = {}
    for use_case, label in result:
        use_case_subjects[label.strip()] = use_case
    return use_case_subjects

def get_programming_language_paradigm_subjects(programming_language_subject):
    query = PROGRAMMING_LANGUAGE_PARADIGM_QUERY.replace("%programming_language_subject%", str(programming_language_subject))
    result = g.query(query)
    paradigm_subjects = {}
    for paradigm, label in result:
        paradigm_subjects[label.strip()] = paradigm
    return paradigm_subjects

def get_programming_language_influenced_by_subjects(programming_language_subject):
    query = PROGRAMMING_LANGUAGE_INFLUENCED_BY_QUERY.replace("%programming_language_subject%", str(programming_language_subject))
    result = g.query(query)
    influenced_by_subjects = {}
    for influenced_by, label in result:
        influenced_by_subjects[label.strip()] = influenced_by
    return influenced_by_subjects

def ensure_file(file_path):
    if not os.path.isfile(file_path):
        system.exit(f"Expected file '{file_path}' but was not found...")

def sanitize_programming_language_names(programming_languages):
    sanitized_names = []
    # Split up names which have a '/' character into two individual names.
    for language in programming_languages:
        sanitized_names += language.split('/')
    return sanitized_names

def get_most_popular_repos_for_programming_language(programming_language, number_of_results = 10):
    # Get most popular repositories for the given programming language
    query_string = f"language:{programming_language}&sort=stars&order=desc&per_page={number_of_results}&page=1"
    url = f"{GITHUB_SEARCH_API}/repositories?q={query_string}"
    headers = {
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": SECRETS["GITHUB_API_TOKEN"],
    }
    response = requests.get(url, headers=headers)
    status_code = response.status_code
    # Check for none sucessful status and return empty list if something went wrong...
    if not status_code == 200:
        print(f"Received none successful status code {status_code} for language {programming_language}. Empty list will be returned")
        return []
    response_json = response.json()
    repos = []
    for item in response_json["items"]:
        repo = {
            "url": item["html_url"],
            "name": item["full_name"],
            "number_of_stars": item["stargazers_count"],
            "description": item["description"]
        }
        repos.append(repo)
    return repos

def add_programming_languages_to_onto(onto, g, programming_languages, create_onto_programming_language_instance_func):
    with onto:
        programming_language_subjects = get_programming_language_subjects(programming_languages)
        
        print("Found the following subjects")
        for label, subject in programming_language_subjects.items():
            print(f"{label} => {subject}")

        # Query for detail information using the found subjects
        for programming_language_label, programming_language_subject in programming_language_subjects.items():
            # Depending on the programming languages (can be the ones people are already working with or want to work with) we need to create another type of instance (e.g onto.ProgrammingLanguagePeopleHaveWorkedWith or onto.ProgrammingLanguagePeopleWantToWorkWith).
            # We delegate this task to the appropriate function which is passed in as an argument.
            programming_language = create_onto_programming_language_instance_func(programming_language_label)
            programming_language.wikiDataUrl = [str(programming_language_subject)]

            # Use cases
            use_case_subjects = get_programming_language_use_case_subjects(programming_language_subject)
            use_cases = []
            print(f"Found the following use cases for language {programming_language_label}")
            for use_case_label, use_case_subject in use_case_subjects.items():
                print(f"{use_case_label} => {use_case_subject}")
                use_case = onto.ProgrammingLanguageUseCase(use_case_label, wikiDataUrl=[str(use_case_subject)])
                use_cases.append(use_case)
            programming_language.useCase = use_cases

            # Programming Paradigm
            paradigm_subjects = get_programming_language_paradigm_subjects(programming_language_subject)
            paradigms = []
            print(f"Found the following paradigms for language {programming_language_label}")
            for paradigm_label, paradigm_subject in paradigm_subjects.items():
                print(f"{paradigm_label} => {paradigm_subject}")
                paradigm = onto.ProgrammingLanguageParadigm(paradigm_label, wikiDataUrl=[str(paradigm_subject)])
                paradigms.append(paradigm)
            programming_language.paradigm = paradigms

            # Influenced by
            influenced_by_subjects = get_programming_language_influenced_by_subjects(programming_language_subject)
            influences = []
            print(f"Found the following influences for language {programming_language_label}")
            for influenced_by_label, influenced_by_subject in influenced_by_subjects.items():
                print(f"{influenced_by_label} => {influenced_by_subject}")
                influence = onto.ProgrammingLanguageInfluencedBy(influenced_by_label, wikiDataUrl=[str(influenced_by_subject)])
                influences.append(influence)
            programming_language.influencedBy = influences

            # Popular GitHub Repos
            repos = get_most_popular_repos_for_programming_language(programming_language_label)
            popular_repos = []

            # Note that repos is just a list of Python Dicitonaries, we need to instantiate conrete instances...
            for repo in repos:
                popular_repo = onto.ProgrammingLanguagePopularRepo()
                popular_repo.repoDescription = [repo["description"]]
                popular_repo.repoNumberOfStars = [repo["number_of_stars"]]
                popular_repo.repoUrl = [repo["url"]]
                popular_repo.repoName = [repo["name"]]

                popular_repos.append(popular_repo)

            programming_language.popularRepo = popular_repos

    return onto

if __name__ == "__main__":
    ensure_file(DATA_FILE_PATH)
    ensure_file(BASE_ONTOLOGY_FILE_PATH)

    # Load cleaned data file
    with open(DATA_FILE_PATH, "r") as f:
        survey_results = json.load(f)

    # Extract languages.
    languages_people_have_worked_with = [entry["language"].strip() for entry in survey_results["languagesPeopleHaveWorkedWith"]]
    languages_people_want_to_work_with = [entry["language"].strip() for entry in survey_results["languagesPeopleWantToWorkWith"]]

    # Sanitize languages
    languages_people_have_worked_with = sanitize_programming_language_names(languages_people_have_worked_with)
    languages_people_want_to_work_with = sanitize_programming_language_names(languages_people_want_to_work_with)

    # Load ontologie
    onto = get_ontology(f"file://{BASE_ONTOLOGY_FILE_PATH}").load()

    # Create graph used for SPARQL Queries...
    g = create_graph()

    onto = add_programming_languages_to_onto(onto, g, languages_people_have_worked_with, lambda label: onto.ProgrammingLanguagePeopleHaveWorkedWith(label))
    onto = add_programming_languages_to_onto(onto, g, languages_people_want_to_work_with, lambda label: onto.ProgrammingLanguagePeopleWantToWorkWith(label))

    # Save ontology
    onto.save(file=OUTPUT_ONTOLOGY_FILE_PATH)









