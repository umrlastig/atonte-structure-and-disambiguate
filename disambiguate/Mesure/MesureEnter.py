# Evaluation de la sélection
# Cardinalité moyenne
# Exprime la capacité du prgr à fournir des candidats pour l'étape de classement à suivre.
def CardM(dico):
    nb_esn = len(dico)
    print("Number of entities:", nb_esn)
    card = 0
    for c in dico:  # c is one entity like http://data.shom.fr/id/instructionsnautiques/esn/1
        card = card + len(dico[c])
    print("Total number of candidates:", card)
    cardM = card / nb_esn
    return cardM


# Exprime la proportion de candidats non vides et contenant la bonne référence dans l'étape de sélection sur
# l'ensemble des mentions pour lesquelles il existe une référence dans la bdd
# number of entities for which candidates have been found AND for which correct candidate is present in the selection
# divided by number of entities for which a reference exists
def RapCand(Dgold, Dcode):
    # rapp = VraiPositifGlobal(Dgold, Dcode)/len(Dgold)
    print("Number of entities for which candidates have been found AND for which correct candidate is present in the "
          "selection:", EnsembleCandidatsDontLeBon(Dgold, Dcode))
    print("Number of entities for which a gold reference exists:", LengthDicoNonNIL(Dgold))
    rapp = EnsembleCandidatsDontLeBon(Dgold, Dcode) / LengthDicoNonNIL(Dgold)
    return rapp


def EnsembleCandidatsDontLeBon(dg, dc):
    comp = 0
    for entity in dc:
        candidats = dc[entity]
        if len(candidats) == 1 and "nil" in str(candidats[0]):
            continue
        else:
            if entity in dg:
                vraispositifs = dg[entity]
                if not set(vraispositifs).isdisjoint(candidats):
                    comp = comp + 1
                else:
                    continue
    # print ("EnsembleCandidatsDontLeBon = "+str(comp))
    return comp


def LengthDicoNonNIL(dico):
    comp = 0
    for entity in dico:
        if "nil" in str(dico[entity]):
            continue
        else:
            comp = comp + 1
    # print("LengthDicoNonNIL = "+str(comp))
    return comp


def LengthDicoNIL(dico):
    comp = 0
    for entity in dico:
        if "nil" in str(dico[entity]):
            comp = comp + 1
        else:
            continue
    # print("LengthDicoNIL = "+str(comp))
    return comp


def EnsemblesNILVrais(dg, dc):
    comp = 0
    for entity in dc:
        candidats = dc[entity]
        if len(candidats) == 1 and "nil" in str(candidats[0]):
            if entity in dg:
                vraispositifs = dg[entity]
                if not set(vraispositifs).isdisjoint(candidats):
                    comp = comp + 1
                else:
                    continue
        else:
            continue
    # print ("EnsemblesNILVrais = "+str(comp))
    return comp


# Proportion des candidats non vides correct sur total de candidats non vides
def PrecCand(Dgold, Dcode):
    # prec = VraiPositifGlobal(Dg,Dc)/CardM(Dc)
    print("Number of entities for which candidates have been found AND for which correct candidate is present in the "
          "selection:", EnsembleCandidatsDontLeBon(Dgold, Dcode))
    print("Number of entities for which candidates have been found:", LengthDicoNonNIL(Dcode))
    prec = EnsembleCandidatsDontLeBon(Dgold, Dcode) / LengthDicoNonNIL(Dcode)
    return prec

    # Rappel des références nulles (NIL)


# Proportion candidats vides sur nombre total de mentions pour lesquelles il n'existe pas de référence dans la bdd
def RapN(Dg, Dc):
    # if nil_gold(Dg) == 0:
    #    return 0
    # PrecN = VraiNilGlobal(Dg,Dc)/nil_gold(Dg)
    print("Number of entities for which zero candidates have been found AND for which no gold reference exists:",
          EnsemblesNILVrais(Dg, Dc))
    print("Number of entities for which no gold reference exists:", LengthDicoNIL(Dg))
    RapN = EnsemblesNILVrais(Dg, Dc) / LengthDicoNIL(Dg)
    return RapN


# Proportion de "bon" candidats vides sur nombre total de "nil" renvoyés
def PrecN(Dg, Dc):
    # if nil_gold(Dg) == 0:
    #    return 0
    # prec = VraiNilGlobal(Dg,Dc)/nil_gold(Dc)
    print("Number of entities for which zero candidates have been found AND for which no gold reference exists:",
          EnsemblesNILVrais(Dg, Dc))
    print("Number of entities for which zero candidates have been found:", LengthDicoNIL(Dc))
    prec = EnsemblesNILVrais(Dg, Dc) / LengthDicoNIL(Dc)
    return prec


def EnsembleBonsResultats(Dg, Da): # ORIG I think it's wrong
    comp = 0
    for entity in Da:
        resultats = Da[entity]
        verite = Dg[entity]
        if not set(resultats).isdisjoint(verite) and "rdflib.term.Literal('nil')" not in verite:
            comp = comp + 1
        else:
            continue
    return comp


def EnsembleBonsResultatsSansNIL(Dg, Da):
    comp = 0
    for entity in Da:
        resultats = Da[entity]
        verite = Dg[entity]
        if not set(resultats).isdisjoint(verite):
            if "nil" not in str(verite):
                comp = comp + 1
            else:
                continue
    return comp


def EnsembleBonsResultatsInclNIL(Dg, Da):
    comp = 0
    for entity in Da:
        resultats = Da[entity]
        verite = Dg[entity]
        if not set(resultats).isdisjoint(verite):
            comp = comp + 1
        else:
            continue
    return comp


def ExactitudeD(Dg, Da, Dc):
    print("Number of entities for which for which correct candidate is not nil AND for which correct candidate has "
          "been selected as top candidate:", EnsembleBonsResultatsSansNIL(Dg, Da))
    print("Number of entities for which candidates have been found AND for which correct candidate is present in the "
          "selection:", EnsembleCandidatsDontLeBon(Dg, Dc))
    exact = EnsembleBonsResultatsSansNIL(Dg, Da) / EnsembleCandidatsDontLeBon(Dg, Dc)
    return exact


def ExactitudeG(Dg, Da):
    print("Number of entities for which for which correct candidate is not nil AND for which correct candidate has "
          "been selected as top candidate:", EnsembleBonsResultatsSansNIL(Dg, Da))
    print("Number of entities for which a gold reference (not nil) exists:", LengthDicoNonNIL(Dg))
    exact = EnsembleBonsResultatsSansNIL(Dg, Da) / LengthDicoNonNIL(Dg)
    return exact


def ExactitudeN(Dg, Da):
    print("Number of entities for which correct candidate (incl. nil) has been selected as top candidate:",
          EnsembleBonsResultatsInclNIL(Dg, Da))
    print("Number of entities in gold:", len(Dg))
    exact = EnsembleBonsResultatsInclNIL(Dg, Da) / len(Dg)
    return exact
