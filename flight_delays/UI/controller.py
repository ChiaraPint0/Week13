import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_analizzaAeroporti(self, e):
        try:
            min = int(self._view.txtNumCompagnieMinimo.value)

        except ValueError:
            self._view.create_alert("Inserisci un numero valido")
            return

        self._model.buildGraph(min)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"grafo: {self._model._grafo}"))
        self.populate_dd()
        self._view.update_page()



        """name = self._view.txt_name.value
        if name is None or name == "":
            self._view.create_alert("Inserire il nome")
            return
        self._view.txt_result.controls.append(ft.Text(f"Hello, {name}!"))
        self._view.update_page()"""


    def populate_dd(self):
        for node in self._model._nodes:
            self._view.ddAeroportoPartenza.options.append(ft.dropdown.Option(text = node.AIRPORT, key = node.ID))
            self._view.ddAeroportoArrivo.options.append(ft.dropdown.Option(text=node.AIRPORT, key=node.ID))
        self._view.btnAeroportiConnessi.disabled = False
        self._view.ddAeroportoPartenza.disabled = False
        self._view.ddAeroportoArrivo.disabled = False

        self._view.txtNumTratteMassimo.disabled = False
        self._view.btn_CercaItinerario.disabled = False

        self._view.update_page()

    #metodo chiamato quando l'utente cambia la selezione della Dropdown dell'aeroporto di partenza
    def readDDPartenza(self,e):
        idPartenza = int(self._view.ddAeroportoPartenza.value)
        #memorizzo l'aeroporto selezionato nel model
        self._model._partenza = self._model._dizionarioAeroporti[idPartenza]

        print("Aeroporto partenza: ", self._model._partenza)

    #metodo chiamato quando l'utente cambia la selezione della Dropdown dell'aeroporto di arrivo
    def readDDArrivo(self,e):
        idArrivo = int(self._view.ddAeroportoArrivo.value)
        #memorizzo l'aeroporto selezionato nel model
        self._model._arrivo = self._model._dizionarioAeroporti[idArrivo]

        print("Aeroporto arrivo: ", self._model._arrivo)


    def handle_aeroportiConnessi(self, e):
        u = self._model._partenza
        print("Partenza selezionata:", u)
        print("Nodi del grafo:", list(self._model._grafo.nodes))
        print(u in self._model._grafo)

        print(u)
        if u is None:
            self._view.create_alert("Selezionare un aeroporto di partenza")
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Vicini di: {self._model._partenza}"))
        viciniTuple = self._model.getSortedNeighbors(u)
        for v in viciniTuple:
            self._view.txt_result.controls.append(ft.Text(f"{v[1]}-{v[0]}"))
        self._view.update_page()

    def handle_cercaItinerario(self, e):
        pass