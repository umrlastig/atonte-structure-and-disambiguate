# Peuplement d'un index en appliquant le découpage n-gram

# Docs : https://www.elastic.co/guide/en/elasticsearch/reference/7.9/analysis-edgengram-tokenizer.html

# Importation des bibliothèques
import geojson
from elasticsearch import helpers
from elasticsearch import Elasticsearch

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # suppresses "InsecureRequestWarning"


# Fonction qui crée et peuple l'index (cf. CreateAndPopulateIndex.py)
def create_and_populate_index(es_instance, toponyms_to_index, index_name):
    # On charge le fichier geojson avec tous les toponymes
    with open(toponyms_to_index, encoding="utf-8") as geojson_file:
        toponyms = geojson.load(geojson_file)
        # print(toponyms)
        # On vide l'index
        es_instance.options(ignore_status=[400, 404]).indices.delete(index=index_name)
        # es_instance.indices.delete(index=index_name, ignore=[400, 404])  # this is now depreciated
        # On crée un index = une bdd elacticsearch pour stocker le dictionnaire.
        # Un document = une feature = un toponyme.
        k = [{
            "_index": index_name,
            "_source": feature,  # this corresponds to the info associated to each record
            "_doc_type": "toponyme",
            "_body": mapping,
        } for feature in geojson_to_es(toponyms)]
        # On charge les features une par une dans l'index
        helpers.bulk(es_instance, k)


# Fonction qui extrait les features du geojson une par une
def geojson_to_es(geojson):
    for feature in geojson['features']:
        # print(feature.get("properties").get("toponyme"))
        yield feature


# mapping avec le tokenizer de peuplement (autocomplete) et le tokenizer de recherche (autocomplete_search)
mapping = {
    "settings": {
        "analysis": {
            "analyzer": {
                "autocomplete": {  # this is a definition of a custom ANALYZER called 'autocomplete'
                    "tokenizer": "autocomplete",  # this is a custom tokenizer: defined below
                    "filter": [
                        "lowercase"
                    ]
                },
                "autocomplete_search": {  # this is a definition of custom ANALYZER called 'autocomplete'
                    "tokenizer": "autocomplete"
                }
            },
            "tokenizer": {
                "autocomplete": {  # this is definition of custom TOKENIZER called 'autocomplete'
                    "type": "edge_ngram",
                    "min_gram": 2,
                    "max_gram": 10,
                    "token_chars": [
                        "letter",
                        "digit",
                        "whitespace"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "id": {
                "type": "integer"
            },
            "cleabs": {
                "type": "text"
            },
            "gazetier": {
                "type": "text"
            },
            "tablesource": {
                "type": "text"
            },
            "nature": {
                "type": "text"
            },
            "naturedetaillee": {
                "type": "text"
            },
            "toponyme": {
                "type": "text",
                "analyzer": "autocomplete",  # indicates analyser to use for indexing
                "search_analyzer": "autocomplete_search"  # indicates analyser to use for searching
            },
            "geometry": {
                "type": "geo_shape"
            },
        }
    }
}

if __name__ == '__main__':
    # Connexion à ES
    es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200, 'scheme': "https"}],
                       basic_auth=('elastic', 'password'), verify_certs=False)  # enter password for default elastic user
    # Creation des index
    file = "/home/.../toustoponymespoints.geojson"  # chemin du fichier contenant les données de l'index
    # print(file)
    index = 'index_ngram'
    print("Creating index:",index)
    create_and_populate_index(es, file, index)
    print("Index created:",index)
    