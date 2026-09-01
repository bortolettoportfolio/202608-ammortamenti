'''
##### DEFINIZIONE AMMORTAMENTO BULLET ####
'''

import pandas as pd


def ammortamento_bullet(capitale: float, i_annuo: float, n: int) -> pd.DataFrame:
    """
    Calcola il piano di ammortamento Bullet e restituisce un DataFrame strutturato.
    """
    array_temporale = list(range(1, n + 1))
    array_rata = []
    array_quota_capitale = []
    array_quota_interessi = []
    array_debito_residuo = []
    
    for k in array_temporale:
        # La quota interessi è fissa su tutto il periodo perché il debito residuo non scala
        quota_interessi = capitale * i_annuo
        array_quota_interessi.append(quota_interessi)
        
        # Gestione della quota capitale (zero fino all'ultima rata)
        if k < n:
            quota_capitale = 0.0
            debito_rimanente = capitale
        else:
            # Ultima rata: rimborso integrale del capitale
            quota_capitale = capitale
            debito_rimanente = 0.0
            
        array_quota_capitale.append(quota_capitale)
        
        # La rata è la somma matematica delle due quote nel periodo corrente
        rata = quota_capitale + quota_interessi
        array_rata.append(rata)
        
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

    df = ammortamento_bullet(cap, tasso, rate)

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