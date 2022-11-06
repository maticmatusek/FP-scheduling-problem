from cgi import test
from cgitb import text
from gettext import find
import random
from turtle import color
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, solve
from itertools import count, permutations 

def naredi_trikotnik(dolzina=None,spodnja_meja=1,zgornja_meja=10,celostevilski=True):
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
    plt.text(x=max(konec)/2,y=max(dolzina)+1,s=f"Dolžina urnika: {dolzina_urnik}",color="r")
    return plt.show()

def dolzina_urnika(trikotniki):
    seznam_polozaj_noge = []
    seznam_dolzina = []
    for i in range(len(trikotniki)):
        seznam_dolzina.append(trikotniki[i]["dolzina"])
        seznam_polozaj_noge.append(trikotniki[i]["polozaj_noge"])
    maksimum = max(seznam_polozaj_noge)
    for i in range(len(seznam_polozaj_noge)):
        if maksimum == seznam_polozaj_noge[i]:
            return seznam_polozaj_noge[i] + seznam_dolzina[i]
    
def razvrsti_v_seznam(trikotniki):
    seznam = [None] * len(trikotniki)
    seznam_imen = [None] * len(trikotniki)
    for i in range(len(trikotniki)):
        seznam[trikotniki[i]["vrstni_red"]] = trikotniki[i]
        seznam_imen[trikotniki[i]["vrstni_red"]] = i
    return seznam

def doloci_polozaj_noge_glede_na_vrstni_red(urejeni_trikotniki_v_seznamu):
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
                elif urejeni_trikotniki_v_seznamu[j]["dolzina"] < urejeni_trikotniki_v_seznamu[i]["dolzina"]:
                    seznam[j] = urejeni_trikotniki_v_seznamu[i]["dolzina"] - ( urejeni_trikotniki_v_seznamu[i]["dolzina"] - urejeni_trikotniki_v_seznamu[j]["dolzina"] ) - (urejeni_trikotniki_v_seznamu[i]["polozaj_noge"] - urejeni_trikotniki_v_seznamu[j]["polozaj_noge"] )
            index = seznam.index(max(seznam))
            urejeni_trikotniki_v_seznamu[i]["polozaj_noge"] = urejeni_trikotniki_v_seznamu[i]["polozaj_noge"] + seznam[index]
    return urejeni_trikotniki_v_seznamu

def iz_seznama_v_slovar(seznam):
    trikotniki = dict()
    for i in range(len(seznam)):
        trikotniki[i]=seznam[i]
    return trikotniki


#narisi_trikotnike( iz_seznama_v_slovar( doloci_polozaj_noge_glede_na_vrstni_red( razvrsti_v_seznam( naredi_trikotnike(6,[9,2,1,1.5,3,10]) ) ) ) )
#narisi_trikotnike( iz_seznama_v_slovar( doloci_polozaj_noge_glede_na_vrstni_red( razvrsti_v_seznam( naredi_trikotnike(6,[9,2,0.9,2.1,3,10]) ) ) ) )


# ni vredu brut fore bo treba še enkrat narest
def brute_force(trikotniki):
    trikotniki1 = trikotniki
    dolzina = []
    parmutacija = []
    seznam = []
    for i in range(len(trikotniki)):
        seznam.append(i)
    perm = permutations(seznam) 
    for i in list(perm): 
        for j in trikotniki:
            trikotniki1[j]["vrstni_red"] = i[j]
        print(i)
        print(trikotniki1)
        dolzina.append(dolzina_urnika(trikotniki1))
        parmutacija.append(i)
        print(dolzina_urnika(trikotniki1))
    print(dolzina)
    index = dolzina.index(min(dolzina))
    najboljsa_permutacija = parmutacija[index]
    for k in trikotniki1:
            trikotniki1[k]["vrstni_red"] = najboljsa_permutacija[k]
    print(najboljsa_permutacija)
    print(trikotniki1)
    return trikotniki1
    
#test = naredi_trikotnike(10,[1,2,1,10,1,1,1,20,4,1])
#test =  naredi_trikotnike(3,[1,2,10])
#narisi_trikotnike( iz_seznama_v_slovar( doloci_polozaj_noge_glede_na_vrstni_red( razvrsti_v_seznam( test ) ) ) )
#brut = brute_force(test)
#narisi_trikotnike( iz_seznama_v_slovar( doloci_polozaj_noge_glede_na_vrstni_red( razvrsti_v_seznam( brut ) ) ) )        