# Programming Language Insights based on Stackoverflow Survey
A simple web application using `rdflib`, `owlready2` and the Stackoverflow Annual Developer Survey from 2023 to display useful information about Programming Languages and popular GitHub Repositories. 

## :computer: Scripts

|Script|Description|
|-------|-----|
|`clean_data.py`| Generats a JSON File from the Stackoverflow CSV File.|
|`knowledge_engineering_extraction.py`| Generates an Ontology based on JSON File (see Script `clean_data.py`).|
|`streamlit_app.py`| Starts a Streamlit App in order to explore the generated Ontology in a Dashboard.|

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

## :chart_with_upwards_trend: Streamlit
A simple Dashboard was created with Streamlit. In order to launch it simply execute the following command:

```bash
streamlit run app.py
```

## :clap: Used References

|Link|Description|
|-------|-----|
|[Stackoverflow Annual Developer Survey](https://insights.stackoverflow.com/survey)| Stackoverflow Annual Developer Survey Dataset|
|[GitHub REST API](https://docs.github.com/en/rest/search?apiVersion=2022-11-28)| Documentation about GitHub REST API|
|[GitHub REST API Rate Limits](https://docs.github.com/en/rest/rate-limit/rate-limit?apiVersion=2022-11-28)| Rate Limits on GitHub REST API|
|[Streamlit](https://streamlit.io/)| A very Framework to create simple Web Apps.|

