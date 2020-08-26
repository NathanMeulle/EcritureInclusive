################################################################################
################################################################################
######################### Projet Ecriture Inclusive ############################
################################################################################
################################################################################

#Copyright © 2020 Nathan. All rights reserved.
#@author Nathan
#name : EcritureInclusive


## Imports
from Dictionnaire import init_dico
import time ## Permet l'ajout d'un nombre au fichier enregistré
import os # pour afficher le répertoire courant où est enregistré le fichier

## INITIALISATION (MODIFIABLE)
GRAS =  True
SORTIE_TERMINAL = False # True : sortie sur le terminal, False : crée une fichier .txt
ENTREE_TERMINAL = False # True : saisie sur le terminal, False : ouvre le fichier .txt dans le meme repertoire


## Affichage - Style
class style:
    if GRAS and SORTIE_TERMINAL:
        BOLD = '\033[1m'
        END = '\033[0m'
    else :
        BOLD = ''
        END = ''

## Correction

def correction(text):
    load_dico()
    corriger_nom(text)

def corriger_nom(text):
    for k in range(len(text)):
        #Suppresion de la ponctuation pour recherche dans le dictionnaire
        PONCTU=False
        MAJ=False
        _=""
        if text[k].endswith(".") or text[k].endswith(","):
            _ = text[k][-1]
            text[k]=text[k][:-1]
            PONCTU=True
        if text[k]!=text[k].lower():
            MAJ=True
        mot,analyse = detect_pluriel(text[k])
        # print(mot)
        if any(mot.lower() in i for i in dico_nom):#Recherhce dans le dictionnaire
            res = obtenir_racine(list(filter(lambda x: mot.lower() in x, dico_nom))[0])
            # print(res)
            pluriel(res, analyse)
            if MAJ:
                text[k] = style.BOLD + str(res[0]).capitalize() + str(res[1]) + "·" + res[2] + _ + style.END
            else:
                text[k] = style.BOLD + str(res[0]) + str(res[1]) + "·" + res[2] + _ + style.END
            PONCTU=False
            corriger_determinant(text, k)
            corriger_adjectif(text, k)
        if PONCTU: text[k]+=_ #Rajout de la ponctuation

def corriger_determinant(text, k):
    MAJ=False
    if k!=0 and any(text[k-1].lower() in i for i in list(dico_determinant.values())):
        if text[k-1]!=text[k-1].lower():
            MAJ=True
        if MAJ:
            text[k-1] = style.BOLD + str([i for i,j in dico_determinant.items() if any(l==text[k-1].lower() for l in j)][0]).capitalize() + style.END
        else:
            text[k-1] = style.BOLD + str([i for i,j in dico_determinant.items() if any(l==text[k-1].lower() for l in j)][0]) + style.END

def corriger_adjectif(text, k):
    MAJ=False
    if k!=0 and any(text[k-1].lower() in i for i in list(dico_adjectif.values())):
        if text[k-1]!=text[k-1].lower():
            MAJ=True
        mot = str([i for i,j in dico_adjectif.items() if any(l==text[k-1].lower() for l in j)][0])
        if text[k-1][-1]!="s":
            if MAJ: text[k-1] = style.BOLD + mot.capitalize() + style.END
            else : text[k-1] = style.BOLD + mot + style.END
        else:
            mot+="·s"
            if MAJ: text[k-1] = style.BOLD + mot.capitalize() + style.END
            else : text[k-1] = style.BOLD + mot + style.END

    if k+1<len(text) and any(text[k+1] in i for i in list(dico_adjectif.values())):
        if text[k+1]!=text[k+1].lower():
            MAJ=True
        mot = str([i for i,j in dico_adjectif.items() if any(l==text[k+1] for l in j)][0])
        if text[k+1][-1]!="s": text[k+1] = style.BOLD + mot + style.END
        else: text[k+1] = style.BOLD + mot +"·s" + style.END


def obtenir_racine(liste_mots):
    racine = ""
    for k in range(min(len(liste_mots[0]), len(liste_mots[1]))):
        if(liste_mots[0][k]==liste_mots[1][k]):
            racine+=liste_mots[0][k]
        else:break
    mas = liste_mots[0][k+1:]
    fem = liste_mots[1][k+1:]

    if liste_mots[0].endswith("er"):
        mas="e"+mas
        fem="è"+fem
    if liste_mots[0].endswith("eur") and liste_mots[1].endswith("euse"):
            mas="r"+mas
            fem="euse"
    if liste_mots[0].endswith("eur") and liste_mots[1].endswith("rice"):
            mas="eur"
            fem="rice"
    if liste_mots[0].endswith("if"):
        mas="f"
        fem="ive"
    return [racine, mas, fem]

def detect_pluriel(mot):
    if mot[-1:]=="s" :

        if mot.endswith("ales"):
            return mot[:-2], "ales"

        if mot.endswith("efs") or mot.endswith("effes"):
            return mot[:-1], "efs"

        if mot.endswith("els") or mot.endswith("elles"):
            return mot[:-1], "els"

        if mot.endswith("ens") or mot.endswith("ennes"):
            return mot[:-1], "iens"

        if mot.endswith("ers") or mot.endswith("ères"):
            return mot[:-1], "ers"

        if mot.endswith("eurs") or mot.endswith("euses") or mot.endswith("rices"):
            return mot[:-1], "eurs"

        if mot.endswith("ifs") or mot.endswith("ives"):
            return mot[:-1], "ifs"

        if mot.endswith("ais") or mot.endswith("aises"):
            return mot, "ais"

        if mot.endswith("ons") or mot.endswith("onnes"):
            return mot[:-1], "ons"

        return mot[:-1], "s"

    if mot.endswith("aux"):
        return mot[:-3]+"al", "aux"

    return mot, ""

def pluriel(res, pluriel):
    if pluriel=="s":
            res[2] = "e·s"
            res[1] = ""

    if pluriel=="aux" or pluriel=="ales":
        res[0] = res[0][:-2]
        res[2] = "ales"
        res[1] = "aux"

    if pluriel=="efs":
        res[2] = "fe·s"
        res[1] = ""

    if pluriel=="iens":
        res[2] = "ne·s"
        res[1] = ""

    if pluriel=="ers":
        res[2] = "ère·s"
        res[1] = "er"

    if pluriel=="eurs" and res[1] == "r":
        res[2] = "euse·s"

    if pluriel=="eurs" and res[2] == "rice":
        res[2] = "rice·s"

    if pluriel=="ifs":
        res[2] += "·s"

    if pluriel=="ais":
        res[2] = "e·s"
        res[1] = ""
    if pluriel=="ons":
        res[2] = "ne·s"
        res[1] = ""


## Dictionnaire
def load_dico():
    global dico_nom
    global dico_determinant
    global dico_adjectif
    tmp = init_dico()
    dico_nom = tmp[0]
    dico_determinant = tmp[1]
    dico_adjectif = tmp[2]

## Affichage

if ENTREE_TERMINAL:
    text = str(input("Entrez votre texte :\n"))
else :
    try:
        with open(str(input("Entrez le nom du fichier (ex: mon_texte.txt) :\n")), "r") as fichier:
            text = fichier.read()
    except FileNotFoundError:
        text = "Une erreur est survenue, fichier non trouvé..."

text_list = text.split()
correction(text_list)

if SORTIE_TERMINAL:
    print("Texte suggéré : \n" + " ".join(text_list))
else :
    file = open("Suggestion_Ecriture_inclusive" + "_"+str(int(time.time()))+".txt", "w")
    file.write(" ".join(text_list))
    print("Votre fichier a été enregistré dans :" + os.getcwd())
    file.close()









