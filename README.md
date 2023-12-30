# Programming Language Insights based on Stackoverflow Survey
A simple web application using `rdflib`, `owlready2` and the Stackoverflow Annual Developer Survey from 2023 to display useful information about Programming Languages and popular GitHub Repositories. 

## :computer: Scripts

|Script|Description|
|-------|-----|
|`clean_data.py`| Generats a JSON File from the Stackoverflow CSV File.|
|`knowledge_engineering_extraction.py`| Generates an Ontology based on JSON File (see Script `clean_data.py`).|
|`app.py`| A simple Frontend written with Flask.|

## :rocket: Setup

### GitHub PAT Token
In order for the Script `knowledge_engineering_extraction.py` to work a valid GitHub PAT Token is required. This is needed because this Script fetches the most popular Repositories for each Programming Language via the GitHub REST API. You can generate a PAT (Personal Access Token) [here](https://github.com/settings/tokens).

> Note that you do NOT have to give any permission, just leave everything blank.

Once you have your token you can enter it into the `.env` file.

### Python
```bash
python -m venv ./venv
source ./venv/bin/activate.sh
pip install -r requirements.txt
```

### Documentation
Make sure pandoc and the necessary latex packages are installed:
```bash
sudo pacman -S pandoc texlive
```

## :books: Documentation
As a base template the awesome pandoc-latex-template from [Wandmalfarbe](https://github.com/Wandmalfarbe/pandoc-latex-template) was used. In order to generate the Documentation simply the `doc.sh` file executable and run it:

```bash
cd doc
chmod +x doc.sh
./doc.sh
```

## Frontend
The Frontend is build with the awesome [Deno Fresh Framework](https://fresh.deno.dev/). Therefore in order for things to work please make sure you have [Deno](https://docs.deno.com/runtime/manual/getting_started/installation) installed.

After that to start up the frontend simply run:

```bash
cd frontend
deno task start
```

## Backend
For the Frontend a simple Backend was implemented with [FastAPI](https://fastapi.tiangolo.com/).

To start the backend simply run the following commands:

```bash
cd backend
python -m venv ./venv
source venv/bin/activate.sh
uvicorn app:app --port 6969 --reload
```

## :clap: Used References

|Link|Description|
|-------|-----|
|[Stackoverflow Annual Developer Survey](https://insights.stackoverflow.com/survey)| Stackoverflow Annual Developer Survey Dataset|
|[GitHub REST API](https://docs.github.com/en/rest/search?apiVersion=2022-11-28)| Documentation about GitHub REST API|
|[GitHub REST API Rate Limits](https://docs.github.com/en/rest/rate-limit/rate-limit?apiVersion=2022-11-28)| Rate Limits on GitHub REST API|

