from flask import Flask, render_template, redirect, url_for
from owlready2 import get_ontology

import os

def ensure_file(file_path):
    if not os.path.isfile(file_path):
        system.exit(f"Expected file '{file_path}' but was not found...")

def load_ontology():
	file_path = "./static/data/output_ontology.rdf"
	ensure_file(file_path)
	return get_ontology(f"file://{file_path}").load()

# Global variables
ONTOLOGY = load_ontology()

app = Flask(__name__)

def get_use_cases_for_language(language):
	use_cases = []
	for element in language.useCase:
		use_case = {
			"name": element.name,
			"url": element.wikiDataUrl[0]
		}
		use_cases.append(use_case)
	return use_cases

def get_programming_languages_people_are_working_with():
	languages = []
	with ONTOLOGY:
		for element in ONTOLOGY.ProgrammingLanguagePeopleHaveWorkedWith.instances():
			# TODO: Check why we get this weird 'fusionclass...'
			if element.name.startswith("fusion"):
				continue
			language = {
				"name": element.name,
				"use_cases": get_use_cases_for_language(element),
				"url": element.wikiDataUrl[0]
			}
			languages.append(language)
	return languages

def get_programming_languages_people_want_to_work_with():
	languages = []
	with ONTOLOGY:
		for element in ONTOLOGY.ProgrammingLanguagePeopleWantToWorkWith.instances():
			# TODO: Check why we get this weird 'fusionclass...'
			if element.name.startswith("fusion"):
				continue

			language = {
				"name": element.name,
				"use_cases": get_use_cases_for_language(element),
				"url": element.wikiDataUrl[0]
			}
			languages.append(language)
	return languages


@app.route("/")
def index():
	# Per Default we show the programming languages people are working with
	programming_languages = get_programming_languages_people_are_working_with()
	return render_template("index.html", programming_languages = programming_languages)

@app.route("/languages_people_want_to_work_with")
def languages_people_want_to_work_with():
	programming_languages = get_programming_languages_people_want_to_work_with()
	return render_template("index.html", languages_people_want_to_work_with = True, programming_languages = programming_languages)
