

from database.consumo_DAO import ConsumoDAO
from database.impianto_DAO import ImpiantoDAO


'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()


    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        # TODO
        self.load_impianti()
        lista_impianti= self._impianti
        medie_consumi_mensili= []
        lista_consumi=[]
        for impianto in lista_impianti:
            lista_consumi_importata = ConsumoDAO.get_consumi(impianto.id)
            for consumo in lista_consumi_importata:
                if consumo.id_impianto == impianto.id:
                    if consumo.data.month == mese:
                        lista_consumi.append(consumo.kwh)
            consumo_medio= sum(lista_consumi)/len(lista_consumi)
            coppia= impianto.nome, consumo_medio
            medie_consumi_mensili.append(coppia)
        return medie_consumi_mensili


    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        # TODO
        if  giorno>7:
            if self.__costo_ottimo== -1 or costo_corrente< self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = sequenza_parziale


        else:
            chiavi = list(consumi_settimana.keys())
            for impianto in chiavi:
                costo= costo_corrente
                costo += consumi_settimana[impianto][giorno-1]
                if impianto != ultimo_impianto and ultimo_impianto is not None:
                    costo += 5
                sequenza_parziale_aggiornata = list(sequenza_parziale)
                sequenza_parziale_aggiornata.append(impianto)

                self.__ricorsione(sequenza_parziale_aggiornata, giorno +1, impianto, costo, consumi_settimana)



    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        # TODO
        self.load_impianti()
        lista_impianti = self._impianti
        dizionario_settimanale = {}
        for impianto in lista_impianti:
            consumi_settimanali = []
            lista_consumi_importata = ConsumoDAO.get_consumi(impianto.id)
            for consumo in lista_consumi_importata:
                if consumo.data.month == mese:
                    consumi_settimanali.append(consumo.kwh)
                if len(consumi_settimanali)==7:
                    break

            dizionario_settimanale[impianto.id] = consumi_settimanali
            print(dizionario_settimanale)
        return dizionario_settimanale












