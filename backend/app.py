from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from owlready2 import get_ontology
import os
import sys
from request_models import *

def create_app():
    app = FastAPI()

    # Allow CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

def filter_out_fusion_class(elements):
	return [element for element in elements if not "fusionclass" in element.name]

def ensure_file(file_path):
    if not os.path.isfile(file_path):
        sys.exit(f"Expected file '{file_path}' but was not found...")

def load_ontology():
	ensure_file(ONTOLOGY_FILE_PATH)
	return get_ontology(f"file://{ONTOLOGY_FILE_PATH}").load()

def create_programming_language_from_onto_element(element):
	language = {
		"name": element.name,
		"useCases": get_use_cases_for_language(element),
		"influences": get_influences_for_language(element),
		"paradigms": get_paradigms_for_language(element),
		"url": element.wikiDataUrl[0],
	}
	return language

def get_programming_languages_people_are_working_with():
	languages = []
	with ONTOLOGY:
		for element in filter_out_fusion_class(ONTOLOGY.ProgrammingLanguagePeopleHaveWorkedWith.instances()):
			language = create_programming_language_from_onto_element(element)
			languages.append(language)
	return languages

def get_programming_languages_people_want_to_work_with():
	languages = []
	with ONTOLOGY:
		for element in filter_out_fusion_class(ONTOLOGY.ProgrammingLanguagePeopleWantToWorkWith.instances()):
			language = create_programming_language_from_onto_element(element)
			languages.append(language)
	return languages

def get_use_cases_for_language(language):
	use_cases = []
	for element in language.useCase:
		use_case = {
			"name": element.name,
			"url": element.wikiDataUrl[0]
		}
		use_cases.append(use_case)
	return use_cases

def get_influences_for_language(language):
	influences = []
	for element in filter_out_fusion_class(language.influencedBy):
		influence = {
			"name": element.name,
			"url": element.wikiDataUrl[0]
		}
		influences.append(influence)
	return influences

def get_paradigms_for_language(language):
	paradigms = []
	for element in filter_out_fusion_class(language.paradigm):
		paradigm = {
			"name": element.name,
			"url": element.wikiDataUrl[0]
		}
		paradigms.append(paradigm)
	return paradigms

def get_git_repos_for_language_name(language_name):
	git_repos = []
	with ONTOLOGY:
		for element in filter_out_fusion_class(ONTOLOGY.ComputerLanguage.instances()):
			print(element)
			if element.name == language_name:
				for repo in element.popularRepo:
					repo_entry = {
						"name": repo.repoName[0],
						"numberOfStars": repo.repoNumberOfStars[0],
						"description": repo.repoDescription[0],
						"url": repo.repoUrl[0]
					}
					git_repos.append(repo_entry)
				break
	return git_repos

ONTOLOGY_FILE_PATH = "./data/output_ontology.rdf"
ONTOLOGY = load_ontology()
PROGRAMMING_LANGUAGES_PEOPLE_WANT_TO_WORK_WITH = get_programming_languages_people_want_to_work_with()
app = create_app()


@app.get("/languages_people_want_to_work_with")
async def languages_people_want_to_work_with():
	return PROGRAMMING_LANGUAGES_PEOPLE_WANT_TO_WORK_WITH

@app.post("/git_repos/")
async def git_repos(request: GitRepoRequest):
	print(request.language)
	return get_git_repos_for_language_name(request.language)