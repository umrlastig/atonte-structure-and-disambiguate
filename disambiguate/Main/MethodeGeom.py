# Main pour la méthode de la proximité géographique

# Importations bibliothèques
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import OWL
from elasticsearch import Elasticsearch

# Importations fichiers
from GraphDB import SelectEntityFromGraphDB
from CandidateRanking import CandidateRankingGeom

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # suppresses "InsecureRequestWarning"

# Préfixes
ENT = Namespace("http://data.shom.fr/id/spatialentity/")
ATLN = Namespace("http://data.shom.fr/def/atlantis#")

# Répertoires
repos_in = "http://localhost:7200/repositories/data"

# Main
if __name__ == '__main__':
    # Connexion à Elastic Search (serveur local, port 9200)
    es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200, 'scheme': "https"}],
                       basic_auth=('elastic', 'password'), verify_certs=False)  # enter password for default elastic user
    # Récupération des entités de GraphDB dans un dictionnaire organisé par paragraphe des IN
    dico_esn = SelectEntityFromGraphDB.getEntitiesFromGraphDB(repos_in)
    Gs = Graph()  # graphe contenant les triplets de la selection
    Gc = Graph()  # graphe contenant les triplets du classement
    for p in dico_esn:
        for i in range(len(dico_esn[p])):
            esn = dico_esn[p][i][0]  # recuperation du toponyme et de l'uri
            uri = dico_esn[p][i][1]  # de chaque esn du dico
            geog_feat = dico_esn[p][i][2]
            print("----------------------")
            print("Entité recherchée :", esn)
            print("Type:", geog_feat)
            index = 'index_toponymes'
            print("Recherche dans l'index :", index)
            # for i in range(1, 12):
            #     index = 'index_maritime' + str(
            #         i)  # boucle pour parcourir tous les index chargés sur ES contenant les données de ref
            # print(index)
            # ------ CHANGE HERE ------
            # result = CandidateRankingGeom.setCandidateResult(esn, index, p, dico_esn)  # candidats renvoyes par ES
            result = CandidateRankingGeom.setCandidateResult(esn, geog_feat, index, p, dico_esn)  # candidats renvoyes par ES
            print("Result:", result)
            for r in result:
                if 10 <= r[0] < 100000:
                    # print("Match score:", r[0], "add to file")
                    Gs.add((Literal(uri), OWL.sameAs, Literal(
                        r[2])))  # ajout des triplets (uri esn, owl:sameAs, uri cleabs) dans le graphe selection
                else:
                    # print("Match score:", r[0], "don't add to file")
                    Gs.add((Literal(uri), OWL.sameAs, Literal("nil")))
            cand = CandidateRankingGeom.ESRanking(result)  # renvoie le meilleur candidat
            if 10 <= cand[0] < 100000:
                print("Top candidate:", cand)
                # print("Top candidate score is greater or equal to 10:", cand[0])
                # this line (below) adds all top candidates to file
                Gc.add((Literal(uri), OWL.sameAs, Literal(cand[2])))  # ajout des triplets dans le graphe final
            else:
                print("Top candidate: [0, 'nil', 'nil']")
                # print("Top candidate is not good enough:", cand[0])
                Gc.add((Literal(uri), OWL.sameAs, Literal("nil")))  # ajout des triplets dans le graphe final
    #print(Gc)
    Gc.serialize(destination='/home/.../Geom_top_candidates.ttl',
                 format='turtle')
    #print(Gs)
    Gs.serialize(destination='/home/.../Geom_all_candidates.ttl',
                 format='turtle')
