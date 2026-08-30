 # Simulazione Piani di Ammortamento Classici
Questa repository ospita un set di algoritmi in Python dedicati alla simulazione, all'analisi comparativa e alla visualizzazione grafica dei principali modelli di ammortamento per prestiti.

Le logiche implementate riflettono fedelmente le specifiche matematiche e finanziarie documentate nel file di riferimento `piani_ammortamento_classici.pdf`.

#### 🧭 Cosa cerchi?
-  [Per farti una idea](piani_ammortamento_classici.pdf)

- [Codice Python](py)

- [Immagini generate nelle simulazioni di esempio](png)

- Nucleo trasferibile in obsidian: [file Markdown](md), [configuazione personale del vault](.obsidian)

> consiglio la lettura del paragrafo "🚀 Requisiti e Utilizzo"

## 📌 Astrazione del Dominio
Costruire il piano di ammortamento di un prestito significa redigere il prospetto temporale attraverso il quale il debitore rimborsa il capitale e liquida gli interessi al creditore.

Gli script automatizzano la creazione di questi prospetti, calcolando per ogni periodo $s$ il sistema ricorsiva fondamentale:
- **Rata $R_{s}$**: somma matematica della quota capitale e della quota interessi al periodo corrente ($R_{s} = C_{s} + I_{s}$).
- **Quota interessi $I_{s}$**: frazione di remunerazione, calcolata applicando il tassi contrattuale $i_{s-1}$ al debito residuo del periodo precedente ($I_{s}=i*D_{s-1}$).
- **Debito residuo $D_{s}$**: porzione di debito ancora da rimborsare, decrescente in funzione della quota capitale versata ($D_{s}=D_{s-1}-C_{s}$).

## ⚙️ Modelli Implementati
La repository fornisce moduli indipendenti, strutturati per replicare specifiche logiche di rimborso:
| Modello di ammortamento | Script di riferimento | Caratteristica principale | Dinamica del piano |
|---|---|---|---|
| Francese | `ammortamento_francese.py` | Rata periodica invariata ($R_{s} = R$) | Quota interessi decrescente; quota capitale in progressione geometrica |
| Italiano | `ammortamento_italiano.py` | Quota capitale costante ($C_{s} = C = D_{0}/n$) | Abbattimento lineare del debito; rata periodica decrescente nel tempo |
| Bullet | `ammortamento_bullet.py` | Esclusivo pagamento di quote interessi | Rimborso integrale del capitale in un'unica soluzione alla scadenza finale ($C_{n} = D_{0}$) |
| Comparativo globale | `pyplot_struttura_rata_ammortamenti.py` | Elaborazione simultanea dei tre regimi | Analisi visiva della distribuzione percentuale temporale tra quota capitale e quota interessi |

## 🛠 Stack Tecnologico e Pipeline di Output
Per ogni modello eseguito, la pipeline di elaborazione esegue le seguenti operazioni:
1. **Generazione dati** (`pandas`): costruzione matriciale di un DataFrame strutturato contenente le serie: *Periodo*, *Rata*, *Quota interessi*, *Quota capitale* e *Debito residuo*.
2. **Esportazione I/O**: salvataggio opzionale del prospetto generato su file rigifo in formato CSV (configurato con separatore `;` e decimale `,`).
3. **Data visualization** (`matplot`): creazione ed esportazione di grafici a barre impilate per un'ispezione visiva dell'evoluzione temporale delle quote e del decadimento del debito.

## 🚀 Requisiti e Utilizzo
Il codice è progettato per essere eseguito in un ambiente Python locale standard.

#### Prerequisiti
Assicurarsi di disporre delle librerie di data manipulation e plotting. Da terminale:
``` bash
pip install pandas maplotlib
```
#### Esecuzione
Lanciare lo script target direttamente da terminale o tramite un IDE dedicato (es. VS Code). Esempio di esecuzione per il modello a rata costante:
``` bash
python ammortamento_francese.py
```
A runtime, l'algoritmo richiederà l'immissione da standard input dei seguenti parametri di calcolo (esclusivamente valori strettamente positivi):

1. Capitale da finanziare (€)
2. Tasso di interesse espresso in formato decimale
3. Numero totale di rate (intero)

---

**Dati usati per i grafici nella repository** 
- *finanziamento da 12K€*
- *tasso di interesse mensile fisso al 2,2%*
- *36 rate (3 anni di ammortamento)*

