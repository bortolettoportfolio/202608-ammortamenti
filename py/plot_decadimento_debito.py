import matplotlib.pyplot as plt
import pandas as pd


def plot_confronto_decadimento(df: pd.DataFrame, cap: float, tasso: float, rate: int,):
    """
    Grafico che mostra il decadimento del debito residuo nei piani di ammortamento classici.
    """
    # Creazione tela con dimensioni standardizzate
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Titolo Globale
    fig.suptitle("Decadimento debito residuo", fontsize=25, fontweight='bold', y=0.88)

    # CORREZIONE: Assegnazione della 'label' direttamente alla riga tracciata
    ax.plot(df['Periodo'], df['Debito Residuo (€)'], label="Andamento del debito rimanente")    
    
    # Formattazione Assi
    ax.set_xlabel("Numero Rata", fontsize=18, labelpad=15)
    ax.set_ylabel("Debito residuo [€]", fontsize=18, labelpad=15)
    
    ax.set_xticks(df['Periodo'])
    ax.tick_params(axis='both', pad=10)
    
    ax.grid(axis='y', linestyle=':', color='gray', alpha=0.4)

    # CORREZIONE: Invocazione pulita della legenda (estrae in automatico la label dal plot)
    fig.legend(loc='lower center', 
               bbox_to_anchor=(0.5, 0.12), 
               ncol=2, 
               fontsize=15, 
               frameon=False)

    # Testo aggiuntivo a fine grafico
    testo_specifiche = f"Dati della simulazione ⟶ Finanziamento: {round(cap, 2)} €;  Interesse su periodo: {round(tasso * 100, 2)} %;  Numero periodi: {rate}"

    fig.text(0.5, 0.085, testo_specifiche, 
             ha='center',       
             va='bottom',       
             fontsize=12, 
             color='#666666',   
             style='italic')
    
    plt.tight_layout(rect=[0, 0.22, 1, 0.90])
    plt.show()