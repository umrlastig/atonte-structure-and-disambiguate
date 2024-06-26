# Main pour la méthode de levenshtein

# Importations bibliothèques
from rdflib import Graph, Namespace, Literal
from rdflib.namespace import OWL
from elasticsearch import Elasticsearch

# Importations fichiers
from GraphDB import SelectEntityFromGraphDB
from CandidateRanking import CandidateRanking3

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # suppresses "InsecureRequestWarning"

# Préfixes
ENT = Namespace("http://data.shom.fr/id/spatialentity/")
ATLN = Namespace("http://data.shom.fr/def/atlantis#")

# Répertoires GraphDB
repos_in = "http://localhost:7200/repositories/data"

# Main
if __name__ == '__main__':
    # Connexion à Elastic Search (serveur local, port 9200)
    es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200, 'scheme': "https"}],
                       basic_auth=('elastic', 'password'), verify_certs=False)  # enter password for default elastic user
    # Récupération des entités de GraphDB dans un dictionnaire organisé par paragraphe des IN
    dico_esn = SelectEntityFromGraphDB.getEntitiesFromGraphDB(repos_in)
    Gs = Graph()  # graphe contenant les triplets de la selection ALL CANDIDATES
    Gc = Graph()  # graphe contenant les triplets du classement TOP CANDIDATE
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
            # ------ CHANGE HERE ------
            # result = CandidateRanking3.setCandidateResult(esn, index)  # candidats renvoyes par ES # ORIG
            result = CandidateRanking3.setCandidateResult(esn, geog_feat, index)  # candidats renvoyes par ES # HMR
            print("Result:", result)
            # result is a list of all the match lists (a list of lists, one match is a list of score, cleabs and uri)
            for r in result:
                if r[0] >= 10:
                    # print("Match score:", r[0], "add to file")
                    Gs.add((Literal(uri), OWL.sameAs, Literal(
                        r[2])))  # ajout des triplets (uri esn, owl:sameAs, uri cleabs) dans le graphe selection
                else:
                    # print("Match score:", r[0], "don't add to file")
                    Gs.add((Literal(uri), OWL.sameAs, Literal("nil")))
            cand = CandidateRanking3.ESRanking(result)  # renvoie le meilleur candidat
            if cand[0] >= 10:
                print("Top candidate:", cand)
                # print("Top candidate score is greater or equal to 10:", cand[0])
                # this line (below) adds all top candidates to file
                Gc.add((Literal(uri), OWL.sameAs, Literal(cand[2])))  # ajout des triplets dans le graphe final
            else:
                print("Top candidate: [0, 'nil', 'nil']")
                # print("Top candidate is not good enough:", cand[0])
                Gc.add((Literal(uri), OWL.sameAs, Literal("nil")))  # ajout des triplets dans le graphe final
    # print(Gc)
    Gc.serialize(destination='/home/.../Lev_top_candidates.ttl', format='turtle')
    # print(Gs)
    Gs.serialize(destination='/home/.../Lev_all_candidates.ttl', format='turtle')
