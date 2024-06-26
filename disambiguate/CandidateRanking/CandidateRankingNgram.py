# Récupération et classement de candidats par la méthode n-gram

# Importations bibliothèques
from elasticsearch import Elasticsearch

# Importations fichiers
from ES import SearchParamBuilder

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # suppresses "InsecureRequestWarning"

# Connexion à ES
es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200, 'scheme': "https"}],
                   basic_auth=('elastic', 'password'), verify_certs=False)  # enter password for default elastic user


# Fonction pour récupérer le cleabs
def getCleabsTopo(u):
    cleabs = u['_source']['properties']['cleabs']
    return cleabs


def getToponymeTopo(u):
    bdt_toponyme = u['_source']['properties']['toponyme']
    return bdt_toponyme


def getNatureTopo(u):
    bdt_nature = u['_source']['properties']['nature']
    return bdt_nature


# Fonction pour récupérer l'uri
def getURITopo(u):
    uri = '<http://data.ign.fr/id/topo/' + getCleabsTopo(u) + '>'
    return uri


# Fonction pour récupérer le score de similarité dans ES
def getScoreTopo(u):
    score = u['_score']
    return score


# Fonction pour trouver des candidats avec ES
# ------ CHANGE HERE ------
# def getCandidateFromES(esn, index_ngram):  # ORIG
def getCandidateFromES(esn, geog_feat, index_ngram):  # HMR
    # ------ CHANGE HERE ------
    # params = SearchParamBuilder.candidate_selection_ngram(esn)  # ORIG
    params = SearchParamBuilder.candidate_selection_ngram_toponyme_type_80_boost(esn, geog_feat)  # HMR v1
    res = es.search(index=index_ngram, body=params)
    res_hit = res['hits']['hits']
    if res_hit == []:
        return 'nil'
    else:
        return res_hit


# Fonction pour renvoyer les candidats trouvés par ES
# ------ CHANGE HERE ------
# def setCandidateResult(esn, index_ngram): # ORIG
def setCandidateResult(esn, geog_feat, index_ngram):  # HMR
    result = []
    # ------ CHANGE HERE ------
    # res_hit = getCandidateFromES(esn, index_ngram) # ORIG
    res_hit = getCandidateFromES(esn, geog_feat, index_ngram)  # HMR
    if res_hit == 'nil':
        return [[0, 'nil', 'nil']]
    else:
        # RES_autres = getOtherCandidates(esn, p, dico_esn)
        for u in res_hit:
            cleabs_toponyme = getCleabsTopo(u)
            uri_toponyme = getURITopo(u)
            score = getScoreTopo(u)
            bdt_toponyme = getToponymeTopo(u)
            # GEOM = getGeomCandidat(u)
            # score = DistScore(GEOM, RES_autres)
            print("Here's a match:", [score, cleabs_toponyme, uri_toponyme])
            result.append([score, cleabs_toponyme, uri_toponyme])
        result_sort = sorted(result, reverse=True)
        return result_sort


# Fonction pour renvoyer le meilleur candidat trouvé par ES
def ESRanking(result_sort):
    return result_sort[0][0]
