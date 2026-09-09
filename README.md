 # Simulazione dei flussi di cassa nei finanziamenti classici
Questa repository ospita un set di algoritmi in Python dedicati alla simulazione, all'analisi comparativa e alla visualizzazione grafica dei principali modelli di ammortamento per prestiti.

> Le logiche implementate riflettono fedelmente le specifiche matematiche finanziarie classiche.

## 🧭 Cosa cerchi?
|link interno |avanzamento|
|:---|:---:|
|[programma completo](py/main.py)| 🟡|
|[immagini delle simulazioni](png)| 🟡|
|[teoria senza troppi giri di parole](piani_ammortamento_classici.pdf)| 🟡| 

> Consiglio la lettura del paragrafo "🤞 Requisiti e Utilizzo"

## 🫠 In sintesi
Costruire il piano di ammortamento di un prestito significa redigere il prospetto temporale attraverso il quale il debitore rimborsa il capitale e liquida gli interessi al creditore.

Gli script automatizzano la creazione di questi prospetti, calcolando per ogni periodo $s$ il sistema ricorsivo fondamentale:
- **Rata $R_{s}$**: somma matematica della quota capitale e della quota interessi al periodo corrente ($R_{s} = C_{s} + I_{s}$).
- **Quota interessi $I_{s}$**: frazione di remunerazione, calcolata applicando il tassi contrattuale $i_{s-1}$ al debito residuo del periodo precedente ($I_{s}=i*D_{s-1}$).
- **Debito residuo $D_{s}$**: porzione di debito ancora da rimborsare, decrescente in funzione della quota capitale versata ($D_{s}=D_{s-1}-C_{s}$).


### Rata costante
L'[ammortamento alla francese](py/francese.py) è una modalità di calcolo impiegata in modo ampio da banche e finanziarie quando si deve stabilire l'ammontare di un finanziamento.
Prevede un rimborso con **rate costanti per tutta la durata del piano di ammortamento**.

---
### Quota capitale costante
L’[ammortamento all’italiana](py/italiano.py) è un metodo di rimborso del debito che prevede **rate di importo decrescente nel tempo**.
Ogni rata è composta da una quota di capitale costante e da una quota di interessi che diminuisce progressivamente, poiché viene calcolata sul debito residuo.

---
### Quota interessi costante 
L'[ammortamento bullet](py/bullet.py) è un piano di rimborso di un prestito in cui il capitale viene restituito interamente in un'unica soluzione alla scadenza, mentre durante la vita del finanziamento si pagano periodicamente solo gli interessi

---
### fico, ma non ci sono ancora :(
* **ammortamento tedesco**: viene utilizzata la stessa logica del piano alla francese, con rata fissa, quota interessi “fissa” decrescente e quota capitale che si adatta in modo tale da mantenere la rata costante. Tuttavia nell’ammortamento tedesco *il calcolo degli interessi avviene in modo anticipato*, per cui ci si riferisce a valori attualizzati, che sono leggermente più bassi rispetto il calcolo con l’ammortamento francese.

* **ammortamento americano/anglossassone**: si tratta di una soluzione strutturata su un piano di rimborso ed uno di investimento. I *tassi di interesse devono essere scelti in modo tale da ridurre l’impatto degli interessi passivi del mutuo attraverso quelli legati agli investimenti*. A livello di organizzazione la quota degli interessi è fissa, e le rate sono fatte di soli interessi, mentre con l’accumulo di capitale si costruiscono le somme che periodicamente vengono usate per rimborsare il prestito ottenuto.
> testo per quelli mancanti preso da [questo sito](https://www.calcoloratamutuo.org/guida/piano-ammortamento)

## 🛠 Flusso simulazione
Per ogni modello eseguito, la pipeline di elaborazione esegue le seguenti operazioni:
1. **Generazione dati** (`pandas`): costruzione di un DataFrame strutturato contenente le serie:

    |*Periodo*|*Rata*|*Quota interessi*|*Quota capitale*|*Debito residuo*|
    |:---:|:---:|:---:|:---:|:---:|
    | $s$ | $R_{s}$ | $I_{s}$ | $C_{s}$ | $D_{s}$ |

2. **Esportazione I/O**: salvataggio **opzionale** del prospetto generato su file rigido in formato CSV (configurato con separatore `;` e decimale `,`).
3. **Data visualization** (`matplot`): creazione ed esportazione dei grafici 

## 🤞 Requisiti e Utilizzo
Il codice è progettato per essere eseguito in un ambiente Python locale standard.

#### 🖥️ Prerequisiti
Assicurarsi di disporre delle librerie di data manipulation e plotting. 
Da terminale:
``` bash
pip install pandas maplotlib
```
#### ▶️ Esecuzione
Lanciare lo script target direttamente da terminale o tramite un IDE dedicato (es. VS Code). 
Esempio di esecuzione per il modello a rata costante:
``` bash
python francese.py
```
Esempio di esecuzione per visualizzare esclusivamente uno dei plot in particolare:
``` bash
python pie_plot_piani.py
```

A runtime, l'algoritmo richiederà l'immissione da standard input dei seguenti parametri di calcolo (esclusivamente valori strettamente positivi)

---

**Dati usati per i grafici nella repository** 
- *finanziamento da 30K€*
- *TAN pari a 3,25 %*
- *60 rate (5 anni di ammortamento)*

---
## guide utili
- [Pandas user guide](https://pandas.pydata.org/docs/user_guide/index.html)
- [Matplotlib user guide](https://matplotlib.org/stable/users/index)


