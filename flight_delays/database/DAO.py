from flight_delays.database.DB_connect import DBConnect
from flight_delays.model.airport import Airport
from flight_delays.model.connessione import Connessione


class DAO:

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_nodes(min, dizionarioAeroporti):  # passo alla funzione il dizionario di Aeroporti
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = ("""SELECT tmp.id, tmp.iata_code, COUNT(*) AS somma
                    FROM (SELECT a.id, a.iata_code, f.airline_id
                          FROM airports a, flights f
                          WHERE a.id = f.origin_airport_id OR a.id = f.destination_airport_id 
                          GROUP BY a.id, a.iata_code, f.airline_id) AS tmp
                    GROUP BY tmp.id, tmp.iata_code
                    HAVING somma >= %s

                    """)
        try:
            cursor.execute(query, (min,))
            for row in cursor:
                id = row['id']  # prendo id di un aeroporto tramite la query
                airport = dizionarioAeroporti[id]  # vado nel dizionario a prendere aeroporto con quell'id
                result.append(airport)  # aggiungo al risultato

        except Exception as e:
            print(f"Errore durante la query: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_edges(dizionarioAeroporti):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None
        cursor = cnx.cursor(dictionary=True)
        query = ("""SELECT f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID, COUNT(*) as VOLI
                    FROM `flights` f 
                    GROUP BY f.ORIGIN_AIRPORT_ID, f.DESTINATION_AIRPORT_ID

                    """)
        try:
            cursor.execute(query)
            for row in cursor:
                idPartenza = row['ORIGIN_AIRPORT_ID']
                idArrivo = row['DESTINATION_AIRPORT_ID']
                aPartenza = dizionarioAeroporti[idPartenza]
                aArrivo = dizionarioAeroporti[idArrivo]
                voli = row['VOLI']
                result.append(Connessione(aPartenza, aArrivo, voli))

        except Exception as e:
            print(f"Errore durante la query: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()
        return result