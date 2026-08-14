# Forme  de graphe utilisée: 
#     * Graphe sanas coûts :
#         graphe = {
#             "A": ["B", "C"],
#             "B": ["A", "C"],
#             "C": ["A", "B"],
#         }

#     * Graphe avec coûts :
#         graphe = {
#             "A": [("B", 1), ("C", 2)],
#             "B": [("A", 1), ("C", 3)],
#             "C": [("A", 2), ("B", 3)],
#         }   



#Fonction qui permet d' extraire la liste d'arêtes d'un graphe donné sous forme de dictionnaire
def extraire_aretes(graphe , cout , oriente ):
    aretes = []
    couples_deja_vus = set() #Pour éviter les doublons dans le cas d'un graphe non orienté
    if(cout ): #Pour un graphe avec coûts
         for sommet in graphe :
            for voisin, poids in graphe[sommet]:
                if oriente:
                    aretes.append((sommet , voisin , poids))
                else:
                    couple = tuple(sorted((sommet, voisin)))
                    if couple not in couples_deja_vus:
                        aretes.append((sommet , voisin , poids))
                        couples_deja_vus.add(couple)

    else: #Pour un graphe sans coûts
       for sommet in graphe :
            for voisin in graphe[sommet]:
                if oriente:
                    aretes.append((sommet , voisin))
                else:
                    couple = tuple(sorted((sommet, voisin)))
                    if couple not in couples_deja_vus:
                        aretes.append((sommet , voisin))
                        couples_deja_vus.add(couple)
    return aretes

    
#Cette fonction permet de construire un graphe à partir d'une liste de sommets et d'une liste d'arêtes.
def construire_graphe(sommets , aretes , cout , oriente ):
    graphe = {s: [] for s in sommets}
    
    if(cout): #Pour creer un graphe pondéré
        for u , v , p in aretes : 
            graphe[u].append((v,p))
            if not oriente: # Si le graphe n'est pas orienté, on ajoute l'arête dans les deux sens
                graphe[v].append((u,p))
    else:   #Pour creer un graphe non pondéré
        for u , v in aretes : 
            graphe[u].append(v)
            if not oriente:  # Si le graphe n'est pas orienté, on ajoute l'arête dans les deux sens
                graphe[v].append(u)
    return graphe


# Cette fonction permet de construire un dictionnaire de coûts à partir d'un graphe donné .
# Cette fonction est utilisée dans la fonction relacher qui est utilisée dans l'algorithme de Dijkstra et TopoDAG
def construire_cout(graphe,oriente):
    cout = {s: {} for s in list(graphe.keys())}
    aretes = extraire_aretes(graphe,True,oriente)
    for u , v , p in aretes :
        cout[u][v] = p
        if not oriente:
            cout[v][u] = p
    return cout


#Cette fonction permet de visiter un graphe donné sous forme de dictionnaire à partir d'un sommet donné.
#Cette fonction est utilisée dans la fonction tri_topologique 
def visite(G,s,couleur,ordre):
    couleur[s] = "gray"
    for voisin in succ(G,s,True,True):
        if couleur[voisin] == "white":
            visite(G,voisin,couleur,ordre)
    couleur[s] = "black"
    ordre.append(s)


#Cette fonction permet de trier topologiquement un graphe orienté acyclique (DAG) donné sous forme de dictionnaire.
#Cette fonction est utilisée dans l'algorithme TopoDAG
def tri_topologique(G):
    couleur = {s: "white" for s in list(G.keys())}
    ordre = []

    for s in list(G.keys()):
        if couleur[s] == "white":
            visite(G, s, couleur, ordre)

    ordre.reverse()  
    return ordre


#Cette fonction est utilisee dans la fonction "Kruskal" de MST  
def meme_composant(E, s_i, s_j):
    visited = {}
    traites = []
    if s_i == s_j:
        return True
    
    while traites:
        sommet = traites.pop()

        if sommet == s_j:
            return True

        for voisin in E.get(sommet , []):
            if voisin not in visited : 
                visited.add(voisin)
                traites.append(voisin)
    return False



#Fonction qui retourne la liste des voisins d'un sommet donné dans un graphe donné 
def succ(G,sommet,cout,oriente ):
    voisin=[]
    arret=extraire_aretes(G,cout,oriente)
    for sommet1,sommet2 in arret:
        if(sommet1==sommet):
            voisin.append(sommet2)
        elif(sommet2==sommet):
            voisin.append(sommet1)
    return(voisin)


#Page 22 : Fonction qui affiche les successeurs d'un sommet donné
def afficherSucc(G,sommet,cout,oriente):
    for s in succ(G,sommet,cout,oriente):
        print(s)


#Page 33 : BFS : Fonction qui permet de faire le parcours en largeur d'un graphe donné à partir d'un sommet donné
def parcour_en_largeur(G,s0):
    sommets = list(G.keys())
    #INITIALISATION
    file = list()
    P = {}
    col=["green" for i in range(len(sommets))]
    couleur = {}
    for s in sommets:
        P[str(s)]=None
        couleur[str(s)] = "green"
    file.append(s0)
    couleur[str(s0)]="gray"

    #PARCOUR
    while len(file) > 0:
        s_k = file[0]
        s_i=0
        i=0
        indice =0
        successeurs = succ(G,s_k,False,False)
        for s_i in successeurs:
            if couleur[str(s_i)] == "green":
                file.append(s_i)
                couleur[str(s_i)]="gray"
                for indice in range(len(couleur.keys())):
                    col[indice]=couleur[str(sommets[indice])]
                P[str(s_i)] = s_k            

            i+=1
        couleur[str(s_k)]="black"
        file.remove(s_k)
    return P



# Page 35 : Fonction qui permet de calculer la distance entre un sommet donné et tous les autres sommets du graphe
def calcul_distance(G,s_0):
    sommets=list(G.keys())
    S_i=0
    P={}
    couleur = {}
    distance = {}
    file = list()

    #INITIALISATION
    for s_i in sommets:
        P[s_i]=None
        couleur[s_i]="green"
        distance[s_i]=float('inf')
    file.append(s_0)
    couleur[s_0]="gray"
    distance[s_0]=0

    while len(file) > 0:
        s_k = file[0]
        for s_i in succ(G,s_k,False,False):
            if couleur[s_i] == "green":
                file.append(s_i)
                couleur[s_i]="gray"
                distance[s_i]=distance[s_k]+1
                P[s_i]=s_k
        couleur[s_k]="black"
        file.remove(s_k)
    return distance,P


#Page 36    :   Affichage du plus court chemin
def plusCourtChemin(s_0,s_j,P):
    if s_j == s_0:
        print(s_0)
    elif P[s_j] == None:
        print("Il n’y a pas de chemin de ",s_0 ," jusque ",s_j)
    else:
        plusCourtChemin(s_0,P[s_j],P)
        print(" suivi de ",s_j)

#Page 38    :   Parcours en profondeur (Depth First search / DFS)
def DFS(G,s_0):
    pile=[]
    P={}
    couleur = {}
    sommets=list(G.keys())
    s_i=0
    for s_i in sommets:
        P[s_i]=None
        couleur[s_i]="green"
    pile.append(s_0)
    couleur[s_0]="gray"
    while len(pile) > 0:
        s_k = pile[len(pile)-1]
        for s_i in succ(G,s_k,False , True):
            if couleur[s_i] == "green":
                pile.append(s_i)
                couleur[s_i]="gray"
                P[s_i]=s_k
            else:
                couleur[s_k]="black"
                pile.remove(s_k)
    return P




#Page 39 : Version récursive de DFS
def DFSrec(G,s_0):
    couleur[s_0]="gray"
    for s_i in succ(G,s_0,False , True):
        if couleur[s_i] == "green":
            P[s_i]=s_0
            DFSrec(G,s_i)
    couleur[s_0]="black"



#Page 40 : Recherche de circuits
def DFSrec(G,s_0):
    couleur[s_0]="gray"
    for s_i in succ(G,s_0,False , True):
        if couleur[s_i] == "gray":
            print("Circuit")
        elif couleur[s_i] == "green":
            P[s_i]=s_0
            DFSrec(G,s_i)
    couleur[s_0]="black"
    return(couleur)



#Page 41: Numérotation des sommets
    ###Procédure DFSnum(g)
def DFSnum(G):
    num = {}
    cpt = 1
    couleur = ["green" for i in range(len(G.keys()))]
    for s_i in G.keys():
        if couleur[s_i] == "green":
            DFSnumrec(G,s_i,cpt,couleur,num)
    
    return(num)


    ###Procédure DFSnumrec(g, s0, cpt, couleur)
def DFSnumrec(G,s_0,cpt,couleur,num):
    couleur[s_0]="gray"
    for s_i in succ(G,s_0):
        if couleur[s_i] == "green":
            P[s_i]=s_0
            DFSnumrec(G,s_i,cpt,couleur)
    couleur[s_0]="black"
    num[s_0]=cpt
    cpt+=1



#Page 43 : Recherche des composantes fortements connexes
def SCC(G):

    Scc=[]

    num = DFSnum(G)
    #Construction  de graphe g'= (S, A' ) tel que A' = {(si , sj ) | (sj , si ) ∈ A}

    G_t={}
    Sommets=list(G.keys())
    Arretes=[]
    for s_j,s_i in extraire_aretes(G,False,True):
        Arretes.append((s_i,s_j))
    G_t= construire_graphe(Sommets,Arretes,False,True)
    Couleur=["green" for sommet in Sommets]

    #Ranger dans l'ordre decroissante selon le num les sommets 
    Sommets= sorted(Sommets,key=lambda x:num[x],reverse=True)

    for sommet in Sommets:
        Blanc=[]
        if Couleur[sommet] == "green" :
            Blanc.append(sommet)
            Couleur=DFSrec(G_t,sommet)
            if(Couleur[sommet]=="black"):
                Scc.append(sommet)
    
    return(Scc)
    


#Page 48 : Fonction qui permet de relacher un sommet s_j à partir d'un sommet s_i
#count est un dictionnaire qui contient les poids des arêtes du graphe
#Forme de cout :
#    cout = {
#        "A": {"B": 4, "C": 2},
#        "B": {"A": 4, "C": 1},
#        "C": {"A": 2, "B": 1},
#    }


def relacher(s_i,s_j,P,d,cout):
    if d[s_j] > d[s_i] + cout[s_i][s_j]:
        d[s_j] = d[s_i] + cout[s_i][s_j]
        P[s_j]=s_i

    


#Page 51  : Algorithme de Dijkstra
def Dijkstra(G,cout,s0):
    d={}
    P={}
    couleur={}
    for s_i in list(G.keys()):
        d[s_i] = float("inf")
        P[s_i] = None
        couleur[s_i] = "green"

    d[s0] = 0
    couleur[s0] = "gray"
    while any(couleur[s] == "gray" for s in list(G.keys())):
        s_i = min((s for s in list(G.keys()) if couleur[s] == "gray"), key=lambda s: d[s])
        for s_j in succ(G,s_i,True,True):
            if couleur[s_j] == "green" or couleur[s_j] == "gray":
                relacher(s_i,s_j,P,d,cout)
                if couleur[s_j] == "green":
                    couleur[s_j] = "gray"
                    
        couleur[s_i] = "black"

    return d, P


#Page 55 : Algorithme TopoDAG 
# Pour le graphe DAG (graphe orienté acyclique, sans circuit) seulement. 
def TopoDAG(G,cout,s0):
    
    d={}
    P={}
    couleur={}
    for s_i in list(G.keys()):
        d[s_i] = float("inf")
        P[s_i] = None

    d[s0] = 0

    #Trier topologiquement les sommets de g
    for s_i in tri_topologique(G):
        for s_j in succ(G,s_i,True,True):
            relacher(s_i,s_j,P,d,cout)
    return P,d



#Page 59 (186) : Algorithme de Bellman-Ford
def BellmanFord(G,cout,s0):
    d={}    
    P={}
    for s_i in list(G.keys()):
        d[s_i] = float("inf")
        P[s_i] = None
    d[s0] = 0

    for k in range(1,len(list(G.keys()))-1):
        for s_i,s_j in extraire_aretes(G,True,True):
            relacher(s_i,s_j,P,d,cout)

    if any(d[s_i] + cout[s_i][s_j] < d[s_j] for s_i,s_j in extraire_aretes(G,True,True)):
        print("G contient un circuit absorbant")

    return P,d


#Page 63 :  Algorithme générique 
def MSTgenerique(G):
    S=list(G.keys())
    E=[]
    P=[]
    P.append(S[0])
    while len(E) < len(S) -1 :
        min_arete = None

        for u , v , poids in extraire_aretes(G,True,False):
            
                if min_arete is None or poids < min_arete[2]:
                    min_arete=(u,v,poids)

        
        E.append(min_arete)
        P.append(u)
        P.append(v)

    return E



###Page 65 (203) : Algorithme de Kruskal 
def Kruskal(G):
    E = []
    A_trie = []
    arete_min = None
    #Triage des arêtes de A par order de cout croissant
    while len (A_trie) < len(extraire_aretes(G,True,False)):
        for u , v , poids in extraire_aretes(G,True,False):
            if arete_min is None or poids < arete_min[2]:
                arete_min = (u,v,poids)
        A_trie.append(arete_min)

    for u,v,p in A_trie :
        if not meme_composant(E, u, v) : #tester la connexité entre deux sommets. 
            arete = (u,v,p)
            E.append(arete)

    return E



###Page 67  : Algorithme de Prim
def Prim(G,cout):
    S = list(G.keys())
    s0=S[0]
    E = []
    P = {}
    C = {}

    for s_i in S :
        if s_i in succ(G,s0,True,False):
            P[s_i] = s0
            C[s_i] = cout[s0][s_i]
        else:
            P[s_i] = None
            C[s_i] = float("inf")   
    

    while len(P) != len(S):
        s_i = min((s for s in P.keys()), key=lambda s: C[s])
        E.append((P[s_i], s_i, C[s_i]))
        del P[s_i]
        del C[s_i]

        for s_j in succ(G,s_i,True,False):
            if s_j not in P.keys() and cout[s_i][s_j] < C[s_j]:
                P[s_j] = s_i
                C[s_j] = cout[s_i][s_j]

    return E

    

    