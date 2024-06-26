# Récupération de candidats avec ES avec méthode de levenshtein et classement par proximité géographique

# Importations bibliothèques
import numpy as np
from elasticsearch import Elasticsearch

# Importations fichiers
from ES import SearchParamBuilder
from CandidateRanking import CandidateRanking3

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # suppresses "InsecureRequestWarning"

# Connexion à ES
es = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200, 'scheme': "https"}],
                       basic_auth=('elastic', 'password'), verify_certs=False)  # enter password for default elastic user


# Fonction pour récupérer le cleabs d'un toponyme
def getCleabsTopo(u):
    cleabs = u['_source']['properties']['cleabs']
    return cleabs


# Fonction pour récupérer l'uri d'un toponyme
def getURITopo(u):
    uri = '<http://data.ign.fr/id/topo/' + getCleabsTopo(u) + '>'
    return uri


# Fonction qui calcule le centroide
def getGeomCandidat(u):
    # print("getGeomCandidat u['_source']['geometry']['type']:", u['_source']['geometry']['type'])
    if u['_source']['geometry']['type'] == 'MultiPolygon':
        g = u['_source']['geometry']['coordinates']
        geo = g[0][0]
        l_geo = len(geo)
        x_coord = [p[0] for p in geo]
        y_coord = [p[1] for p in geo]
        x_centroid = sum(x_coord) / l_geo
        y_centroid = sum(y_coord) / l_geo
    if u['_source']['geometry']['type'] == 'Point':
        g = u['_source']['geometry']['coordinates']
        # print("getGeomCandidat g:", g)
        x_centroid = g[0]
        y_centroid = g[1]
    else:
        x_centroid = 0
        y_centroid = 0
    GEOM = [x_centroid, y_centroid]
    # print("getGeomCandidat GEOM:", GEOM)
    return GEOM


# Fonction pour calculer la distance entre l'esn et les autres esn du même paragraphe
def DistScore(geo, L_autres):
    GEO_AUTRES = []
    m = []
    # print("DistScore L_autres:", L_autres)
    for res in L_autres:
        # print("DistScore res:", res)
        # if res == 'nil':
            # print("DistScore nil")
            # return 0
        if res != 'nil':
        # else:
            for u in res:
                # print("DistScore u:", u)
                geo_autre = getGeomCandidat(u)
                # print("DistScore geo_autre:", geo_autre)  # this is GEOM
                GEO_AUTRES.append(geo_autre)
                # print("DistScore GEO_AUTRES:", GEO_AUTRES)
    for g in GEO_AUTRES:
        # print("DistScore g[0]:", g[0])
        # print("DistScore geo[0]:", geo[0])
        # print("DistScore g[1]:", g[1])
        # print("DistScore geo[1]:", geo[1])
        distance = np.sqrt((g[0] - geo[0]) ** 2 + (g[1] - geo[1]) ** 2)
        # print("DistScore distance:", distance)
        m.append(distance)
    return np.median(m)


# Fonction pour trouver des candidats avec ES
# ------ CHANGE HERE ------
# def getCandidateFromES(esn, index_topo): # ORIG
def getCandidateFromES(esn, geog_feat, index_topo): # HMR
    params = SearchParamBuilder.candidate_selection_toponyme_type(esn, geog_feat)
    res = es.search(index=index_topo, body=params)
    res_hit = res['hits']['hits']
    if res_hit == []:
        return 'nil'
    else:
        return res_hit


# Fonction pour renvoyer les candidats trouvés par ES
# ------ CHANGE HERE ------
# def setCandidateResult(esn, index_topo, numpara, dico_esn): # ORIG
def setCandidateResult(esn, geog_feat, index_topo, numpara, dico_esn): # HMR
    result = []
    # ------ CHANGE HERE ------
    # res_hit = getCandidateFromES(esn, index_topo)  # liste des candidats renvoyés par ES # ORIG
    res_hit = getCandidateFromES(esn, geog_feat, index_topo)  # liste des candidats renvoyés par ES # HMR
    RES_AUTRES = getOtherCandidates(esn, geog_feat, numpara, dico_esn)
    # print("setCandidateResult res_hit:", res_hit)
    # print("setCandidateResult RES_AUTRES:", RES_AUTRES)
    if res_hit == 'nil':
        return [[0, 'nil', 'nil']]
    if RES_AUTRES == []:
        return CandidateRanking3.setCandidateResult(esn, geog_feat, index_topo)
    else:
        for u in res_hit:
            cleabs_toponyme = getCleabsTopo(u)
            uri_toponyme = getURITopo(u)
            GEOM = getGeomCandidat(u)
            score = DistScore(GEOM, RES_AUTRES)
            print("Here's a match:", [score, cleabs_toponyme, uri_toponyme])
            result.append([score, cleabs_toponyme, uri_toponyme])
        result_sort = sorted(result)
        # print("setCandidateResult result_sort:", result_sort)
        return result_sort


# Fonction qui récupère tous les candidats des autres esn dans le même paragraphe que l'esn à traiter
def getOtherCandidates(esn, geog_feat, numpara, dico_esn):
    L_autres = []
    for i in range(len(dico_esn[numpara])):
        if dico_esn[numpara][i][0] != esn:
            esn_autre = dico_esn[numpara][i][0]
            index = 'index_toponymes'
            res_hit = getCandidateFromES(esn_autre, geog_feat, index)
            # print("getOtherCandidates res_hit:", res_hit)
            if res_hit != 'nil':  # added this so that RES_AUTRES == [] if no candidates found
                L_autres.append(res_hit)
    return L_autres


# Renvoie l'uri du meilleur candidat extrait par ES avec l'uri de l'esn a desambiguiser
def ESRanking(result_sort):
    if len(result_sort) == 0:
        return [0, 'nil', 'nil']
    else:
        return result_sort[0]
