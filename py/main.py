## =============================================== ##
##                   IMPORT                        ##
## =============================================== ##
import os
import subprocess

import matplotlib.pyplot as plt
import pandas as pd

## +++++++++++++++++++++++++++++++++++++++++++++++ ##
## +++++++++++++++++++++++++++++++++++++++++++++++ ##
## DEFINIZIONI CLASSICHE DEI PIANI DI AMMORTAMENTO ##
## +++++++++++++++++++++++++++++++++++++++++++++++ ##
## +++++++++++++++++++++++++++++++++++++++++++++++ ##

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

## +++++++++++++++++++++++++++++++++++++++++++++++ ##
## +++++++++++++++++++++++++++++++++++++++++++++++ ##
##                      PLOT                       ##
## +++++++++++++++++++++++++++++++++++++++++++++++ ##
## +++++++++++++++++++++++++++++++++++++++++++++++ ##

def pie_plot_confronto(df_francese: pd.DataFrame, df_italiano: pd.DataFrame, df_bullet: pd.DataFrame,
                       cap: float, tasso: float, rate: int, frequenza: str,
                       percorso_salvataggio: str | None = None,
                       show: bool = True):

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
    colori = ['#648fff', '#fe6100']

    pie_kwargs = {
        'startangle': 90,
        'colors': colori,
        'labeldistance': 1.24,
        'wedgeprops': {'edgecolor': 'white', 'linewidth': 1.5},
        'textprops': {'fontsize': 13, 'fontweight': 'bold', 'color': '#111111'}
    }

    wedges, _ = ax1.pie(valori_fr, labels=labels_fr, **pie_kwargs)
    ax1.set_title("Piano alla Francese\n(Rata Costante)", fontsize=15, pad=30)
    ax1.set_xlabel(str_tot_fr, fontsize=13, bbox={'facecolor': '#f9f9f9', 'edgecolor': '#cccccc', 'boxstyle': 'round,pad=0.6'})


    ax2.pie(valori_it, labels=labels_it, **pie_kwargs)
    ax2.set_title("Piano all'Italiano\n(Quota Capitale Costante)", fontsize=15, pad=30)
    ax2.set_xlabel(str_tot_it, fontsize=13, bbox={'facecolor': '#f9f9f9', 'edgecolor': '#cccccc', 'boxstyle': 'round,pad=0.6'})

    ax3.pie(valori_bu, labels=labels_bu, **pie_kwargs)
    ax3.set_title("Piano Bullet\n(Rimborso Capitale a Scadenza)", fontsize=15, pad=30)
    ax3.set_xlabel(str_tot_bu, fontsize=13, bbox={'facecolor': '#f9f9f9', 'edgecolor': '#cccccc', 'boxstyle': 'round,pad=0.6'})

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
        
    if show:
         plt.show()
            
    plt.close(fig)

def plot_confronto_decadimento(df_fr: pd.DataFrame, df_it: pd.DataFrame, df_bl: pd.DataFrame,
                               percorso_salvataggio: str | None = None,
                               show: bool = True):
    """
    Grafico che mostra il decadimento del debito residuo nei piani di ammortamento classici.
    """
    fig, ax = plt.subplots(figsize=(14, 7.5))

    
    fig.suptitle("Decadimento debito residuo", fontsize=25, fontweight='bold', y=0.88)
    fig.set_facecolor('none')
    ax.set_facecolor('none')


    ax.plot(df_fr['Periodo'], df_fr['Debito Residuo (€)'], label="Francese", color='#ffb000')    
    ax.plot(df_it['Periodo'], df_it['Debito Residuo (€)'], label="Italiano", color='#648fff')    
    ax.plot(df_bl['Periodo'], df_bl['Debito Residuo (€)'], label="Bullet", color='#dc267f')    


    ax.set_xlabel("Asse temporale ", fontsize=14, labelpad=14)
    ax.set_ylabel("Debito residuo [€]", fontsize=14, labelpad=14)
    
    ax.set_xticks(df_fr['Periodo'])
    ax.set_xticklabels([])

    
    ax.grid(axis='y', linestyle=':', color='gray', alpha=0.35)

    fig.legend(loc='lower center', 
               bbox_to_anchor=(0.5, 0.05), 
               ncol=2, 
               fontsize=16, 
               frameon=False)

    plt.tight_layout(rect=[0, 0.22, 1, 0.90])
    if percorso_salvataggio:
            plt.savefig(
                percorso_salvataggio, 
                dpi=300, 
                bbox_inches="tight", 
                format="png"
            )
        
    if show:
         plt.show()
            
    plt.close(fig)

## +++++++++++++++++++++++++++++++++++++++++++++++ ##
## +++++++++++++++++++++++++++++++++++++++++++++++ ##
##                      ALTRO                      ##
## +++++++++++++++++++++++++++++++++++++++++++++++ ##
## +++++++++++++++++++++++++++++++++++++++++++++++ ##

def pulisci_schermo():
    comando = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run(comando, shell=True, check=False)

def cancella_ultima_riga():
    print("\033[F\033[K", end="")


def stampa_intestazione_iniziale(cap : int, tasso: float, rate : int, frequenza : str, tipo_piano : str):
    print("=" * 60)
    print()
    print(" CALCOLATORE DEL PRESTITO PERSONALE ".center(60))
    print()
    print("-" * 60)
    print(f"\n Finanziamento: {cap:,.2f} € | TAN: {tasso*100:.2f} %")
    print(f" Rate: {rate} ({frequenza}) | Piano: {tipo_piano.upper()}")
    print(" In costruzione: min e massimo dei piani")
    print()
    print("-" * 60)
    print()
    print("Assenza del Day Count e festività | Tasso fisso ")
    print("Nessun preammortamento")
    print()
    print("=" * 60)
    print()

def stampa_intestazione_finale(cap : int, tasso: float, rate : int, frequenza : str, tipo_piano : str,
                               csv: bool = False, png1: bool = False, png2: bool = False):
    print("=" * 60)
    print()
    print(" CALCOLATORE DEL PRESTITO PERSONALE ".center(60))
    print()
    print("-" * 60)
    print(f"\n Finanziamento: {cap:,.2f} € | TAN: {tasso*100:.2f} %")
    print(f" Rate: {rate} ({frequenza}) | Piano: {tipo_piano.upper()}")
    print(" In costruzione: min e massimo dei piani")
    print()
    print("-" * 60)
    print()
    print("Assenza del Day Count e festività | Tasso fisso ")
    print("Nessun preammortamento")
    print()
    print("-" * 60)
    print()
    if csv == False:
        print("Esportazione CSV: NO")
    else:
        print("Esportazione CSV: SI")
    if png1 == False:
        print("Esportazione PNG 1: NO")
    else:
        print("Esportazione PNG 1: SI")
    if png2 == False:
        print("Esportazione PNG 2: NO")
    else:
        print("Esportazione PNG 2: SI")
    print()
    print("=" * 60)


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

    pulisci_schermo()
    print("=" * 60)
    print("INSERIMENTO DATI SIMULAZIONE".center(60))
    print("=" * 60)
    print()
    ## ------------------------------------------------##
    ##         INSERIMENTO DELLE VARIABILI             ##
    ## ----------------------------------------------- ##
    cap = acquisisci_input_numerico("Inserire valore finanziamento (presunto in €): ", float)
    cancella_ultima_riga()
    tasso = acquisisci_input_numerico("Inserire TAN in formato decimale (es. 0.05 per 5%): ", float)
    cancella_ultima_riga()
    rate = acquisisci_input_numerico("Inserire il numero totale delle rate: ", int)
    cancella_ultima_riga()
    while True:
        tipo_piano = input("Quale piano vorresti simulare a schermo? (tra: francese, italiano, bullet): ").strip().lower()   
        if tipo_piano in ['francese', 'italiano', 'bullet']:
            break
    cancella_ultima_riga()
    while True:
        frequenza = input("Inserire la frequenza delle rate (tra: mensile, trimestrale, semestrale e annuale): ").strip().lower()
        if frequenza in ['mensile', 'trimestrale', 'semestrale', 'annuale']:
            break
    cancella_ultima_riga()

    pausa = input("PREMERE INVIO PER PROCEDERE...")
    cancella_ultima_riga()

    ## ------------------------------------------------ ##
    ##             ELABORAZIONE DEI DATI                ##
    ## ------------------------------------------------ ##

    interesse = tasso
    if frequenza == "mensile":
        interesse = tasso / 12
    elif frequenza == "trimestrale":
        interesse = tasso / 4
    elif frequenza == "semestrale":
        interesse = tasso / 2
    elif frequenza == "annuale":
        interesse = tasso
    else:
        print("Frequenza non valida. Impostata a 'annuale' per default.")
        
    piani = {
        "francese": ammortamento_francese(cap, interesse, rate),
        "italiano": ammortamento_italiano(cap, interesse, rate),
        "bullet": ammortamento_bullet(cap, interesse, rate)
    }
    
    df = piani[tipo_piano]
    
    interesse_totale = df['Quota Interessi (€)'].sum()
    capitale_totale = df['Quota Capitale (€)'].sum()
    pagato_totale = capitale_totale + interesse_totale

    ## ------------------------------------------------ ##
    ##  STAMPA A RIGA COMANDO DEI RISULTATI ESSENZIALI  ##
    ## ------------------------------------------------ ##

    pd.options.display.float_format = '{:,.2f}'.format

    pulisci_schermo()
    stampa_intestazione_iniziale(cap, tasso, rate, frequenza, tipo_piano)

    print(df.to_string(index=False))

    print("\nImpatto componenti sul totale rimborsato:")
    print(f"- Quota interessi: {interesse_totale/pagato_totale*100:.2f} %")
    print(f"- Quota capitale:  {capitale_totale/pagato_totale*100:.2f} %")
    print("\n" + "-" * 60)
    input("PREMERE INVIO PER PROCEDERE CON LE SCELTE DI ESPORTAZIONE...")
    pulisci_schermo()

    stampa_intestazione_iniziale(cap, tasso, rate, frequenza, tipo_piano)

    ## ------------------------------------------------ ##
    ##            ESPORTAZIONE CSV (facoltativo)        ##
    ## ------------------------------------------------ ##

    salva_CSV = input(f"Scaricare piano selezionato ({tipo_piano}) in formato .csv? (s/n): ").strip().lower()
    cancella_ultima_riga()
    if salva_CSV in ['s', 'si', 'y', 'yes']:
        nome_file = input("Nome file (es. piano.csv) o Invio per default:  ").strip()
        salva_CSV = True
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
        except OSError as e:
            print(f"[ERRORE] Impossibile salvare i dati del DataFrame: {e}")
    else:
        salva_CSV = False

    ## ------------------------------------------------ ##
    ##                    PNG                           ##
    ## ------------------------------------------------ ##

    # ---- GRAFICO 1: A TORTA ----
    print("-----------------------------------------")
    print("- GRAFICO 1: Ripartizione Costi (Torta) -")
    print("-----------------------------------------")
    print()
    mostra_PNG_1 = input("Visualizzare a schermo? (s/n): ").strip().lower() in ['s', 'si', 'y', 'yes']
    cancella_ultima_riga()
    salva_PNG_1 = input("Salvare sul PC? (s/n): ").strip().lower() in ['s', 'si', 'y', 'yes']
    cancella_ultima_riga()
    if mostra_PNG_1:
        mostra_PNG_1 = True
    else:
        mostra_PNG_1 = False
    
    if mostra_PNG_1 or salva_PNG_1:
        percorso_completo_1 = None
        
        if salva_PNG_1:
            nome_file = input("Inserisci il nome del file (es. torta.png) o premi Invio per default: ").strip()
            cancella_ultima_riga()
            salva_PNG_1 = True
            if not nome_file:
                nome_file = "grafico1_torta.png"
            elif not nome_file.endswith((".png", ".jpg", ".pdf")):
                nome_file += ".png"
                

            percorso_completo_1 = os.path.join(os.getcwd(), nome_file)
        else:
            salva_PNG_1 = False
           
        try:
            pie_plot_confronto(
                piani["francese"], piani["italiano"], piani["bullet"], 
                cap, tasso, rate, frequenza, 
                percorso_salvataggio=percorso_completo_1, 
                show=mostra_PNG_1
            )
            if salva_PNG_1:
                print(f"[SUCCESSO] Grafico 1 salvato in: {percorso_completo_1}")
        except OSError as e:
            print(f"[ERRORE] Impossibile generare il grafico 1: {e}")

    pausa = input("\nPremi Invio per passare al prossimo grafico...")

    pulisci_schermo()
    stampa_intestazione_iniziale(cap, tasso, rate, frequenza, tipo_piano)

    # ---- GRAFICO 2: DECADIMENTO DEBITO ----
    print("-----------------------------------------")
    print("- GRAFICO 2: Decadimento Debito Residuo -")
    print("-----------------------------------------")
    print()
    mostra_PNG_2 = input("Visualizzare a schermo? (s/n): ").strip().lower() in ['s', 'si', 'y', 'yes']
    cancella_ultima_riga()
    salva_PNG_2 = input("Salvare sul PC? (s/n): ").strip().lower() in ['s', 'si', 'y', 'yes']
    cancella_ultima_riga()
    if mostra_PNG_2:
        mostra_PNG_2 = True
    else:
        mostra_PNG_2 = False
    
    if mostra_PNG_2 or salva_PNG_2:
        percorso_completo_2 = None
        
        if salva_PNG_2:
            salva_PNG_2 = True
            nome_file = input("Inserisci il nome del file (es. decadimento.png) o premi Invio per default: ").strip()
            cancella_ultima_riga()
            if not nome_file:
                nome_file = "grafico2_decadimento.png"
            elif not nome_file.endswith((".png", ".jpg", ".pdf")):
                nome_file += ".png"
                

            percorso_completo_2 = os.path.join(os.getcwd(), nome_file)
        else:
            salva_PNG_2 = False   
        try:
            plot_confronto_decadimento(
                piani["francese"], piani["italiano"], piani["bullet"], 
                percorso_salvataggio=percorso_completo_2, 
                show=mostra_PNG_2
            )
            if salva_PNG_2:
                print(f"[SUCCESSO] Grafico 2 salvato in: {percorso_completo_2}")
        except OSError as e:
            print(f"[ERRORE] Impossibile generare il grafico 2: {e}")

    pulisci_schermo()
    print("Elaborazione completata.\n")     
    stampa_intestazione_finale(cap, tasso, rate, frequenza, tipo_piano,
                                 csv=salva_CSV, png1=salva_PNG_1, png2=salva_PNG_2)
    