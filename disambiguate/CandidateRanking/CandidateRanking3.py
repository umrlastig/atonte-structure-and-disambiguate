# Récupération et classement de candidats avec ES avec méthode de levenshtein

# Importations bibliothèques
from elasticsearch import Elasticsearch
from collections import namedtuple

Matching = namedtuple('Matching', ['score', 'cleabs_toponyme', 'uri_toponyme'])

# Importations fichiers
from ES import SearchParamBuilder

# Connexion au serveur d'ES
es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200, 'scheme': "https"}],
                   basic_auth=('elastic', 'password'), verify_certs=False)  # enter password for default elastic user


# Fonction pour récupérer le cleabs du toponyme dans la réponse ES
def getCleabsTopo(u):
    cleabs = u['_source']['properties']['cleabs']
    return cleabs


# Fonction pour récupérer l'uri du toponyme dans la réponse ES
def getURITopo(u):
    uri = '<http://data.ign.fr/id/topo/' + getCleabsTopo(u) + '>'
    return uri


# Fonction pour récupérer le score de similarité dans ES
def getScoreTopo(u):
    score = u['_score']
    return score


# Fonction pour trouver des candidats avec ES
# ------ CHANGE HERE ------
# def getCandidateFromES(esn, index_topo): # ORIG
def getCandidateFromES(esn, geog_feat, index_topo): # HMR
    # ------ CHANGE HERE ------
    # params = SearchParamBuilder.candidate_selection_match_fuzzy(esn)  # méthode Levenshtein d'ES ajouter _fuzzy # ORIG
    params = SearchParamBuilder.candidate_selection_toponyme_type(esn, geog_feat)  # HMR v1 and v2
    # params = SearchParamBuilder.candidate_selection_toponyme_type_80_boost(esn, geog_feat)  # HMR v3+
    res = es.search(index=index_topo, body=params)  # requête d'ES
    res_hit = res['hits']['hits']  # liste des résultats d'ES
    if res_hit == []:
        return 'nil'  # renvoie 'nil' si ES n'a pas trouvé de candidats
    else:
        return res_hit  # renvoie la liste des candidats


# Fonction pour renvoyer les candidats trouvés par ES
# ------ CHANGE HERE ------
# def setCandidateResult(esn, index_topo): # ORIG
def setCandidateResult(esn, geog_feat, index_topo): # HMR
    result = []
    # ------ CHANGE HERE ------
    # res_hit = getCandidateFromES(esn, index_topo)  # liste des candidats renvoyés par ES # ORIG
    res_hit = getCandidateFromES(esn, geog_feat, index_topo)  # liste des candidats renvoyés par ES # HMR
    if res_hit == 'nil':
        return [[0, 'nil', 'nil']]  # si aucun candidat, renvoie la liste score nulle, cleabs 'nil' et uri 'nil'
    else:
        for u in res_hit:
            cleabs_toponyme = getCleabsTopo(u)  # récupération du cleabs
            uri_toponyme = getURITopo(u)  # récupération de l'uri
            score = getScoreTopo(u)  # récupération du score
            mat = Matching(score, cleabs_toponyme, uri_toponyme)
            print("Here's a match:", mat)
            result.append(mat)  # stockage dans une liste de la forme : [[score,cleabs,uri],...]
        result_sort = sorted(result, key=lambda x: getattr(x, 'score'),
                             reverse=True)  # tri de la liste par score décroissant (meilleur candidat en 1er)
        return result_sort


# Fonction pour renvoyer le meilleur candidat trouvé par ES
def ESRanking(result_sort):
    return result_sort[0]
