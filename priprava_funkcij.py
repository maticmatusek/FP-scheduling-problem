from cgi import test
from cgitb import text
from gettext import find
import random
from turtle import color
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, solve
from itertools import count, permutations 
import math
import copy
from pyomo.environ import * 
from pyomo.opt import SolverFactory
import os

def naredi_trikotnik(dolzina=None,spodnja_meja=1,zgornja_meja=10,celostevilski=True):
    """ 
    Naredi trikotnik:
    * Sprejme : dolžino, spodnjo/zgornjo mejo, celoštevilskost
    * Naključen položaj noge
    * Vrstni red je 0
    Vrne : trikotnik
    """
    if dolzina == None and celostevilski:
        dolzina = random.randint(spodnja_meja,zgornja_meja)
    if dolzina == None and celostevilski == False :
        dolzina = random.uniform(spodnja_meja,zgornja_meja)
    a_x = lambda x: x
    b_x = lambda x: x
    c_x = lambda x: x + dolzina
    a_y = lambda y: 0
    b_y = lambda y: dolzina
    c_y = lambda y: dolzina
    trikotnik = dict()
    trikotnik["a"] = (a_x,a_y)
    trikotnik["b"] = (b_x,b_y)
    trikotnik["c"] = (c_x,c_y)
    trikotnik["dolzina"] = dolzina
    trikotnik["polozaj_noge"] = random.randint(spodnja_meja,zgornja_meja)
    trikotnik["vrstni_red"] = 0
    return trikotnik

def narisi_trikotnik(trikotnik):
    """
    Nariše trikotnik
    """
    x = trikotnik["polozaj_noge"]
    x_a_do_b = np.array([trikotnik["a"][0](x), trikotnik["b"][0](x)])
    x_a_do_c = np.array([trikotnik["a"][0](x), trikotnik["c"][0](x)])
    x_b_do_c = np.array([trikotnik["b"][0](x), trikotnik["c"][0](x)])
    y_a_do_b = np.array([trikotnik["a"][1](x), trikotnik["b"][1](x)])
    y_a_do_c = np.array([trikotnik["a"][1](x), trikotnik["c"][1](x)])
    y_b_do_c = np.array([trikotnik["b"][1](x), trikotnik["c"][1](x)])
    ab_stranica = plt.plot(x_a_do_b,y_a_do_b,"k")
    ac_stranica = plt.plot(x_a_do_c, y_a_do_c,"k")
    bc_stranica = plt.plot(x_b_do_c, y_b_do_c,"k")
    return ab_stranica, bc_stranica, ac_stranica

def naredi_trikotnike(stevilo_trikotnikov, dolzine = None,spodnja_meja=1,zgornja_meja=10,celostevilski=True):
    """
    * Naredi n trikotnikov (PAZI stevilo_trikotnikov mora biti enako kot dolzina seznama)
    * vrstni red doloci glede na številko trikotnika 
    * vrne slovar trikotnikov brez specifično določenih vrstnih redov in položaj nog
    """
    slovar = dict()
    if dolzine == None:
        for i in range(stevilo_trikotnikov):
            slovar[i] = naredi_trikotnik(dolzine,spodnja_meja,zgornja_meja,celostevilski)
    else: 
        if stevilo_trikotnikov != len(dolzine):
            raise "Število trikotnikov se ne ujema s številom podanih dolžin"
        if stevilo_trikotnikov == len(dolzine):
            for i in range(stevilo_trikotnikov):
                slovar[i]= (naredi_trikotnik(dolzine[i],spodnja_meja,zgornja_meja,celostevilski))
    for i in range(len(slovar)):
        slovar[i]["vrstni_red"] = i
    return slovar

def narisi_trikotnike(trikotniki):
    """
    sprejme slovar trikotnikov in jih izriše
    """
    konec = []
    dolzina = []
    dolzina_urnik = dolzina_urnika(trikotniki)
    for i in range(len(trikotniki)):
        narisi_trikotnik(trikotniki[i])
        konec.append(trikotniki[i]["dolzina"] + trikotniki[i]["polozaj_noge"])
        dolzina.append(trikotniki[i]["dolzina"] )
    dolzina_x = np.array([0, max(konec)])
    dolzina_y = np.array([0,0])
    plt.plot(dolzina_x,dolzina_y,"r:^")
    plt.plot(np.array([0,0]),np.array([0,max(dolzina)]),"r:")
    plt.plot(np.array([max(konec),max(konec)]),np.array([0,max(dolzina)]),"r:")
    plt.text(x=max(konec)/2,y=max(dolzina)+3,s=f"Dolžina urnika: {dolzina_urnik}",color="r")
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    return plt.show()

def dolzina_urnika(trikotniki):
    """
    Sprejme slovar trikotnikov in izračuna max(polozaj_noge + dolzina)
    """
    dolzine = []
    for i in range(len(trikotniki)):
        dolzine.append(trikotniki[i]["polozaj_noge"]+trikotniki[i]["dolzina"])
    return max(dolzine)

    
def razvrsti_v_seznam_glede_na_vrstni_red(trikotniki):
    """
    * Pomožna funkcija sprejme seznam trikotnikov in jih razvrsti v seznam po vrsti glede na vrstni_red
    * Vrne 2 seznama in sicer 1) seznam trikotnikov 2) seznam imen trikotnikov
    * Funkcija se uporabi v: iz_slovarja_doloci_polozaj_noge_nazaj_v_slovar(trikotniki)
    """
    seznam = [None] * len(trikotniki)
    seznam_imen = [None] * len(trikotniki)
    for i in range(len(trikotniki)):
        seznam[trikotniki[i]["vrstni_red"]] = trikotniki[i]
        seznam_imen[trikotniki[i]["vrstni_red"]] = i
    return seznam , seznam_imen

def doloci_polozaj_noge_glede_na_vrstni_red(urejeni_trikotniki_v_seznamu):
    """
    * Pomožna funkcija
    * spremeni zgolj položaj_noge
    * sprejme seznam urejenih trikotnikov in določi položaj noge glede na vrstni red
    * Funkcija se uporabi v: iz_slovarja_doloci_polozaj_noge_nazaj_v_slovar(trikotniki)
    """
    urejeni_trikotniki_v_seznamu[0]["polozaj_noge"] = 0
    for i in range(1,len(urejeni_trikotniki_v_seznamu)):
        if urejeni_trikotniki_v_seznamu[i-1]["dolzina"] >= urejeni_trikotniki_v_seznamu[i]["dolzina"]:
            urejeni_trikotniki_v_seznamu[i]["polozaj_noge"] = urejeni_trikotniki_v_seznamu[i-1]["polozaj_noge"] + urejeni_trikotniki_v_seznamu[i]["dolzina"]
        else:
            urejeni_trikotniki_v_seznamu[i]["polozaj_noge"] = urejeni_trikotniki_v_seznamu[i-1]["polozaj_noge"] + urejeni_trikotniki_v_seznamu[i-1]["dolzina"]
            seznam = [None] * i
            for j in range(i):
                if urejeni_trikotniki_v_seznamu[j]["polozaj_noge"] + urejeni_trikotniki_v_seznamu[j]["dolzina"] < urejeni_trikotniki_v_seznamu[i]["polozaj_noge"]:
                    seznam[j] = 0
                elif urejeni_trikotniki_v_seznamu[j]["dolzina"] > urejeni_trikotniki_v_seznamu[i]["dolzina"]:
                    seznam[j] =  urejeni_trikotniki_v_seznamu[j]["dolzina"] -( (urejeni_trikotniki_v_seznamu[j]["dolzina"]) - (urejeni_trikotniki_v_seznamu[i]["dolzina"])  ) - (urejeni_trikotniki_v_seznamu[i]["polozaj_noge"] - urejeni_trikotniki_v_seznamu[j]["polozaj_noge"] )
                elif urejeni_trikotniki_v_seznamu[j]["dolzina"] <= urejeni_trikotniki_v_seznamu[i]["dolzina"]:
                    seznam[j] = urejeni_trikotniki_v_seznamu[i]["dolzina"] - ( urejeni_trikotniki_v_seznamu[i]["dolzina"] - urejeni_trikotniki_v_seznamu[j]["dolzina"] ) - (urejeni_trikotniki_v_seznamu[i]["polozaj_noge"] - urejeni_trikotniki_v_seznamu[j]["polozaj_noge"] )
            index = seznam.index(max(seznam))
            urejeni_trikotniki_v_seznamu[i]["polozaj_noge"] = urejeni_trikotniki_v_seznamu[i]["polozaj_noge"] + seznam[index]
    return urejeni_trikotniki_v_seznamu

def iz_seznama_v_slovar(seznam, seznam_imen):
    """
    * Pomožna funkcija
    * Sprejme seznam trikotnikov in seznam imen potem pa zapise trikotnike nazaj v slovar
    * Funkcija se uporabi v: iz_slovarja_doloci_polozaj_noge_nazaj_v_slovar(trikotniki)
    """
    trikotniki = dict()
    for i in range(len(seznam_imen)):
        trikotniki[seznam_imen[i]] = seznam[i]
    return trikotniki


def iz_slovarja_doloci_polozaj_noge_nazaj_v_slovar(trikotniki):
    """
    Funkcija, ki sprejme trikotnike katerim mora biti določen vrstni red, da lahko izračuna položaje nog
    Vrne slovar trikotnikov
    """
    seznam, seznam_imen = razvrsti_v_seznam_glede_na_vrstni_red(trikotniki)
    dolocen_polozaj_noge = doloci_polozaj_noge_glede_na_vrstni_red(seznam)
    return iz_seznama_v_slovar(dolocen_polozaj_noge,seznam_imen)

def apply_permutacijo_na_trikotnike(permutacija,trikotniki):
    """
    Pomožna funkcija, ki trikotnikom nastavi vrstni red glede na permutacijo
    Permutacija: (x,y,z,...)
    """
    for i in range(len(trikotniki)):
        trikotniki[i]["vrstni_red"] = permutacija[i]
    return trikotniki

def brute_force(trikotniki):
    """ 
    * Vrne slovar optimalno postavljenih trikotnikov, ki imajo že določen položaj noge
    * Potrebno zgolj še narisati
    """
    trikotniki1 = trikotniki
    dolzina = []
    parmutacija = []
    seznam = []
    for i in range(len(trikotniki)):
        seznam.append(i)
    perm = permutations(seznam) 
    for i in list(perm): 
        trikotniki1 = apply_permutacijo_na_trikotnike(i,trikotniki1)
        trikotniki1 = iz_slovarja_doloci_polozaj_noge_nazaj_v_slovar(trikotniki1)
        dolzina.append(dolzina_urnika(trikotniki1))
        parmutacija.append(i)
    index = dolzina.index(min(dolzina))
    najboljsa_permutacija = parmutacija[index]
    narisi_trikotnike(iz_slovarja_doloci_polozaj_noge_nazaj_v_slovar(apply_permutacijo_na_trikotnike(najboljsa_permutacija,trikotniki1)))
    return iz_slovarja_doloci_polozaj_noge_nazaj_v_slovar(apply_permutacijo_na_trikotnike(najboljsa_permutacija,trikotniki1))
    
def spremeni_mesto_trikotnika(mesto,trikotniki,trikotnik):
    """
    Vzame trikotnik in ga postavi na željeno mesto
    """
    mesto_trikotnika = trikotniki[trikotnik]["vrstni_red"]
    if mesto == mesto_trikotnika:
        return trikotniki
    else:
        for i in range(len(trikotniki)):
            if i == trikotnik:
                trikotniki[trikotnik]["vrstni_red"] = mesto 
            elif mesto>mesto_trikotnika and trikotniki[i]["vrstni_red"] <= mesto and trikotniki[i]["vrstni_red"]>= mesto_trikotnika:
                trikotniki[i]["vrstni_red"] = trikotniki[i]["vrstni_red"]-1
            elif mesto < mesto_trikotnika and trikotniki[i]["vrstni_red"] <= mesto_trikotnika and trikotniki[i]["vrstni_red"] >= mesto:
                trikotniki[i]["vrstni_red"] = trikotniki[i]["vrstni_red"]+1
        return trikotniki

def printanje(trikotniki):
    for i in range(len(trikotniki)):
        print(f"""trikotnik {i} ja na mestu""",trikotniki[i]["vrstni_red"])

def greedy_algoritem(trikotniki,prikaz_simulacije=False):
    """
    * Naredi nov slovar greedy_trikotniki
    * V prvi zanki doda slovarju greedy_trikotniki trikotnik iz seznama vseh trikotnikov in hkrati beleži optimalne lokalne podatke
    * V drugi zanki preizkusi vse možne izbire, kam lahko vtakne novi trikotnik in si zabeleži tisto izbiro, ki je lokalno optimalna
    * Nariše in vrne trikotnike urejene z Greedy algoritmom
    * Zahtevnost cca. c*(št. trikotnikov)^2
    """
    greedy_trikotniki = dict()
    opt_dolzina = []
    opt_trikotniki = []
    for i in range(len(trikotniki)):
        if i > 0:
            greedy_trikotniki = opt_trikotniki[i-1]
        greedy_trikotniki[i] = trikotniki[i]
        lok_dolzina=[]
        lok_trikotniki=[]

        for j in range(len(greedy_trikotniki)):
            trikotniki1 = spremeni_mesto_trikotnika(j,greedy_trikotniki,i)
            dolocene_noge = iz_slovarja_doloci_polozaj_noge_nazaj_v_slovar( trikotniki1)
            lok_dolzina.append(dolzina_urnika(dolocene_noge))
            lok_trikotniki.append(j)
            if prikaz_simulacije:
#                printanje(dolocene_noge)
                dolzina = dolzina_urnika(dolocene_noge) 
                print(f"{i} na mestu {j} z dolzino { dolzina }") 
                narisi_trikotnike(dolocene_noge) 

        index = lok_dolzina.index(min(lok_dolzina))    
        opt_dolzina.append(lok_dolzina[index])
        opt_trikotniki.append(iz_slovarja_doloci_polozaj_noge_nazaj_v_slovar(spremeni_mesto_trikotnika(lok_trikotniki[index],greedy_trikotniki,i)))
        if prikaz_simulacije:
            print("---------------") 
            printanje(spremeni_mesto_trikotnika(lok_trikotniki[index],greedy_trikotniki,i)) 
#            print(lok_dolzina,lok_dolzina[index],index)
            narisi_trikotnike(iz_slovarja_doloci_polozaj_noge_nazaj_v_slovar(spremeni_mesto_trikotnika(lok_trikotniki[index],greedy_trikotniki,i))) #
            print("===================") 
    if prikaz_simulacije:
        print("rezultat") 
        narisi_trikotnike(opt_trikotniki[-1])
    return opt_trikotniki[-1]




os.environ['NEOS_EMAIL'] = 'kgustavo.c.lopese@volknakone.tk'

def linearno_programiranje(trikotniki):
    """
    * Poišče optimalne položaje nog trikotnikov
    * Nariše in vrne trikotnike, katerim ni določen vrstni red, zgolj položaj nog
    """
    kriticnost_trikotnikov = []
    for _ in range(len(trikotniki)):
        kriticnost_trikotnikov.append(trikotniki[_]["dolzina"])
    T = sum(kriticnost_trikotnikov)
    CLP = ConcreteModel()
    CLP.t = Var(domain=NonNegativeReals)
    CLP.I = Set(initialize=range(len(kriticnost_trikotnikov)))
    CLP.J = Set(initialize=range(len(kriticnost_trikotnikov)))
    CLP.select_combos = Set(within = CLP.I * CLP.J, )
    CLP.s = Var(CLP.I,domain=NonNegativeReals)
    CLP.X = Var(CLP.I, CLP.J, domain=Boolean)
    CLP.constraints = ConstraintList()
    CLP.profit = Objective(expr = CLP.t , sense=minimize)
    for i, d in enumerate(kriticnost_trikotnikov):
        CLP.constraints.add(CLP.s[i] >= 0)
        CLP.constraints.add(CLP.s[i] + d <= CLP.t)
        for j, e in enumerate(kriticnost_trikotnikov[i+1:],i+1):
            m = min(d, e)
            CLP.constraints.add(CLP.X[i,j]+CLP.X[j,i]==1)
            CLP.constraints.add(CLP.s[j]-CLP.s[i]>=m-T*CLP.X[i,j])
            CLP.constraints.add(CLP.s[i]-CLP.s[j]>=m-T*CLP.X[j,i])
    solver_manager = SolverManagerFactory('neos')
    results = solver_manager.solve(CLP, opt='cplex')
    polozaj_nog = []
    count = 0
    for v in CLP.component_data_objects(Var, active=True):
        if count == len(trikotniki)+1:
            break
        elif count == 0:
            count=count+1
        else:
            count=count+1
            polozaj_nog.append(value(v))
    for z in range(len(trikotniki)):
        trikotniki[z]["polozaj_noge"] = polozaj_nog[z]
    narisi_trikotnike(trikotniki)
    return trikotniki


test = naredi_trikotnike(9,[20,20,10,4,4,4,4,5,5])
test1 = copy.deepcopy(test)
test2 = copy.deepcopy(test)

# greedy_algoritem(test2)

# linearno_programiranje(test)

# brute_force(test1)


