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

def get_use_cases_for_from_onto_element(language):
	use_cases = []
	for element in language.useCase:
		use_case = {
			"name": element.name,
			"url": element.wikiDataUrl[0]
		}
		use_cases.append(use_case)
	return use_cases

def get_popular_repos_from_onto_element(language):
	popular_repos = []
	print(f"Getting repos from {language}")
	for element in language.popularRepo:
		print(f"Got repo {element}")
		repo = {
			"name": element.repoName[0],
			"number_of_stars": element.repoNumberOfStars[0],
			"description": element.repoDescription[0],
			"url": element.repoUrl[0]
		}
		popular_repos.append(repo)
	return popular_repos

def get_programming_languages_people_are_working_with():
	languages = []
	with ONTOLOGY:
		for element in ONTOLOGY.ProgrammingLanguagePeopleHaveWorkedWith.instances():
			# TODO: Check why we get this weird 'fusionclass...'
			if element.name.startswith("fusion"):
				continue
			language = create_programming_language_from_onto_element(element)
			languages.append(language)
	return languages

def get_programming_languages_people_want_to_work_with():
	languages = []
	with ONTOLOGY:
		for element in ONTOLOGY.ProgrammingLanguagePeopleWantToWorkWith.instances():
			# TODO: Check why we get this weird 'fusionclass...'
			if element.name.startswith("fusion"):
				continue

			language = create_programming_language_from_onto_element(element)
			languages.append(language)
	return languages

def create_programming_language_from_onto_element(element):
	language = {
		"name": element.name,
		"use_cases": get_use_cases_for_from_onto_element(element),
		"url": element.wikiDataUrl[0],
		"popularRepos": get_popular_repos_from_onto_element(element)
	}
	return language

def get_programming_language_by_name(name):
	language = None
	with ONTOLOGY:
		for element in ONTOLOGY.ComputerLanguage.instances():
			print(element)
			if element.name == name:
				language = create_programming_language_from_onto_element(element)
				break
	return language



@app.route("/")
def index():
	# Per Default we show the programming languages people are working with
	programming_languages = get_programming_languages_people_are_working_with()
	return render_template("index.html", programming_languages = programming_languages)

@app.route("/details/<programming_language_name>")
def details(programming_language_name = None):
	programming_language = get_programming_language_by_name(programming_language_name)
	return render_template("detail.html", programming_language = programming_language)

@app.route("/languages_people_want_to_work_with")
def languages_people_want_to_work_with():
	programming_languages = get_programming_languages_people_want_to_work_with()
	return render_template("index.html", languages_people_want_to_work_with = True, programming_languages = programming_languages)
