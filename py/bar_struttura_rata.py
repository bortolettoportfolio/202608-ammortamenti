import os

import matplotlib.pyplot as plt
import pandas as pd

"""
Generazione del plot per la visualizzazione temporale della struttura della rata (colonne in pila)

"""

def bar_plot_inpila(df: pd.DataFrame):
    """
    Genera il grafico a barre impilate del DataFrame e gestisce il salvataggio su file,
    applicando gli standard visivi e strutturali del framework.
    """
    # Tela
    fig, ax = plt.subplots(figsize=(12, 7))
    fig.set_facecolor('none')
    ax.set_facecolor('none')

    # Bar Plot Impilato
    bars_cap = ax.bar(df['Periodo'], df['Quota Capitale (€)'], color='#C0C0C0', label="Quota Capitale", width=0.8)
    bars_int = ax.bar(df['Periodo'], df['Quota Interessi (€)'], bottom=df['Quota Capitale (€)'], color='#B32017', label="Quota Interessi", width=0.8)
    
    # Formattazione Assi
    ax.set_xlabel("Periodo", fontsize=16, labelpad=10)
    ax.set_ylabel("Valore della Rata [€]", fontsize=16, labelpad=15)
    
    ax.set_xticks(df['Periodo'])
    ax.set_xticklabels([])

    ax.grid(axis='y', linestyle=':', color='gray', alpha=0.4)

    # Formattazione legenda
    fig.legend([bars_cap, bars_int], ["Quota Capitale", "Quota Interessi"], 
               loc='lower center', 
               bbox_to_anchor=(0.5,0.12), 
               ncol=2, 
               fontsize=15, 
               frameon=False)

    plt.tight_layout(rect=[0, 0.22, 1, 0.90])

    # Logica di esportazione
    print("\n\n###################################")
    print("### PLOT: struttura della rata  ###")
    print("###################################\n")

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