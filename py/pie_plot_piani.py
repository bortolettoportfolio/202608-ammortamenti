import os

import matplotlib.pyplot as plt
from bullet import ammortamento_bullet
from francese import ammortamento_francese
from italiano import ammortamento_italiano


def acquisisci_input_numerico(prompt: str, tipo_dato: type):
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

def pie_plot_confronto(df_francese, df_italiano, df_bullet, cap: float, tasso: float, rate: int):
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
        return f"Costo Interessi:\n{valore:,.2f} %".replace(",", "X").replace(".", ",").replace("X", ".")

    labels_fr = ["", formatta_valuta(per_int_fr)]
    labels_it = ["", formatta_valuta(per_int_it)]
    labels_bu = ["", formatta_valuta(per_int_bu)]

    str_tot_fr = f"Totale Pagato: € {tot_fr:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    str_tot_it = f"Totale Pagato: € {tot_it:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    str_tot_bu = f"Totale Pagato: € {tot_bu:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    etichette_legenda = ["Quota Capitale", "Quota Interessi"]
    colori = ['#B32017', '#004B87']

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

    fig.suptitle("Impatto percentuale degli interessi", fontsize=25, fontweight='bold')
    fig.set_facecolor('none')
    ax1.set_facecolor('none')
    ax2.set_facecolor('none')
    ax3.set_facecolor('none')

    fig.legend(wedges, etichette_legenda, loc='lower center', bbox_to_anchor=(0.5, 0.12), ncol=2, fontsize=15, frameon=False)

    testo_specifiche = (f"Dati della simulazione ⟶ Finanziamento: {round(cap,2)} €;  Interesse su periodo: {round(tasso*100,2)} %;  Numero periodi: {rate}\n\nTasso fisso | Nessun preammortamento | Assenza del Day Count e festività")
    fig.text(0.5, 0.04, testo_specifiche, ha='center', va='bottom', fontsize=12, color='#111111', style='italic')

    plt.subplots_adjust(top=0.82, bottom=0.25, wspace=0.3)

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


if __name__ == "__main__":
    print("====================================================")
    print("   CONFRONTO STRUTTURA PIANI AMMORTAMENTO CLASSICI  ")
    print("====================================================\n")
    
    cap = acquisisci_input_numerico("Inserisci il capitale da finanziare (in €): ", float)
    tasso = acquisisci_input_numerico("Inserisci il tasso di interesse decimale (es. 0.05 per 5%): ", float)
    rate = acquisisci_input_numerico("Inserisci il numero totale di rate: ", int)
    
    print("\nElaborazione in corso...\n")

    df_fr = ammortamento_francese(cap, tasso, rate)
    df_it = ammortamento_italiano(cap, tasso, rate)
    df_bu = ammortamento_bullet(cap, tasso, rate)

    pie_plot_confronto(df_fr, df_it, df_bu, cap, tasso, rate)
