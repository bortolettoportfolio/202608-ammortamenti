## =============================================== ##
## =============================================== ##
##                   IMPORT                        ##
## =============================================== ##
## =============================================== ##

import os

import matplotlib.pyplot as plt
import pandas as pd

## =============================================== ##
## =============================================== ##
## DEFINIZIONI CLASSICHE DEI PIANI DI AMMORTAMENTO ##
## =============================================== ##
## =============================================== ##

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

def ammortamento_italiano(capitale: float, i: float, n: int) -> pd.DataFrame:
    """
    Calcola il piano di ammortamento italiano e restituisce un DataFrame.
    Metodo Italiano: Quota Capitale costante, Rata decrescente.
    """
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
        
        rata = quota_capitale_costante + quota_interessi
        
        # Aggiornamento debito residuo
        debito_rimanente -= quota_capitale_costante
        
        # Prevenzione float a virgola mobile errati
        if abs(debito_rimanente) < 1e-9: 
            debito_rimanente = 0.0
            
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

## =============================================== ##
## =============================================== ##
##                      PLOT                       ##
## =============================================== ##
## =============================================== ##

def pie_plot_confronto(df_francese: pd.DataFrame, df_italiano: pd.DataFrame, df_bullet: pd.DataFrame, cap: float, tasso: float, rate: int, frequenza: str, percorso_salvataggio: str = None, mostra: bool = True):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 7.5))

    cap_fr = df_francese["Quota Capitale (€)"].sum()
    int_fr = df_francese["Quota Interessi (€)"].sum()
    
    cap_it = df_italiano["Quota Capitale (€)"].sum()
    int_it = df_italiano["Quota Interessi (€)"].sum()
    
    cap_bu = df_bullet["Quota Capitale (€)"].sum()
    int_bu = df_bullet["Quota Interessi (€)"].sum()

    tot_fr = df_francese['Rata (€)'].sum()
    tot_it = df_italiano['Rata (€)'].sum()
    tot_bu = df_bullet['Rata (€)'].sum()

    per_int_fr = int_fr / tot_fr * 100
    per_int_it = int_it / tot_it * 100
    per_int_bu = int_bu / tot_bu * 100

    valori_fr = [cap_fr, int_fr]
    valori_it = [cap_it, int_it]
    valori_bu = [cap_bu, int_bu]

    def formatta_valuta(valore):
        return f"{valore:,.2f} %".replace(",", "X").replace(".", ",").replace("X", ".")

    labels_fr = ["", formatta_valuta(per_int_fr)]
    labels_it = ["", formatta_valuta(per_int_it)]
    labels_bu = ["", formatta_valuta(per_int_bu)]

    str_tot_fr = f"Totale Pagato: € {tot_fr:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    str_tot_it = f"Totale Pagato: € {tot_it:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    str_tot_bu = f"Totale Pagato: € {tot_bu:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    etichette_legenda = ["costo quota Capitale", "costo quota Interessi"]
    colori = ['#004B87', '#B32017']

    pie_kwargs = {
        'startangle': 90,
        'colors': colori,
        'labeldistance': 1.24,
        'wedgeprops': {'edgecolor': 'white', 'linewidth': 1.5},
        'textprops': {'fontsize': 13, 'fontweight': 'bold', 'color': '#111111'}
    }

    wedges, texts = ax1.pie(valori_fr, labels=labels_fr, **pie_kwargs)
    ax1.set_title("Piano alla Francese\n(Rata Costante)", fontsize=15, pad=30)
    ax1.set_xlabel(str_tot_fr, fontsize=13, bbox=dict(facecolor='#f9f9f9', edgecolor="#cccccc", boxstyle='round,pad=0.6'))


    ax2.pie(valori_it, labels=labels_it, **pie_kwargs)
    ax2.set_title("Piano all'Italiano\n(Quota Capitale Costante)", fontsize=15, pad=30)
    ax2.set_xlabel(str_tot_it, fontsize=13, bbox=dict(facecolor='#f9f9f9', edgecolor="#cccccc", boxstyle='round,pad=0.6'))

    ax3.pie(valori_bu, labels=labels_bu, **pie_kwargs)
    ax3.set_title("Piano Bullet\n(Rimborso Capitale a Scadenza)", fontsize=15, pad=30)
    ax3.set_xlabel(str_tot_bu, fontsize=13, bbox=dict(facecolor='#f9f9f9', edgecolor="#cccccc", boxstyle='round,pad=0.6'))

    fig.suptitle("Ripartizione del finanziamento nei regimi classici", fontsize=25, fontweight='bold')
    fig.set_facecolor('none')
    ax1.set_facecolor('none')
    ax2.set_facecolor('none')
    ax3.set_facecolor('none')

    fig.legend(wedges, etichette_legenda, loc='lower center', bbox_to_anchor=(0.5, 0.12), ncol=2, fontsize=15, frameon=False)


    testo_specifiche = (f"Finanziamento: {round(cap,2)} € | Frequenza pagamenti: {frequenza} | TAN (%): {round(tasso*100,2)} % | Numero rate: {rate}\n\nTasso fisso | Nessun preammortamento | Assenza del Day Count e festività")
    fig.text(0.5, 0.015, testo_specifiche, ha='center', va='bottom', fontsize=12, color='#111111', style='italic')

    plt.subplots_adjust(top=0.82, bottom=0.25, wspace=0.3)
    if percorso_salvataggio:
            plt.savefig(
                percorso_salvataggio, 
                dpi=300, 
                bbox_inches="tight", 
                format="png"
            )
        
    if mostra:
         plt.show()
            
    plt.close(fig)

def plot_confronto_decadimento(df_fr: pd.DataFrame, df_it: pd.DataFrame, df_bl: pd.DataFrame, percorso_salvataggio: str = None, mostra: bool = True):
    """
    Grafico che mostra il decadimento del debito residuo nei piani di ammortamento classici.
    """
    # Creazione tela con dimensioni standardizzate
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Titolo Globale
    fig.suptitle("Decadimento debito residuo", fontsize=25, fontweight='bold', y=0.88)
    fig.set_facecolor('none')
    ax.set_facecolor('none')

    ax.plot(df_fr['Periodo'], df_fr['Debito Residuo (€)'], label="francese", color='#117733')    
    ax.plot(df_it['Periodo'], df_it['Debito Residuo (€)'], label="italiano", color='#D55E00')    
    ax.plot(df_bl['Periodo'], df_bl['Debito Residuo (€)'], label="bullet", color='#78288C')    

    # Formattazione Assi
    ax.set_xlabel("Asse temporale ", fontsize=16, labelpad=15)
    ax.set_ylabel("Debito residuo [€]", fontsize=16, labelpad=15)
    
    ax.set_xticks(df_fr['Periodo'])
    ax.set_xticklabels([])

    
    ax.grid(axis='y', linestyle=':', color='gray', alpha=0.4)

    fig.legend(loc='lower center', 
               bbox_to_anchor=(0.5, 0.05), 
               ncol=2, 
               fontsize=15, 
               frameon=False)

    plt.tight_layout(rect=[0, 0.22, 1, 0.90])
    if percorso_salvataggio:
            plt.savefig(
                percorso_salvataggio, 
                dpi=300, 
                bbox_inches="tight", 
                format="png"
            )
        
    if mostra:
         plt.show()
            
    plt.close(fig)

## =============================================== ##
## =============================================== ##
##                      ALTRO                      ##
## =============================================== ##
## =============================================== ##

def acquisisci_input_numerico(prompt: str, tipo_dato: type):
    while True:
        valore_input = input(prompt)
        valore_input = valore_input.replace(',', '.')
        
        try:
            valore = tipo_dato(valore_input)
            if valore <= 0:
                print("Errore: Il valore deve essere strettamente maggiore di zero. Riprova.\n")
                continue
            return valore
        except ValueError:
            print(f"Errore: Formato non valido. È richiesto un dato di tipo {tipo_dato.__name__}.\n")


#####################################################
#####################################################
#####################################################
##                    MAIN                         ##
#####################################################
#####################################################
#####################################################

if __name__ == "__main__":

    ## ------------------------------------------------##
    ##         INSERIMENTO DELLE VARIABILI             ##
    ## ----------------------------------------------- ##

    cap = acquisisci_input_numerico("Inserisci valore finanziamento (in €): ", float)
    tasso = acquisisci_input_numerico("Inserisci TAN in formato decimale (es. 0.05 per 5%): ", float)
    rate = acquisisci_input_numerico("Inserisci il numero totale di rate: ", int)
    
    while True:
        tipo_piano = input("Piano (francese, italiano, bullet): ").strip().lower()
        if tipo_piano in ['francese', 'italiano', 'bullet']:
            break
        print("Errore: Piano non riconosciuto. Inserire 'francese', 'italiano' o 'bullet'.\n")

    while True:
        frequenza = input("Inserisci frequenza delle rate (tra mensile, trimestrale, semestrale e annuale): ").strip().lower()
        if frequenza in ['mensile', 'trimestrale', 'semestrale', 'annuale']:
            break
        print("Errore: Frequenza non valida. Inserire 'mensile', 'trimestrale', 'semestrale' o 'annuale'.\n")  

    ## ------------------------------------------------ ##
    ##             ELABORAZIONE DEI DATI                ##
    ## ------------------------------------------------ ##

    print("\n=========================================")
    print("=========================================")
    print("    CALCOLATORE DEL PRESTITO PERSONALE   ")
    print("==========================================\n")
    print("Dati inseriti dell'user:")
    print(f"Finanziamento da {round(cap,0)} €")
    print(f"Tasso interesse annuale (TAN) del contratto: {round(tasso*100,2)} %")
    print(f"Numero di rate: {rate}")
    print(f"Frequenza delle rate: {frequenza}\n")
    print(f"Piano da scaricare in formato csv: {tipo_piano}\n")
    pausa = input("Premi Invio per avviare l'elaborazione dei dati...")
    print("----------------------------")
    print("Elaborazione in corso...")
    print("----------------------------\n")
    
    interesse_periodo = tasso
    if frequenza == "mensile":
        interesse_periodo = tasso / 12
    elif frequenza == "trimestrale":
        interesse_periodo = tasso / 4
    elif frequenza == "semestrale":
        interesse_periodo = tasso / 2
    elif frequenza == "annuale":
        interesse_periodo = tasso
    else:
        print("Frequenza non valida. Impostata a 'annuale' per default.")
        
    piani = {
        "francese": ammortamento_francese(cap, interesse_periodo, rate),
        "italiano": ammortamento_italiano(cap, interesse_periodo, rate),
        "bullet": ammortamento_bullet(cap, interesse_periodo, rate)
    }
    
    df = piani[tipo_piano]
    
    interesse_totale = df['Quota Interessi (€)'].sum()
    capitale_totale = df['Quota Capitale (€)'].sum()
    pagato_totale = capitale_totale + interesse_totale

    ## ------------------------------------------------ ##
    ##  STAMPA A RIGA COMANDO DEI RISULTATI ESSENZIALI  ##
    ## ------------------------------------------------ ##

    pd.options.display.float_format = '{:,.2f}'.format

    print("\n----------------------------\n")
    print("Impatto componenti sul totale rimborsato:")
    print(f"- Quota interessi: {interesse_totale/pagato_totale*100:.2f} %")
    print(f"- Quota capitale:  {capitale_totale/pagato_totale*100:.2f} %\n")
    print("=========================================\n")
    print(df.to_string(index=False))
    print("\n----------------------------\n")
    print("Impatto componenti sul totale rimborsato:")
    print(f"- Quota interessi: {interesse_totale/pagato_totale*100:.2f} %")
    print(f"- Quota capitale:  {capitale_totale/pagato_totale*100:.2f} %\n")
    print("=========================================\n")
    pausa = input("Premi Invio per continuare...") 

    ## ------------------------------------------------ ##
    ##               ESPORTAZIONE ON/OFF                ##
    ## ------------------------------------------------ ##

    ## ------------------------------------------------ ##
    ##                      CSV                         ##
    ## ------------------------------------------------ ##

    salva_CSV = input(f"\nDesideri scaricare il piano selezionato ({tipo_piano}) in formato .csv? (s/n): ").strip().lower()

    if salva_CSV in ['s', 'si', 'y', 'yes']:
        nome_file = input("Inserisci il nome del file (es. X.csv) o premi Invio per default: ").strip()
        
        if not nome_file:
            nome_file = "piano_ammortamento.csv"
        elif not (nome_file.endswith(".csv")):
            nome_file += ".csv"
            
        try:
            cartella_destinazione = os.path.dirname(nome_file)
            if cartella_destinazione and not os.path.exists(cartella_destinazione):
                os.makedirs(cartella_destinazione)
            
            df.to_csv(nome_file, index=False, sep=';', decimal=',')
            
            print(f"[SUCCESSO] Esportazione dei dati csv avvenuta '{nome_file}'.")
        except Exception as e:
            print(f"[ERRORE] Impossibile salvare i dati del DataFrame: {e}")

    pausa = input("Premi Invio per continuare...")

    ## ------------------------------------------------ ##
    ##                    PNG                           ##
    ## ------------------------------------------------ ##

    # ---- GRAFICO 1: A TORTA ----
    print("\n--- GRAFICO 1: Ripartizione Costi (Torta) ---")
    mostra_PNG_1 = input("Vuoi VISUALIZZARE il grafico a schermo? (s/n): ").strip().lower() in ['s', 'si', 'y', 'yes']
    salva_PNG_1 = input("Vuoi SALVARE il grafico sul PC? (s/n): ").strip().lower() in ['s', 'si', 'y', 'yes']

    if mostra_PNG_1 or salva_PNG_1:
        percorso_completo_1 = None
        
        if salva_PNG_1:
            nome_file = input("Inserisci il nome del file (es. torta.png) o premi Invio per default: ").strip()
            if not nome_file:
                nome_file = "grafico1_torta.png"
            elif not nome_file.endswith((".png", ".jpg", ".pdf")):
                nome_file += ".png"
                

            percorso_completo_1 = os.path.join(os.getcwd(), nome_file)
            
        try:
            pie_plot_confronto(
                piani["francese"], piani["italiano"], piani["bullet"], 
                cap, tasso, rate, frequenza, 
                percorso_salvataggio=percorso_completo_1, 
                mostra=mostra_PNG_1
            )
            if salva_PNG_1:
                print(f"[SUCCESSO] Grafico 1 salvato in: {percorso_completo_1}")
        except Exception as e:
            print(f"[ERRORE] Impossibile generare il grafico 1: {e}")

    pausa = input("\nPremi Invio per passare al prossimo grafico...")


    # ---- GRAFICO 2: DECADIMENTO DEBITO ----
    print("\n--- GRAFICO 2: Decadimento Debito Residuo ---")
    mostra_PNG_2 = input("Vuoi VISUALIZZARE il grafico a schermo? (s/n): ").strip().lower() in ['s', 'si', 'y', 'yes']
    salva_PNG_2 = input("Vuoi SALVARE il grafico sul PC? (s/n): ").strip().lower() in ['s', 'si', 'y', 'yes']

    if mostra_PNG_2 or salva_PNG_2:
        percorso_completo_2 = None
        
        if salva_PNG_2:
            nome_file = input("Inserisci il nome del file (es. decadimento.png) o premi Invio per default: ").strip()
            if not nome_file:
                nome_file = "grafico2_decadimento.png"
            elif not nome_file.endswith((".png", ".jpg", ".pdf")):
                nome_file += ".png"
                

            percorso_completo_2 = os.path.join(os.getcwd(), nome_file)
            
        try:
            plot_confronto_decadimento(
                piani["francese"], piani["italiano"], piani["bullet"], 
                percorso_salvataggio=percorso_completo_2, 
                mostra=mostra_PNG_2
            )
            if salva_PNG_2:
                print(f"[SUCCESSO] Grafico 2 salvato in: {percorso_completo_2}")
        except Exception as e:
            print(f"[ERRORE] Impossibile generare il grafico 2: {e}")