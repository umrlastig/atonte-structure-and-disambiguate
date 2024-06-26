from Mesure import Mesures
from GraphDB import SelectEntityFromGraphDB

rep = "http://localhost:7200/repositories/data"
dico = SelectEntityFromGraphDB.getResultFromGraphDB(rep)
# gold = SelectResultatFromGraphDB.getGoldFromGraphDB(rep)
print(dico)
# print(gold)

# card = Mesure.CardM(dico)
# print(card)
# cardel = Mesure.CardElt(dico)
# print(cardel)
# print(len(dico))
# rapcand = Mesure.RapCand(dico,dico)
# print(rapcand)
# preccand = Mesure.PrecCand(dico,dico)
# print(preccand)
