# %programming_language% functions as a template and will be dynamically replaced
PROGRAMMING_LANGUAGE_QUERY = """
    SELECT DISTINCT ?programming_language ?programming_language_label WHERE {
        SERVICE <https://query.wikidata.org/sparql> {
          ?programming_language wdt:P31 ?instance_type;
                                rdfs:label ?programming_language_label.

          # instance of computer language
          # The * goes up the inheritance hierarchy until it finds a match
          ?instance_type wdt:P279* wd:Q629206.

          # For example CSS is called Cascading Style Sheets in english and CSS in german etc.
          # Therefore we check both languages while also ignoring casing
          FILTER((LANG(?programming_language_label) = "en" || LANG(?programming_language_label) = "de") && REGEX(str(?programming_language_label), "%programming_language%", "i"))
        }
    }
    LIMIT 1000
"""

PROGRAMMING_LANGUAGE_USE_CASES_QUERY = """
   SELECT DISTINCT ?use_case ?use_case_label WHERE {
        SERVICE <https://query.wikidata.org/sparql> {

          <%programming_language_subject%> wdt:P366 ?use_case.
          ?use_case rdfs:label ?use_case_label.
  
          FILTER(LANG(?use_case_label) = "en")
        }
    }
    LIMIT 10 
"""

PROGRAMMING_LANGUAGE_PARADIGM_QUERY = """
   SELECT DISTINCT ?paradigm ?paradigm_label WHERE {
        SERVICE <https://query.wikidata.org/sparql> {

          <%programming_language_subject%> wdt:P3966 ?paradigm.
          ?paradigm rdfs:label ?paradigm_label.
  
          FILTER(LANG(?paradigm_label) = "en")
        }
    }
    LIMIT 20
"""

PROGRAMMING_LANGUAGE_INFLUENCED_BY_QUERY = """
   SELECT DISTINCT ?influenced_by ?influenced_by_label WHERE {
        SERVICE <https://query.wikidata.org/sparql> {

          <%programming_language_subject%> wdt:P737 ?influenced_by.
          ?influenced_by rdfs:label ?influenced_by_label.
  
          FILTER(LANG(?influenced_by_label) = "en")
        }
    }
    LIMIT 20
"""
