# coding: utf-8
# Importations des bibliothèques
import geojson
from elasticsearch import helpers
from elasticsearch import Elasticsearch


# Fonction qui crée et peuple l'index d'ES (paramètres : connexion ES, fichier de l'index, nom de l'index)
def create_and_populate_index(es_instance, toponyms_to_index, index_name):
    # On charge le fichier geojson avec tous les toponymes
    with open(toponyms_to_index, encoding="utf-8") as geojson_file:
        toponyms = geojson.load(geojson_file)
        # On vide l'index
        es_instance.options(ignore_status=[400, 404]).indices.delete(index=index_name)
        # es_instance.indices.delete(index=index_name, ignore=[400, 404])  # this is now depreciated
        # On crée un index = une bdd elacticsearch pour stocker le dictionnaire
        # Un document = une feature = un toponyme
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
    for feature in geojson['features']:  # 'features' is from the geojson file
        # one 'feature' is one record in the db
        # each one contains contains "type", "properties" and "geometry" fields
        # "properties" contains "nature", "toponyme", etc. fields
        # print(feature.get("properties").get("toponyme"))
        yield feature


# le mapping qui sert à dire à Elasticsearch quels sont les attributs dans les données et leurs types respectifs
mapping = {
    "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 1,
        "max_result_window": 1000
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
                "analyzer": "standard",
                "type": "text"
            },
            "geometry": {
                "type": "geo_shape"
            },
        }
    }
}

# Non utilisé si on lance InitializeEverything
if __name__ == '__main__':
    # Connexion à ES
    es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200, 'scheme': "https"}],
                       basic_auth=('elastic', 'password'), verify_certs=False)  # enter password for default elastic user
    # Creation des index
    file = "/home/.../toustoponymespoints.geojson"  # chemin du fichier contenant les données de l'index
    create_and_populate_index(es, file, 'index_toponymes')
