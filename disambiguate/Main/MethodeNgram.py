# Main pour la méthode n-gram

# Importations bibliothèques
from rdflib import Graph, Literal
from rdflib.namespace import OWL
from elasticsearch import Elasticsearch

# Importations fichiers
from GraphDB import SelectEntityFromGraphDB
from CandidateRanking import CandidateRankingNgram

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # suppresses "InsecureRequestWarning"

# Répertoires
repos_in = "http://localhost:7200/repositories/data"

# Main
if __name__ == '__main__':
    # Connexion à Elastic Search (serveur local, port 9200)
    es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200, 'scheme': "https"}],
                       basic_auth=('elastic', 'password'), verify_certs=False)  # enter password for default elastic user
    # Récupération des entités de GraphDB dans un dictionnaire organisé par paragraphe des IN
    dico_esn = SelectEntityFromGraphDB.getEntitiesFromGraphDB(repos_in)
    # Structure du dico :
    # dico = { 'n°§' : [[esn,uri], [esn,uri], ...] ; 'n°' : [[ , ], ...] ; ... }
    # Initialisation des 2 graphes de résultats
    Gs = Graph()  # Graphe qui contiendra tous les candidats de la sélection
    Gf = Graph()  # Graphe qui contiendra le meilleur candidat pour chaque esn
    # print(dico_esn.keys())
    # Bouclage pour parcourir tout le dico
    for p in dico_esn:
        # Boucle sur chaque paragraphe (p est le n° de paragraphe)
        for i in range(len(dico_esn[p])):  # Boucle parcourant toutes les esn de chaque paragraphe
            cla = []
            esn = dico_esn[p][i][0]  # recuperation du toponyme et de l'uri
            uri = dico_esn[p][i][1]  # de chaque esn du dico
            geog_feat = dico_esn[p][i][2]
            print("----------------------")
            print("Entité recherchée :", esn)
            print("Type:", geog_feat)
            for j in range(1):
                index = 'index_ngram'  # + str(j)  # boucle pour parcourir tous les index chargés sur ES contenant les
                print("Recherche dans l'index :", index)
                # données de ref
                # print(index)
                # ------ CHANGE HERE ------
                # result = CandidateRankingNgram.setCandidateResult(esn, index)  # renvoie les candidats trouvés pour 'esn' dans 'index' # ORIG
                result = CandidateRankingNgram.setCandidateResult(esn, geog_feat, index)  # renvoie les candidats trouvés pour 'esn' dans 'index' # HMR
                cla.append(result)
                print("Result:", result)
                for r in result:
                    if r[0] >= 10:
                        Gs.add((Literal(uri), OWL.sameAs, Literal(r[2])))  # ajout des triplets (uri esn, owl:sameAs, uri cleabs) dans le graphe selection
                    else:
                        Gs.add((Literal(uri), OWL.sameAs, Literal("nil")))
            cand = CandidateRankingNgram.ESRanking(cla)  # renvoie le meilleur candidat
            if cand[0] >= 10:
                print("Top candidate:", cand)
                # print("Top candidate score is greater or equal to 10:", cand[0])
                # this line (below) adds all top candidates to file
                Gf.add((Literal(uri), OWL.sameAs, Literal(cand[2])))  # ajout des triplets dans le graphe final
            else:
                print("Top candidate: [0, 'nil', 'nil']")
                # print("Top candidate is not good enough:", cand[0])
                Gf.add((Literal(uri), OWL.sameAs, Literal("nil")))  # ajout des triplets dans le graphe final
    # Enregistrement des 2 graphes au format ttl (puis chargés dans GraphDB)
    Gf.serialize(
        destination='/home/.../Ngram_top_candidates.ttl',
        format='turtle')
    Gs.serialize(
        destination='/home/.../Ngram_all_candidates.ttl',
        format='turtle')
