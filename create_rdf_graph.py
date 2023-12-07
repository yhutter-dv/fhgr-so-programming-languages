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
        "dpo": Namespace("https://dbpedia.org/")
    }

    # Bind all namespaces so that they do not need to be defined via PREFIX in queries...
    for name, ns in namespaces.items():
        g.bind(name, ns)

    return g

if __name__ == "__main__":
    input_file = "./data/survey_results_public_cleaned.json"
    if not os.path.isfile(input_file):
        print(f"Expected file '{input_file}' was not found...")
        exit(1)

    with open(input_file, "r") as f:
        survey_results = json.load(f)

    programming_languages_people_have_worked_with = [
        entry["language"] for entry in survey_results["languagesPeopleHaveWorkedWith"]]

    g = create_graph()

    programming_language_subjects = []
    for language in programming_languages_people_have_worked_with[:1]:
        query = PROGRAMMING_LANGUAGE_QUERY.replace("%programming_language%", language.lower())
        result = g.query(query)
        number_of_results = len(result)
        if number_of_results == 0:
            print(f"No result found for {language}, skipping...")
            continue
        elif number_of_results == 1:
            print(f"Found exactly one match for {language}")
            programming_language_subjects.append(result[0])
        else:
            # There have been multiple results try finding the result with the name that matches the closest.
            # TODO: Try to find the one that matchest the closest.
            print(f"Found multiple matches for {language}, trying to find the one that matches the description the closest.")
            for query_language, query_label in result:
                print(query_language, query_label)
            
       
