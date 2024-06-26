from GraphDB import SelectEntityFromGraphDB

import csv

# Chargement des fichiers pour le gold et les données à mesurer
from Mesure import MesureEnter

rep = "http://localhost:7200/repositories/data"

dico_desamb = SelectEntityFromGraphDB.getResultFromGraphDB(rep)  # contains all candidate results
auto = SelectEntityFromGraphDB.getAutoFromGraphDB(rep)  # contains top candidates only
gold = SelectEntityFromGraphDB.getGoldFromGraphDB(rep)  # contains gold candidates

#print("dico_desamb:", dico_desamb)
print("len(dico_desamb):", len(dico_desamb))
#print("auto:", auto)
print("len(auto):", len(auto))
#print("gold:", gold)
print("len(gold):", len(gold))

print("----------------")

# Calcul des mesures
print("------- CardM -------")
CardM = MesureEnter.CardM(dico_desamb)
print("CardM = " + str(CardM))

print("------- PrecCand -------")
PrecCand = MesureEnter.PrecCand(gold, dico_desamb)
print("PrecCand = " + str(PrecCand))

print("------- RapCand -------")
RapCand = MesureEnter.RapCand(gold, dico_desamb)
print("RapCand = " + str(RapCand))

print("------- RapN -------")
RapN = MesureEnter.RapN(gold, dico_desamb)
print("RapNil = " + str(RapN))

print("------- PrecN -------")
PrecN = MesureEnter.PrecN(gold, dico_desamb)
print("PrecNil = " + str(PrecN))

print("------- ExactD -------")
ExactD = MesureEnter.ExactitudeD(gold, auto, dico_desamb)
print("ExactD = " + str(ExactD))

print("------- ExactG -------")
ExactG = MesureEnter.ExactitudeG(gold, auto)
print("ExactG = " + str(ExactG))

print("------- ExactN -------")
ExactN = MesureEnter.ExactitudeN(gold, auto)
print("ExactN = " + str(ExactN))

print("-----------------------")
print("------- RESULTS -------")

print("CardM = " + str(CardM))
print("PrecCand = " + str(PrecCand))
print("RapCand = " + str(RapCand))
print("RapNil = " + str(RapN))
print("PrecNil = " + str(PrecN))
print("ExactD = " + str(ExactD))
print("ExactG = " + str(ExactG))
print("ExactN = " + str(ExactN))
