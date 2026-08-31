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
import os

import matplotlib.pyplot as plt
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


def acquisisci_input_numerico(prompt: str, tipo_dato: type):
    """
    Gestisce l'acquisizione dell'input da terminale forzando un tipo di dato
    e richiedendo valori strettamente positivi.
    """
    while True:
        valore_input = input(prompt).replace(',', '.')
        try:
            valore = tipo_dato(valore_input)
            if valore <= 0:
                print("Errore: Il valore deve essere strettamente maggiore di zero. Riprova.\n")
                continue
            return valore
        except ValueError:
            print(f"Errore: Formato non valido. È richiesto un dato di tipo {tipo_dato.__name__}.\n")


def gestisci_grafico(df: pd.DataFrame, cap: float, tasso: float, rate: int):
    """
    Genera il grafico a barre impilate dal DataFrame e gestisce il salvataggio su file,
    applicando gli standard visivi e strutturali del framework.
    """
    # Creazione tela con dimensioni standardizzate
    fig, ax = plt.subplots(figsize=(12, 7))

    # Titolo Globale
    fig.suptitle("Piano di Ammortamento a Rate Costanti (Francese)", fontsize=25, fontweight='bold', y=0.88)

    #  Generazione del Bar Plot Impilato
    bars_cap = ax.bar(df['Periodo'], df['Quota Capitale (€)'], color='#FD9F89', label="Quota Capitale", width=0.8)
    bars_int = ax.bar(df['Periodo'], df['Quota Interessi (€)'], bottom=df['Quota Capitale (€)'], color='#648C87', label="Quota Interessi", width=0.8)
    
    # Formattazione Assi
    ax.set_xlabel("Numero Rata", fontsize=18, labelpad=15)
    ax.set_ylabel("Valore della Rata [€]", fontsize=18, labelpad=15)
    
    ax.set_xticks(df['Periodo'])
    ax.tick_params(axis='both', pad=10)
    
    ax.grid(axis='y', linestyle=':', color='gray', alpha=0.4)

    # Formattazione legenda
    fig.legend([bars_cap, bars_int], ["Quota Capitale", "Quota Interessi"], 
               loc='lower center', 
               bbox_to_anchor=(0.5,0.12), 
               ncol=2, 
               fontsize=15, 
               frameon=False)

    # Eventuale testo aggiuntivo da inserire a fine del grafico :)
    testo_specifiche = (f"Dati della simulazione ⟶ Finanziamento: {round(cap,2)} €;  Interesse su periodo: {round(tasso*100,2)} %;  Numero periodi: {rate}")

    fig.text(0.5, 0.085, testo_specifiche, 
             ha='center',       
             va='bottom',       
             fontsize=12, 
             color='#666666',   
             style='italic')
    
    plt.tight_layout(rect=[0, 0.22, 1, 0.90])

    # Logica di esportazione
    salva = input("\nDesideri esportare il grafico come immagine? (s/n): ").strip().lower()
    if salva in ['s', 'si', 'y', 'yes']:
        nome_file = input("Inserisci il nome del file (es. grafico.png) o premi Invio per default: ").strip()
        
        if not nome_file:
            nome_file = "grafico_ammortamento.png"
        elif not (nome_file.endswith(".png") or nome_file.endswith(".jpg") or nome_file.endswith(".pdf")):
            nome_file += ".png"
            
        try:
            cartella_destinazione = os.path.dirname(nome_file)
            if cartella_destinazione and not os.path.exists(cartella_destinazione):
                os.makedirs(cartella_destinazione)
                
            plt.savefig(nome_file, dpi=300, bbox_inches='tight')
            print(f"[SUCCESSO] Grafico esportato correttamente in '{nome_file}'.")
        except Exception as e:
            print(f"[ERRORE] Impossibile salvare il grafico: {e}")

    print("\nChiusura della finestra del grafico in corso... (Chiudi la finestra per terminare il programma)")
    plt.show()


if __name__ == "__main__":
    print("=========================================")
    print("   CALCOLO AMMORTAMENTO ALLA FRANCESE    ")
    print("=========================================\n")
    
    # Acquisizione sicura dei dati
    cap = acquisisci_input_numerico("Inserisci valore finanziamento (in €): ", float)
    tasso = acquisisci_input_numerico("Inserisci il tasso di interesse decimale (es. 0.05 per 5%) riferito al periodo rata: ", float)
    rate = acquisisci_input_numerico("Inserisci il numero totale di rate: ", int)

    print()
    print("----------------------------")
    print("\nElaborazione in corso...\n")
    print("----------------------------")
    print()

    # Generazione del DataFrame
    df_ammortamento = ammortamento_francese(cap, tasso, rate)
    interesse_totale = df_ammortamento['Quota Interessi (€)'].sum()
    capitale_totale = df_ammortamento['Quota Capitale (€)'].sum()
    pagato_totale = capitale_totale + interesse_totale
    
    # Stampa a video
    pd.options.display.float_format = '{:,.2f}'.format
    """
    print(df_ammortamento.to_string(index=False)) 
    """
    print("Impatto componenti rata:")
    print(f"- quota interessi: {interesse_totale/pagato_totale*100:.2f} %")
    print(f"- quota capitale: {capitale_totale/pagato_totale*100:.2f} %")
    print("\n=========================================")
    
    # Esportazione in formato .csv
    salva_csv = input("Desideri esportare la tabella in formato CSV? (s/n): ").strip().lower()
    if salva_csv in ['s', 'si', 'y', 'yes']:
        nome_file_csv = input("Inserisci il nome del file (es. ammortamento.csv) o premi Invio per default: ").strip()
        
        if not nome_file_csv:
            nome_file_csv = "piano_ammortamento.csv"
        elif not nome_file_csv.endswith(".csv"):
            nome_file_csv += ".csv"
            
        try:
            cartella_destinazione_csv = os.path.dirname(nome_file_csv)
            if cartella_destinazione_csv and not os.path.exists(cartella_destinazione_csv):
                os.makedirs(cartella_destinazione_csv)

            df_ammortamento.to_csv(
                nome_file_csv, 
                index=False, 
                sep=';', 
                decimal=',',
                encoding='utf-8-sig'
            )
            print(f"[SUCCESSO] File '{nome_file_csv}' esportato correttamente.")
        except PermissionError:
            print(f"[ERRORE] Permesso negato. Assicurati che '{nome_file_csv}' non sia aperto in altri programmi.")
        except Exception as e:
            print(f"[ERRORE CRITICO] Impossibile salvare il file CSV: {e}")

    # Gestione Grafico
    mostra_grafico = input("\nDesideri visualizzare l'andamento delle quote in un grafico? (s/n): ").strip().lower()
    if mostra_grafico in ['s', 'si', 'y', 'yes']:
        gestisci_grafico(df_ammortamento, cap, tasso, rate)