'''
##### DEFINIZIONE AMMORTAMENTO ITALIANO ####
'''

import pandas as pd


def ammortamento_italiano(capitale: float, i: float, n: int) -> pd.DataFrame:
    """
    Calcola il piano di ammortamento italiano e restituisce un DataFrame.
    Metodo Italiano: Quota Capitale costante, Rata decrescente.
    """
    # 1. CORREZIONE MATEMATICA: La quota capitale è costante (Capitale / Numero Rate)
    quota_capitale_costante = capitale / n
    
    array_temporale = list(range(1, n + 1))
    array_rata = []
    array_quota_capitale = []
    array_quota_interessi = []
    array_debito_residuo = []
    
    debito_rimanente = capitale
    
    for k in array_temporale:
        # Calcolo interessi (sul debito residuo del periodo precedente)
        quota_interessi = debito_rimanente * i
        
        # 2. CORREZIONE STRUTTURALE: Calcolo della rata (variabile e decrescente)
        rata = quota_capitale_costante + quota_interessi
        
        # Aggiornamento debito residuo
        debito_rimanente -= quota_capitale_costante
        
        # Prevenzione float a virgola mobile errati
        if abs(debito_rimanente) < 1e-9: 
            debito_rimanente = 0.0
            
        # 3. CORREZIONE LOGICA: Un singolo append per ogni array
        array_rata.append(rata)
        array_quota_capitale.append(quota_capitale_costante)
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

    df = ammortamento_italiano(cap, tasso, rate)

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