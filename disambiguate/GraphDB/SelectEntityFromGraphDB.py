# Chargement des données enregistrées dans GraphDB.

# Documentation utilisée : rdflib ("https://rdflib.readthedocs.io/en/stable/")

# Importation des bibliothèques
import socket
import urllib

from SPARQLWrapper import SPARQLWrapper, N3
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, OWL
import urllib.request

# Préfixes
ENT = Namespace("http://data.shom.fr/id/spatialentity/")
ATLN = Namespace("http://data.shom.fr/def/atlantis#")
DBP = Namespace("http://dbpedia.org/ontology/")


# Fonction pour requêter en sparql dans le graph de GraphDB
def querygraph(query, repos):  # reqête en sparql, repertoire de requete
    # timeout in seconds
    timeout = 60
    socket.setdefaulttimeout(timeout)

    # Gestion du proxy
    proxy = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(proxy)
    urllib.request.install_opener(opener)

    sparql = SPARQLWrapper(repos)
    sparql.setQuery(query)
    sparql.setReturnFormat(N3)
    results = sparql.query().convert()
    g = Graph()
    g.parse(data=results, format="n3")
    return g


# Sélection des entités dans le repertoire de GraphDB
def getEntitiesFromGraphDB(repos):  # repository dans graphdb
    # creation du graphe avec les esn
    gESN = querygraph("""
        CONSTRUCT {?s ?p ?o.}
        FROM <http://data.shom.fr/id/spatialentity/test/>
        WHERE {?s ?p ?o.}""",
                      repos)  # requete sparql pour construire un graph depuis l'iri du graph de graphdb (ici gold_dev)
    # print("Length of gESN graph:",len(gESN))
    # print(gESN.serialize(format="turtle"))  # print all the triples in the repo
    sub = gESN.subjects(RDF.type, ATLN.SpatialEntity)  # recuperation des sujets des triplets rdf
    dico_esn = dict()  # creation d'un dictionnaire qui contiendra les topo des esn par paragraphe
    # print("dico_esn:", dico_esn)
    # remplissage du dictionnaire de toponyme par paragraphe des IN
    for entity in gESN.subjects(RDF.type, ATLN.SpatialEntity):
        toponyme = gESN.value(entity, RDFS.label, None)  # toponyme de chaque esn
        geog_feat_uri = gESN.value(entity, ATLN.hasTypeOfSpatialEntity, None)  # geogFeat de chaque esn
        geog_feat = str(geog_feat_uri).replace('http://data.shom.fr/id/codes/atln/typeofspatialentity/', '')
        print(f"Entity {entity} has toponym '{toponyme}' and type '{geog_feat}'.")
        if len(toponyme) > 1:
            uri = f"{entity}"  # uri de chaque esn
            for pn in gESN.objects(entity, ATLN.hasSource):
                paraNumber = f"{pn}"  # numero de paragraphe de chaque esn
                if paraNumber not in dico_esn:
                    dico_esn[paraNumber] = []  # creation du positionnement de chaque esn par paragraphe dans le dico
                dico_esn[paraNumber].append(
                    [toponyme, uri, geog_feat])  # ajout des toponymes dans le dico dans la position qui correspond au paragraphe
                # print("paragraph no:", paraNumber)
        else:
            continue
    return dico_esn


# Structure du dico : { 'n°§' : [ [topo, uri], [topo, uri], ... ] , 'n°§' : [ [topo, uri] , ... ] }



#####################################################################
# Sélection des résultats depuis le graph de GraphDB
def getResultFromGraphDB(repos):  # repository de graphdb
    # creation du graphe avec les esn
    # all candidates
    gESN = querygraph("""
             CONSTRUCT {
               ?s owl:sameAs ?o .
             }
             FROM <http://data.shom.fr/id/spatialentity/desambig_all/>
             WHERE { ?s owl:sameAs ?o. }
             """, repos)
    # Construction graph depuis celui de graphdb
    triple = gESN.triples((None, OWL.sameAs, None))  # recuperation triplets rdf
    dico = dict()  # initialisation dictionnaire qui contiendra les 2 uri
    # Boucle pour parcourir les triplets
    # for s, p, o in gESN.triples((None, OWL.sameAs, None)):
    for s, p, o in triple:
        # print(f"{s} same as {o}")
        uri = f"{s}"  # uri de l'esn
        if uri not in dico:
            dico[uri] = []
            obj = gESN.objects(s, OWL.sameAs)
            for u in obj:  # uri de la donnée ign
                dico[uri].append(u)
    return dico


# Structure du dico : { 'uri de l'esn' : [liste des uri ign des candidats] }

# Sélection du gold depuis GraphDB (même méthode)
def getGoldFromGraphDB(repos):  # repository de graphdb
    # creation du graphe avec les esn
    gESN = querygraph("""
         CONSTRUCT {
              ?s owl:sameAs ?o .
         }  
         FROM <http://data.shom.fr/id/spatialentity/desambig_gold/>
         WHERE { ?s owl:sameAs ?o. } 
         """, repos)
    triple = gESN.triples((None, OWL.sameAs, None))
    dico = dict()
    for s, p, o in triple:
        uri = "{}".format(s)
        if uri not in dico:
            dico[uri] = []
            obj = gESN.objects(s, OWL.sameAs)
            for u in obj:
                dico[uri].append(u)
    return dico

    # Sélection du gold depuis GraphDB (même méthode)


def getAutoFromGraphDB(repos):  # repository de graphdb
    # creation du graphe avec les esn
    # top candidates only
    gESN = querygraph("""
         CONSTRUCT {
              ?s owl:sameAs ?o .
         }  
         FROM <http://data.shom.fr/id/spatialentity/desambig_selected/>
         WHERE { ?s owl:sameAs ?o. }
         """, repos)
    triple = gESN.triples((None, OWL.sameAs, None))
    dico = dict()
    for s, p, o in triple:
        uri = "{}".format(s)
        if uri not in dico:
            dico[uri] = []
            obj = gESN.objects(s, OWL.sameAs)
            for u in obj:
                dico[uri].append(u)
    return dico
