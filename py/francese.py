'''
##### SIMULATORE CASH FLOW AMMORTAMENTO FRANCESE ####

Il piano di ammortamento francese è caratterizzato dal pagamenti di una 
rata periodica invariata per tutta la durata del contratto.

Per il principio di chiusura finanziaria, la rata costante si determina 
rapportando il debito iniziale al fattore di valore attuale di una rendita
unitaria: R = D/("a figurato n al tasso i")

Poichè la rata è fissa e il debito residuo decresce, la quota interessi
diminuisce nel tempo, mentre la quota capitale cresce in progressione geometrica
di ragione (1+i)

STRUTTURA DELLE SCELTE
- Definizione del capitale
- Definizione del tasso di interesse annuo/periodale
- Definizione del numero di rate
'''

import pandas as pd


def ammortamento_francese(capitale: float, i: float, n: int) -> pd.DataFrame:
    """
    Calcola il piano di ammortamento alla francese e restituisce il DataFrame correlato.
    Ottimizzato per accuratezza matematica usando il calcolo diretto sul debito residuo.
    """
    # Calcolo della rata costante
    a = (1 - (1 + i)**(-n)) / i
    rata_costante = capitale / a

    # Inizializzazione vettori
    array_temporale = list(range(1, n + 1))
    array_rata = []
    array_quota_capitale = []
    array_quota_interessi = []
    array_debito_residuo = [] 

    debito_rimanente = capitale

    # Generazione dei vettori
    for k in array_temporale:
        # Calcolo quote standard (evita errori di approssimazione con potenze complesse)
        quota_interessi = debito_rimanente * i
        quota_capitale = rata_costante - quota_interessi
        
        # Aggiornamento debito
        debito_rimanente -= quota_capitale
        if abs(debito_rimanente) < 1e-9:
            debito_rimanente = 0.0
            
        array_rata.append(rata_costante)
        array_quota_capitale.append(quota_capitale)
        array_quota_interessi.append(quota_interessi)
        array_debito_residuo.append(debito_rimanente)

    return pd.DataFrame({
        'Periodo': array_temporale,
        'Rata (€)': array_rata,
        'Quota Interessi (€)': array_quota_interessi,
        'Quota Capitale (€)': array_quota_capitale,
        'Debito Residuo (€)': array_debito_residuo
    })


# DEBUG (eliminare """ """ per avviare simulazione)
"""
if __name__ == "__main__":
    cap = float(input("Inserisci il valore del finanziamento (in €): "))
    tasso = float(input("Inserisci il tasso di interesse decimale (es. 0.05 per 5%) riferito al periodo rata: "))
    rate = int(input("Inserisci il numero totale di rate: "))

    df = ammortamento_francese(cap, tasso, rate)

    print("\nDati inseriti dall'utente:")
    print(f"Finanziamento da {round(cap, 2)} €")
    print(f"Tasso di interesse (su periodo rata): {round(tasso * 100, 2)} %")
    print(f"Numero di rate: {rate}")

    interesse_totale = df['Quota Interessi (€)'].sum()
    capitale_totale = df['Quota Capitale (€)'].sum()
    pagato_totale = capitale_totale + interesse_totale

    pd.options.display.float_format = '{:,.2f}'.format
    print("\n")
    print(df.to_string(index=False)) 
        
    print("\nImpatto componenti sul totale rimborsato:")
    print(f"- Quota interessi: {interesse_totale/pagato_totale*100:.2f} %")
    print(f"- Quota capitale:  {capitale_totale/pagato_totale*100:.2f} %")
    print("\n=========================================")
"""