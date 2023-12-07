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
    LIMIT 10
"""
