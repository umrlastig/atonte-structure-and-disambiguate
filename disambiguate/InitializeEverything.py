from elasticsearch import Elasticsearch

from CreateIndex import CreateAndPopulateIndex

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # suppresses "InsecureRequestWarning"

if __name__ == '__main__':
    # On crée une instance elasticsearch
    es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200, 'scheme': "https"}],
                       basic_auth=('elastic', 'password'), verify_certs=False)  # enter password for default elastic user

    # Récupération du fichier contenant tous les toponymes de la base (IGN)
    file = "/home/.../toustoponymespoints.geojson"

    # Création et population du nouvel index sur es avec le fichier toustoponymes (cf. CreateAndPopulateIndex.py)
    CreateAndPopulateIndex.create_and_populate_index(es, file, 'index_toponymes')
