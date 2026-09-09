import os

import pandas as pd
from bar_struttura_rata import bar_plot_inpila
from bullet import ammortamento_bullet
from francese import ammortamento_francese
from italiano import ammortamento_italiano
from pie_plot_piani import pie_plot_confronto
from plot_decadimento_debito import plot_confronto_decadimento


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

if __name__ == "__main__":

    cap = acquisisci_input_numerico("Inserisci valore finanziamento (in €): ", float)
    tasso = acquisisci_input_numerico("Inserisci TAN in formato decimale (es. 0.05 per 5%): ", float)
    rate = acquisisci_input_numerico("Inserisci il numero totale di rate: ", int)
    
    while True:
        tipo_piano = input("Piano (francese, italiano, bullet): ").strip().lower()
        if tipo_piano in ['francese', 'italiano', 'bullet']:
            break
        print("Errore: Piano non riconosciuto. Inserire 'francese', 'italiano' o 'bullet'.\n")
        
    frequenza = input("Inserisci frequenza delle rate (tra mensile, trimestrale, semestrale e annuale): ").strip().lower()

    print("\n=========================================")
    print("=========================================")
    print("    CALCOLATORE DEL PRESTITO PERSONALE   ")
    print("==========================================\n")
    print("Dati inseriti dell'user:")
    print(f"Finanziamento da {round(cap,0)} €")
    print(f"Tasso di interesse annuale (TAN) da contratto: {round(tasso,2)*100} ")
    print(f"Numero di rate: {rate}")
    print(f"Frequenza delle rate: {frequenza}\n")
    print(f"Piano da scaricare in formato csv: {tipo_piano}\n")

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

    pd.options.display.float_format = '{:,.2f}'.format
    print("\n")
    print(df.to_string(index=False)) 
    print("----------------------------\n")
    print("Impatto componenti sul totale rimborsato:")
    print(f"- Quota interessi: {interesse_totale/pagato_totale*100:.2f} %")
    print(f"- Quota capitale:  {capitale_totale/pagato_totale*100:.2f} %\n")
    print("=========================================\n")

    salva = input("\nDesideri scaricare il piano selezionato in formato .csv? (s/n): ").strip().lower()
    if salva in ['s', 'si', 'y', 'yes']:
        nome_file = input("Inserisci il nome del file (es. piano_ammortamento.csv) o premi Invio per default: ").strip()
        
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

    bar_plot_inpila(df)

    pie_plot_confronto(piani["francese"], piani["italiano"], piani["bullet"], cap, tasso, rate, frequenza)
    
    plot_confronto_decadimento(piani["francese"], piani["italiano"], piani["bullet"])