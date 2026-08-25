import os

import pandas as pd
import matplotlib.pyplot as plt


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



def acquisisci_input_numerico(prompt: str, tipo_dato: type):
    """
    Gestisce l'acquisizione dell'input da terminale forzando un tipo di dato
    e richiedendo valori strettamente positivi.
    """
    while True:
        valore_input = input(prompt)
        # Sostituisce l'eventuale virgola usata per i decimali con il punto
        valore_input = valore_input.replace(',', '.')
        
        try:
            valore = tipo_dato(valore_input)
            if valore <= 0:
                print("Errore: Il valore deve essere strettamente maggiore di zero. Riprova.\n")
                continue
            return valore
        except ValueError:
            print(f"Errore: Formato non valido. È richiesto un dato di tipo {tipo_dato.__name__}.\n")

def confronta_torte_ammortamento_completo(df_francese, df_italiano, df_bullet):
    """
    Genera tre grafici a torta affiancati senza etichette individuali, 
    utilizzando una singola legenda globale centralizzata con layout ottimizzato.
    """
    # 1. Creazione della matrice spaziale 1x3
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 7))
    
    # 2. Estrazione dati finanziari aggregati
    valori_fr = [df_francese["Quota Capitale (€)"].sum(), df_francese["Quota Interessi (€)"].sum()]
    valori_it = [df_italiano["Quota Capitale (€)"].sum(), df_italiano["Quota Interessi (€)"].sum()]
    valori_bu = [df_bullet["Quota Capitale (€)"].sum(), df_bullet["Quota Interessi (€)"].sum()]
    
    # 3. Calcolo e formattazione dei totali per i label inferiori
    tot_fr = df_francese['Rata (€)'].sum()
    tot_it = df_italiano['Rata (€)'].sum()
    tot_bu = df_bullet['Rata (€)'].sum()
    
    str_tot_fr = f"Totale Pagato: € {tot_fr:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    str_tot_it = f"Totale Pagato: € {tot_it:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    str_tot_bu = f"Totale Pagato: € {tot_bu:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    etichette = ["Quota Capitale", "Quota Interessi"]
    
    # Ripristino Palette Istituzionale (Nessun Arancione)
    colori = ['#BDE0FE', '#FFC8DD'] 
    
    # Dizionario tipografico per ingrandire i font interni delle percentuali
    font_percentuali = {'fontsize': 14, 'fontweight': 'medium'}
    
    # ==========================================
    # PLOT 1: Ammortamento Francese
    # ==========================================
    wedges, texts, autotexts = ax1.pie(valori_fr, 
                                       autopct='%1.2f%%', 
                                       startangle=90, 
                                       colors=colori,
                                       wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
                                       textprops=font_percentuali)
    ax1.set_title("Piano alla Francese\n(Rata Costante)", fontsize=14, pad=15)
    ax1.set_xlabel(str_tot_fr, fontsize=13, 
                   bbox=dict(facecolor='#f9f9f9', edgecolor="#cccccc", boxstyle='round,pad=0.6'))
    
    # ==========================================
    # PLOT 2: Ammortamento Italiano
    # ==========================================
    ax2.pie(valori_it, 
            autopct='%1.2f%%', 
            startangle=90, 
            colors=colori,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
            textprops=font_percentuali)
    ax2.set_title("Piano all'Italiano\n(Quota Capitale Costante)", fontsize=14, pad=15)
    ax2.set_xlabel(str_tot_it, fontsize=13,
                   bbox=dict(facecolor='#f9f9f9', edgecolor="#cccccc", boxstyle='round,pad=0.6'))

    # ==========================================
    # PLOT 3: Ammortamento Bullet
    # ==========================================
    ax3.pie(valori_bu, 
            autopct='%1.2f%%', 
            startangle=90, 
            colors=colori,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
            textprops=font_percentuali)
    ax3.set_title("Piano Bullet\n(Rimborso Capitale a Scadenza)", fontsize=14, pad=15)
    ax3.set_xlabel(str_tot_bu, fontsize=13, 
                   bbox=dict(facecolor='#f9f9f9', edgecolor="#cccccc", boxstyle='round,pad=0.6'))
    
    # ==========================================
    # LEGENDA E TITOLO GLOBALE
    # ==========================================
    fig.suptitle("Componente capitale vs componente interessi totale", fontsize=18, fontweight='bold')

    # MODIFICA SPAZIALE 1: Legenda abbassata al 7% dell'altezza (y=0.07)
    fig.legend(wedges, etichette, 
               loc='lower center', 
               bbox_to_anchor=(0.5, 0.07), 
               ncol=2, 
               fontsize=13, 
               frameon=False)

    testo_specifiche = (
        "Note Metodologiche: Analisi comparativa basata sulle quote aggregate dell'intero piano.\n"
        "Tasso fisso | Capitalizzazione composta | Nessun preammortamento."
    )
    
    # MODIFICA SPAZIALE 2: Testo abbassato all'1% dell'altezza (y=0.01)
    fig.text(0.5, 0.01, testo_specifiche, 
             ha='center',       
             va='bottom',       
             fontsize=12, 
             color='#555555',   
             style='italic')
    
    # MODIFICA SPAZIALE 3: Margine inferiore riservato aumentato al 22% (bottom=0.22)
    # Questo comprime leggermente i grafici verso l'alto, distanziando i ticket dalla legenda.
    plt.tight_layout(rect=[0, 0.22, 1, 0.85])
    
    # ==========================================
    # LOGICA DI SALVATAGGIO
    # ==========================================
    salva = input("\nDesideri esportare il grafico come immagine? (s/n): ").strip().lower()
    if salva in ['s', 'si', 'y', 'yes']:
        nome_file = input("Inserisci il nome del file (es. grafico.png) o premi Invio per default: ").strip()
        
        if not nome_file:
            nome_file = "grafico.png"
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
    print("   CONFRONTO STRUTTURA PIANI AMMORTAMENTO CLASSICI  ")
    print("=========================================\n")
    
    # Acquisizione sicura dei dati
    cap = acquisisci_input_numerico("Inserisci il capitale da finanziare (in €): ", float)
    tasso = acquisisci_input_numerico("Inserisci il tasso di interesse decimale (es. 0.05 per 5%): ", float)
    rate = acquisisci_input_numerico("Inserisci il numero totale di rate: ", int)
    
    print("\nElaborazione in corso...\n")

    df_fr = ammortamento_francese(cap, tasso, rate)
    df_it = ammortamento_italiano(cap, tasso, rate)
    df_bu = ammortamento_bullet(cap, tasso, rate)

    confronta_torte_ammortamento_completo(df_fr, df_it, df_bu)
