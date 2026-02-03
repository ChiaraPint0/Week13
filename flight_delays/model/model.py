import networkx as nx
from flight_delays.database.DAO import DAO
class Model:
    def __init__(self):
        #COSTRUISCO LISTA E DIZIONARIO DI NODI
        self._listaAeroporti = DAO.getAllAirports() #Qui sto ancora prendendo tutti gli aeroporti
        self._dizionarioAeroporti = {}
        for airport in self._listaAeroporti:
            self._dizionarioAeroporti[airport.ID] = airport

        self._grafo = nx.Graph()
        self._nodes = []
        self._edges = []

        # Aeroporti selezionati dalla dropdown
        self._partenza = None
        self._arrivo = None



    def buildGraph(self, min):
        #NODI
        self._nodes = DAO.get_nodes(min, self._dizionarioAeroporti)
        self._grafo.add_nodes_from(self._nodes)
        #ARCHI
        connessioni = DAO.get_edges(self._dizionarioAeroporti)
        for c in connessioni:
            if c.aPartenza in self._grafo and c.aArrivo in self._grafo:
                if self._grafo.has_edge(c.aPartenza, c.aArrivo):
                     self._grafo[c.aPartenza][c.aArrivo]["weight"] += c.voli #incrementare il peso
                else:
                    self._grafo.add_edge(c.aPartenza, c.aArrivo, weight = c.voli)


    def getSortedNeighbors(self, v0): #recupera i vicini del nodo v0 dal grafo
        vicini = self._grafo.neighbors(v0) #trova i vicini di v0
        viciniTuple = [] #lista vuota che conterrà le tuple (nodo_vicino, peso_arco)
        for v in vicini: #itero su ciascun vicino del nodo v0
            viciniTuple.append((v, self._grafo[v0][v]["weight"]))#creo la tupla con il nodo vicino v e il peso dell'arco tra v0 e v, self._grafo[v0][v]["weight"] con questo accede all'attributo weight tra i due nodi
            viciniTuple.sort(key = lambda x: x[1], reverse = True) #ogni volta riordino la lista in ordine decrescente di peso
        return viciniTuple #restituisco la lista