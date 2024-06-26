# Evaluation de la sélection
# Cardinalité moyenne
# Exprime la capacité du prgr à fournir des candidats pour l'étape de classement à suivre.
def CardM(dico):
    cardM = CardElt(dico) / len(dico)
    return cardM


def CardElt(dico):
    card = 0
    for c in dico:
        card = card + len(dico[c])
    return card

    # Rappel des candidats


# Exprime la proportion de candidats non vides et contenant la bonne référence dans l'étape de sélection sur
# l'ensemble des mentions pour lesquelles il existe une référence dans la bdd
def RapCand(Dgold, Dcode):
    rapp = VraiPositifGlobal(Dgold, Dcode) / len(Dgold)
    return rapp


def VraiPositifGlobal(dg, dc):  # dg = {"esn" : "uri"} et dc = {"esn" : [liste uri]}
    comp = 0
    for i in dg:
        if i in dc:
            for c in dc[i]:
                if c == dg[i]:
                    comp = comp + VraiPositifEntite(dg, dc)
    return comp


def VraiPositifEntite(dg, dc):
    comp = 0
    for c in dc:
        if dg[c] and "nil" not in dc[c]:
            comp = comp + 1
    return comp

    # Précision des candidats


# Proportion des candidats non vides correct sur total de candidats non vides
def PrecCand(Dg, Dc):
    prec = VraiPositifGlobal(Dg, Dc) / CardElt(Dc)
    return prec

    # Rappel des références nulles (NIL)


# Proportion candidats vides sur nombre total de mentions pour lesquelles il n'existe pas de référence dans la bdd
def RapN(Dg, Dc):
    if nil_gold(Dg) == 0:
        return 0
    PrecN = VraiNilGlobal(Dg, Dc) / nil_gold(Dg)
    return PrecN


def nil_gold(Dg):
    n = 0
    for i in Dg:
        if Dg[i] == "nil":
            n = n + 1
    return n


def VraiNilGlobal(Dg, Dc):
    n = 0
    for i in Dg:
        if i in Dc:
            if Dg[i] == "nil" and "nil" in Dc[i]:
                n = n + 1
    return n
