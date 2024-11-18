# Vos import ici
import csv
import doctest
from collections import defaultdict
import os

# le path du fichier de données
FILENAME = "population.csv"


def read_file(filename):
    """retourne les données sous la forme d'une liste de dictionnaires

    Args:
        filename (str): le nom du fichier de données (n lignes)

    Returns:
        list: n-1 dictionnaires dont les clés sont les champs de la première ligne du fichier
    
    >>> data = read_file(FILENAME)
    >>> type(data)
    <class 'list'>
    >>> len(data)
    140827
    >>> type(data[0])
    <class 'dict'>
    >>> len(data[0])
    15
    >>> data[1000]["Nom Officiel Région"]
    'Grand Est'
    >>> data[5000]["Code Officiel Département"]
    '02'
    >>> data[10000]["Code Officiel Arrondissement Départemental"]
    '001'
    >>> data[25000]["Nom Officiel Commune / Arrondissement Municipal"]
    'Baneuil'
    >>> data[50000]["Population totale"]
    '1898.0'
    >>> data[75000]["Année de recensement"]
    '2018'
    >>> data[100000]["Nom Officiel EPCI"]
    'CC de la Région de Bar-sur-Aube'
    >>> data[125000]["Nom Officiel Département"]
    'Charente-Maritime'
    >>> data[1500]["Nom Officiel Région"]
    'Occitanie'
    >>> data[5500]["Code Officiel Département"]
    '25'
    >>> data[10500]["Code Officiel Arrondissement Départemental"]
    '001'
    >>> data[25500]["Nom Officiel Commune / Arrondissement Municipal"]
    'Fontenoy'
    >>> data[50500]["Population totale"]
    '52.0'
    >>> data[75500]["Année de recensement"]
    '2015'
    >>> data[100500]["Nom Officiel EPCI"]
    'CC de Yenne'
    >>> data[125500]["Nom Officiel Département"]
    'Aube'
    """
    l = []
    #with open(filename,encoding='utf-8') as f:
       # file=csv.reader(f,delimiter=';')
       # header = next(file)
        #for row in file:
            #temp=dict()
           # for i,e in enumerate(row):
              #  temp[header[i]]=e
           # l.append(temp)
    with open(filename,encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            l.append(row)


    return l
        
        
   


def build_list_departements(data):
    """retourne la liste ordonnée des départements contenus dans les données

    Args:
        data (list): la liste de dictionnaires retournée par read_file()

    Returns:
        list: la liste ordonnée des tuples (code dpt, nom dpt)
    
    >>> data = read_file(FILENAME)
    >>> ld = build_list_departements(data)
    >>> type(ld)
    <class 'list'>
    >>> len(ld)
    99
    >>> '15' in ld
    False
    >>> 15 in ld
    False
    >>> 'Cantal' in ld
    False
    >>> ('15', 'Cantal') in ld
    True
    >>> ld[::20]
    [('01', 'Ain'), ('22', "Côtes-d'Armor"), ('40', 'Landes'), ('60', 'Oise'), ('80', 'Somme')]
    >>> ld[5::20]
    [('06', 'Alpes-Maritimes'), ('27', 'Eure'), ('45', 'Loiret'), ('65', 'Hautes-Pyrénées'), ('85', 'Vendée')]
    >>> ld[10::20]
    [('11', 'Aude'), ('30', 'Gard'), ('50', 'Manche'), ('70', 'Haute-Saône'), ('90', 'Territoire de Belfort')]
    >>> ld[15::20]
    [('16', 'Charente'), ('35', 'Ille-et-Vilaine'), ('55', 'Meuse'), ('75', 'Paris'), ('95', "Val-d'Oise")]
    >>> ld[20::20]
    [('22', "Côtes-d'Armor"), ('40', 'Landes'), ('60', 'Oise'), ('80', 'Somme')]
    >>> ld[5]
    ('06', 'Alpes-Maritimes')
    >>> ld[15]
    ('16', 'Charente')
    >>> ld[25]
    ('27', 'Eure')
    >>> ld[35]
    ('35', 'Ille-et-Vilaine')
    >>> ld[45]
    ('45', 'Loiret')
    >>> ld[55]
    ('55', 'Meuse')
    >>> ld[65]
    ('65', 'Hautes-Pyrénées')
    """
    l = []
    departements = set()
    for row in data:
        # Vérifier que les clés existent dans le dictionnaire
        if "Code Officiel Département" in row and "Nom Officiel Département" in row:
            temp = (row["Code Officiel Département"], row["Nom Officiel Département"])
            departements.add(temp)
    l= list(sorted(departements))
    return l


def build_list_communes(data):
    """retourne la liste des tuples (code, commune)

    Args:
        data (list): la liste de dictionnaires retournée par read_file()

    Returns:
        list: la liste ordonnée des tuples (code commune, nom commune)
    
    
    
    """
    l = []
    listeCommunes=set()
    for e in data :
        temp=(e["Code Officiel Commune / Arrondissement Municipal"],e["Nom Officiel Commune / Arrondissement Municipal"])
        listeCommunes.add(temp)
    l= list(sorted(listeCommunes))
    return l


def get_pop_commune(data, code):
    """retourne la population totale d'une commune pour l'année de recensement la plus récente

    Args:
        data (list): la liste de dictionnaires retournée par read_file()
        code (str) : code de la commune considérée

    Returns:
        (int, str, str): (nom de la commune, population totale, année de recensement concernée)

    >>> data = read_file(FILENAME)
    >>> get_pop_commune(data, '39124')
    ('Chaumergy', 492, '2018')
    >>> get_pop_commune(data, '63001')
    ('Aigueperse', 2790, '2018')
    >>> get_pop_commune(data, '76005')
    ('Amfreville-la-Mi-Voie', 3354, '2018')
    >>> get_pop_commune(data, '74275')
    ('Talloires-Montmin', 2039, '2018')
    >>> get_pop_commune(data, '94022')
    ('Choisy-le-Roi', 46366, '2018')
    >>> get_pop_commune(data, '11151')
    ("Fontiès-d'Aude", 509, '2018')
    >>> get_pop_commune(data, '53210')
    ("Saint-Denis-d'Anjou", 1581, '2018')
    >>> get_pop_commune(data, '30266')
    ('Saint-Jean-de-Maruéjols-et-Avéjan', 897, '2018')
    >>> get_pop_commune(data, '07222')
    ('Saint-Cierge-sous-le-Cheylard', 211, '2018')
    >>> get_pop_commune(data, '00000')
    
    """
 
    for e in data: 
        if  e["Code Officiel Commune / Arrondissement Municipal"] ==code :
            nom = e["Nom Officiel Commune / Arrondissement Municipal"]
            pop=e["Population totale"]
            anne=e["Année de recensement"]
            break

    t = (nom, pop, anne)
    return t


def multi_dict(K, type):
    if K == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: multi_dict(K-1, type))

def build_dict_departements(data):
    # Initialisation du dictionnaire
    d = dict()
    
    # Appel à la fonction pour obtenir la liste des départements
    listeDep = build_list_departements(data)
    
    # Parcours des départements
    for e in listeDep:
        nbCommune = 0
        popTotale = 0
        
        # Parcours des données
        for elt in data:
            if elt["Code Officiel Département"] == e[0]:
                nbCommune += 1
                popTotale += float(elt["Population totale"])
        
        # Ajout des résultats dans le dictionnaire
        d[e[0]] = (nbCommune, popTotale)

    return d


            
                


    return h
    
    
def stat_by_dpt(dd, dpt):
    """Retourne un tuple (nombre de communes, population totale)

    Args :
        dd (dict) : le dictionnaire retourné par build_dict_departements()
        dpt (str) : le département concerné

    Returns :
        tuple : (nombre de communes, population totale)
    
    >>> data = read_file(FILENAME)
    >>> dd = build_dict_departements(data)
    >>> s = stat_by_dpt(dd, '87')
    >>> type(s)
    <class 'tuple'>
    >>> len(s)
    2
    >>> s
    (202, 383163)
    >>> stat_by_dpt(dd, '77')
    (514, 1433625)
    >>> stat_by_dpt(dd, '13')
    (134, 2058818)
    >>> stat_by_dpt(dd, '08')
    (452, 278875)
    >>> stat_by_dpt(dd, '21')
    (713, 553151)
    >>> stat_by_dpt(dd, '2A')
    (124, 160294)
    >>> stat_by_dpt(dd, '34')
    (344, 1179337)
    >>> stat_by_dpt(dd, '53')
    (264, 346208)
    >>> stat_by_dpt(dd, '64')
    (546, 698710)
    >>> stat_by_dpt(dd, '75')
    (20, 2192485)
    >>> stat_by_dpt(dd, '18')
    (290, 310910)
    >>> sbd = stat_by_dpt(dd, 'Corse')

    """
    # votre code ici

    hello =dd[dpt]

    t = (hello[0], hello[1])

    return t

def main():
    

   # region lecture
    print("")
    print("")
    print("//////////////////////////////////////////")
    print("lecture du fichier: ")
    print("")
    print("")

    data = read_file(FILENAME)
    for e in data :
        print(e)
    
    # region liste dep

    print("")
    print("")
    print("//////////////////////////////////////////")
    print("liste departement ")
    print("")
    print("")

    print("liste departement ")
    l = build_list_departements(data)
    for e in l:
        print(e)

    # region liste communes

    print("")
    print("")
    print("//////////////////////////////////////////")
    print("liste des communes ")
    print("")
    print("")

    
    c = build_list_communes(data)
    for e in c:
        print(e)

    # region population commune

    print("")
    print("")
    print("//////////////////////////////////////////")
    print("population commune ")
    print("")
    print("")
    

    p = get_pop_commune(data, '39124')
    print(p)

    # region dictionnaire departement nb communes nb habitant

    print("")
    print("")
    print("//////////////////////////////////////////")
    print("dictionnaire departement nb communes nb habitant ")
    print("")
    print("")

    d = build_dict_departements(data)
    print(d)

     # region nombre de commmune et nombre habitatn d'un departmemnt

    print("")
    print("")
    print("//////////////////////////////////////////")
    print("nombre de commmune et nombre habitatn d'un departmemnt ")
    print("")
    print("")


    s = stat_by_dpt(d, '80')
    print(s)

    
# Ne pas modifier le code ci-dessous
if __name__ == '__main__':
    
    main()
