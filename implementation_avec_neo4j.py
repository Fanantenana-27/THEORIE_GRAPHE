from neo4j import GraphDatabase
import algorithmes as algo

uri = "bolt://localhost:7687"
user="neo4j"
password ="fanakely"
driver = GraphDatabase.driver(uri,auth=(user,password))


#Graphe sur Neo4j avec : 
#Label : Sommets 
#Propriete de chaque sommet : id
#Liaison : LIEE


#Page 22 : Fonction qui affiche les successeurs d'un sommet donné
def afficherSucc(id):
    with driver.session as session:
        instruction = """
        MATCH (s:Sommets {id : $id})-[LIEE]->(voisin)
        RETURN voisin , voisin.id as Id 
        """
        session.run(instruction,id = id)




#Page 33 : BFS : Fonction qui permet de faire le parcours en largeur d'un graphe donné à partir d'un sommet donné
def parcour_en_largeur():
    with driver.session as session :
        instruction = """
        MATCH (depart {id: 0})
        CALL apoc.path.spanningTree(depart, {
            bfs: true,
            uniqueness: "NODE_GLOBAL"
        })
        YIELD path
        WITH depart, nodes(path) AS sommets
        WHERE size(sommets) > 1
        RETURN
            ns[sommetse(ns)-1].nom AS sommet,
            ns[sommets(ns)-2].nom AS pere;

        """

        session.run(instruction)


# Page 35 : Fonction qui permet de calculer la distance entre un sommet donné et tous les autres sommets du graphe
def calcul_distance():
    with driver.session as session :
        instruction = """
        MATCH (depart {id: 0})
        CALL apoc.path.spanningTree(depart, {
            bfs: true,
            uniqueness: "NODE_GLOBAL"
        })
        YIELD path
        WITH nodes(path) AS ns , path
        RETURN
            ns[size(ns)-1].nom AS sommet,
            length(path) AS distance,
            CASE
                WHEN size(ns) > 1
                THEN ns[size(ns)-2].nom
                ELSE null
            END AS pere
        ORDER BY distance, sommet;
        """ 
        session.run(instruction)

#Page 36    :   Affichage du plus court chemin
def plusCourtChemin(sommet_depart,sommet_arrive):
    with driver.session as session:
        instruction = """
        MATCH (depart:Connected {id : $id_depart})
        MATCH (arriver:Connected {id : $id_arriver})
        WHERE depart <> arriver
        MATCH p=shortestPath((depart)-[*]->(arriver))
        RETURN [n IN nodes(p) | n.id] AS chemin;
        """

        session.run(instruction,id_depart=sommet_depart, id_arriver=sommet_arrive )


#Page 38    :   Parcours en profondeur (Depth First search / DFS)
def DFS():
    with driver.session as session:
        instruction = """
        MATCH (depart {local_id: 0})
        CALL apoc.path.spanningTree(depart, {
            bfs: false,
            uniqueness: "NODE_GLOBAL"
        })
        YIELD path
        WITH nodes(path) AS sommets
        WHERE size(sommets) > 1
        RETURN
            sommets[size(sommets)-1].nom AS sommet,
            sommets[size(sommets)-2].nom AS pere;
        
        """

        session.run(instruction)