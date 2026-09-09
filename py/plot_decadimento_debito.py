import os

import matplotlib.pyplot as plt
import pandas as pd


def plot_confronto_decadimento(df_fr: pd.DataFrame, df_it: pd.DataFrame, df_bl: pd.DataFrame):
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
    print("\n\n############################################")
    print("### PLOT: Decadimento del debito residuo ###")
    print("##############################################\n")
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

            plt.savefig(nome_file, transparent=True, dpi=300, bbox_inches='tight', pad_inches=0.4)
            print(f"[SUCCESSO] Grafico esportato correttamente in '{nome_file}'.")
        except Exception as e:
            print(f"[ERRORE] Impossibile salvare il grafico: {e}")

    print("\nChiusura della finestra del grafico in corso... (Chiudi la finestra per terminare il programma)")
    plt.show()