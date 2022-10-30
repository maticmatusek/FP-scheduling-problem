from gettext import find
import random
import matplotlib.pyplot as plt
import numpy as np

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
        slovar[i]["vrstni_red"] = i+1
    return slovar

def narisi_trikotnike(trikotniki):
    for i in range(len(trikotniki)):
        narisi_trikotnik(trikotniki[i])
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
    
#def narisi_glede_na_polozaj(trikotniki):
#    seznam_vrstni_red = []
#    seznam_dolzin = []
#    slovar = {}
#    for i in range(len(trikotniki)):
#        seznam_dolzin.append(trikotniki[i]["dolzina"])
#        seznam_vrstni_red.append(trikotniki[i]["vrstni_red"])
#    for i in range(1,len(trikotniki)+1):
#        index = seznam_vrstni_red.index(i)
        
