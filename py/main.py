import pandas as pd
from bar_struttura_rata import bar_plot_inpila
from bullet import ammortamento_bullet
from francese import ammortamento_francese
from italiano import ammortamento_italiano
from pie_plot_piani import pie_plot_confronto
from plot_decadimento_debito import plot_confronto_decadimento


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

if __name__ == "__main__":

    cap = acquisisci_input_numerico("Inserisci valore finanziamento (in €): ", float)
    tasso = acquisisci_input_numerico("Inserisci il tasso di interesse decimale (es. 0.05 per 5%) riferito al periodo rata: ", float)
    rate = acquisisci_input_numerico("Inserisci il numero totale di rate: ", int)
    tipo_piano = input("Piano (Francese, Italiano, Bullet): ").strip().capitalize()

    print("=========================================")
    print("    CALCOLATORE DEL PRESTITO PERSONALE   ")
    print("==========================================\n")
    # Qua verranno visualizzate le variabili della simulazione
    print("Dati inseriti dell'user:")
    print(f"Finanziamento da {round(cap,0)} €")
    print(f"Tasso di interesse annuale (TAN) da contratto: {round(tasso,2)*100} ")
    print(f"Numero di rate: {rate}")
    print(f"Piano da scaricare in formato csv: {tipo_piano}\n")

    print("----------------------------")
    print("Elaborazione in corso...")
    print("----------------------------\n")

    if tipo_piano == "Francese":
        df = ammortamento_francese(cap, tasso, rate)
    elif tipo_piano == "Italiano":
        df = ammortamento_italiano(cap, tasso, rate)
    elif tipo_piano == "Bullet":
        df = ammortamento_bullet(cap, tasso, rate)
    else:
        print("Errore: Piano non riconosciuto. Uscita.")

    
    interesse_totale = df['Quota Interessi (€)'].sum()
    capitale_totale = df['Quota Capitale (€)'].sum()
    pagato_totale = capitale_totale + interesse_totale

    # Formattazione e output del piano ammortamento
    pd.options.display.float_format = '{:,.2f}'.format
    print("\n")
    print(df.to_string(index=False)) 
    print("----------------------------\n")
    print("Impatto componenti sul totale rimborsato:")
    print(f"- Quota interessi: {interesse_totale/pagato_totale*100:.2f} %")
    print(f"- Quota capitale:  {capitale_totale/pagato_totale*100:.2f} %\n")
    print("=========================================\n")

    # Finalmente i grafici :)
    # per la tipologia di piano selezionata
    bar_plot_inpila(df, cap, tasso, rate)
    
    ## per il confronto tra i piani classici
    fr = ammortamento_francese(cap, tasso, rate)
    ita = ammortamento_italiano(cap, tasso, rate)
    bul = ammortamento_bullet(cap, tasso, rate)
    pie_plot_confronto(fr, ita, bul, cap, tasso, rate)
    plot_confronto_decadimento(df, cap, tasso, rate)