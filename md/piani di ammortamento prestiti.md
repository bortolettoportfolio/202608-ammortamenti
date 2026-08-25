---
up:
  - "[[matematica finanziaria]]"
link:
  - "[[modelli di ammortamento classici]]"
  - "[[clausole accessorie nei prestiti]]"
  - "[[leasing finanziario e credito al consumo]]"
  - "[[rendite finanziarie - definizioni e calcolo]]"
tipo: concetto
ambito: quantitativo
tips:
  - "Nel calcolo iterativo di un piano di ammortamento per i backtest, utilizza sempre la condizione di ricorrenza $D_{s}=D_{s-1}-C_{s}$ piuttosto che ricalcolare il debito residuo attualizzando le rate future: evita errori di approssimazione in virgola mobile sui flussi terminali."
---
# GENERALE: piani di ammortamento prestiti
Struttura base di un piano di ammortamento

| numero rata | quota capitale | quota interesse | rata | debito residuo |
| ----------- | -------------- | --------------- | ---- | -------------- |

## 1. Architettura dell'Ammortamento

Costruire il piano di ammortamento di un prestito significa redigere il prospetto temporale e quantitativo attraverso il quale il debitore (mutuatario) rimborsa il capitale e liquida gli interessi al creditore (mutuante). 
Il rientro di un debito iniziale $S$ (o $D_{0}$) avviene tramite il versamento di $n$ rate $R_{s}$ a scadenze prefissate $t_{s}$.

Ogni rata è strutturalmente composta da due elementi:
1. **Quota Capitale ($C_{s}$):** la frazione destinata all'effettiva restituzione del debito.
2. **Quota Interessi ($I_{s}$):** la frazione che rappresenta la remunerazione per il capitale non ancora restituito, calcolata al tasso contrattuale $i$.

$$R_{s}=C_{s}+I_{s}$$

## 2. Le Grandezze Fondamentali e il Sistema Ricorsivo

L'evoluzione del prestito nel tempo è descritta da un sistema di equazioni ricorsive basato sulle seguenti variabili di stato all'epoca $s$:

- **Quota Interessi:** Si ottiene applicando il tasso di interesse al debito residuo del periodo precedente.
  $$I_{s}=i\cdot D_{s-1}$$
- **Debito Residuo ($D_{s}$):** La porzione di debito ancora da rimborsare. Diminuisce epoca dopo epoca in funzione della sola quota capitale versata.
  $$D_{s}=D_{s-1}-C_{s}$$
- **Debito Estinto ($E_{s}$):** La somma di tutte le quote capitale già rimborsate fino all'epoca $s$.
  $$E_{s}=E_{s-1}+C_{s}=\sum_{k=1}^{s}C_{k}$$

In qualsiasi istante di valutazione, la somma tra il debito già rimborsato e quello ancora da rimborsare deve eguagliare il prestito iniziale:
$$D_{s}+E_{s}=S$$

## 3. Le Condizioni di Chiusura

Affinché il piano di ammortamento sia in equilibrio finanziario, devono essere soddisfatte due condizioni di chiusura.

### Condizione di Chiusura Elementare
La somma aritmetica di tutte le quote capitale versate nell'arco dell'operazione deve eguagliare esattamente il capitale inizialmente prestato. Alla scadenza $n$, il debito residuo è nullo ($D_{n}=0$) e il debito estinto è massimo ($E_{n}=S$).
$$S=\sum_{s=1}^{n}C_{s}$$

### Condizione di Chiusura Finanziaria
Il valore attuale di tutte le rate (quote capitale e quote interessi) attualizzate al tasso contrattuale $i$ deve corrispondere al capitale prestato all'epoca zero.
$$S=\sum_{s=1}^{n}R_{s}\cdot(1+i)^{-t_{s}}$$

## 4. Valutazione Intermedia del Prestito

La valutazione di un prestito in una data intermedia $t$ (con $0<t<n$) permette di scomporne il valore attuale residuo $V_{t}$ in due componenti, utili per le cessioni del credito o valorizzazioni di bilancio.

- **Nuda Proprietà ($N_{t}$):** Valore attuale delle sole *quote capitale* ancora da corrispondere dal tempo $t$ in poi.
  $$N_{t}=\sum_{s=t+1}^{n}C_{s}\cdot(1+i)^{-(s-t)}$$
- **Usufrutto ($U_{t}$):** Valore attuale delle sole *quote interessi* ancora da corrispondere.
  $$U_{t}=\sum_{s=t+1}^{n}I_{s}\cdot(1+i)^{-(s-t)}$$

Al tasso di valutazione pari al tasso contrattuale, la somma di Nuda Proprietà e Usufrutto eguaglia il valore attuale delle rate residue, che coincide con il Debito Residuo in $t$:
$$V_{t}=N_{t}+U_{t}=D_{t}$$

### Outstanding Capital (Montante Netto)
Dal punto di vista dell'investitore, l'Outstanding Capital ($W_{t}$) rappresenta la differenza tra il montante del prestito originario e il montante di tutti gli incassi già ricevuti fino al tempo $t$. 
$$W_{t}=S\cdot(1+i)^{t}-\sum_{s=1}^{t}R_{s}\cdot(1+i)^{t-s}$$
Al tasso contrattuale, questa grandezza bilancia l'operazione annullandosi in contropartita al valore attuale degli importi ancora da corrispondere.