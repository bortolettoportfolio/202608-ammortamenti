---
up:
  - "[[matematica finanziaria]]"
link:
  - "[[criteri di valutazione degli investimenti (tir e van)]]"
  - "[[problemi inversi nelle rendite]]"
  - "[[piani di ammortamento prestiti]]"
tipo: concetto
ambito: finanziario
tips:
  - Nel calcolo di cash flow perpetui o dividend discount model, ricorda che la rendita perpetua posticipata ha V0 = R/i, un'approssimazione vitale per calcolare rapidamente il terminal value.
---
# RENDITE FINANZIARIE - DEFINIZIONI E CALCOLO
## 1. Definizione e Classificazione delle Rendite

Una **rendita finanziaria** è una sequenza di flussi di cassa (entrate o uscite) denominati **rate** ($R_{s}$), esigibili in epoche temporali prefissate ($t_{s}$).
L'intervallo temporale tra due pagamenti consecutivi è il **periodo**.

Per strutturare correttamente i modelli di valutazione, le rendite si classificano secondo quattro dimensioni assiali:
1. **Importo della Rata:** *Costanti* ($R_{1}=R_{2}=\dots=R$) vs *Variabili*.
2. **Numero di Rate:** *Temporanee* (numero finito $n$) vs *Perpetue* ($n \to +\infty$).
3. **Competenza (Timing):** *Posticipate* (pagamento alla fine del periodo) vs *Anticipate* (pagamento all'inizio del periodo).
4. **Decorrenza:** *Immediate* (valutazione coincidente con l'inizio del primo periodo) vs *Differite* (la prima rata scade dopo un tempo $k>1$).

## 2. Valore Attuale e Montante (Rendita Costante Unitaria Posticipata)

Consideriamo il caso base: una rendita temporanea immediata posticipata, formata da $n$ rate unitarie ($R=1$) equispaziate. L'attualizzazione (in $t=0$) e la capitalizzazione (in $t=n$) avvengono nel regime dell'interesse composto.

### Il Valore Attuale ($V_{0}$)
Il valore attuale è la somma dei valori attuali dei singoli flussi. Fissato il fattore di sconto $v=(1+i)^{-1}$:
$$V_{0}=v+v^{2}+v^{3}+\dots+v^{n}$$
Questa è la somma di una progressione geometrica di ragione $v$. Moltiplicando per $(1+i)$ e calcolando la differenza con la serie originaria, si ottiene la formula chiusa del fattore **$a_{\overline{n}|i}$** ("*a figurato n al tasso i*"):
$$a_{\overline{n}|i}=\frac{1-(1+i)^{-n}}{i}$$

### Il Montante ($V_{n}$)
Il montante (valore in $t=n$) si ricava capitalizzando il valore attuale per $n$ periodi. Genera il fattore **$s_{\overline{n}|i}$** ("*s figurato n al tasso i*"):
$$s_{\overline{n}|i}=a_{\overline{n}|i}\cdot(1+i)^{n}=\frac{(1+i)^{n}-1}{i}$$

*(Per calcolare i valori di una rendita con rata costante non unitaria $R$, si moltiplicano semplicemente i fattori $a_{\overline{n}|i}$ e $s_{\overline{n}|i}$ per lo scalare $R$).*

## 3. Traslazioni Temporali: Variazioni del Modello Base

Le variazioni sul timing dei pagamenti si gestiscono applicando fattori di traslazione algoritmica al modello base.

### Rendite Anticipate
Se i pagamenti avvengono all'inizio di ogni periodo, ogni singolo flusso viene anticipato di un periodo. Matematicamente, equivale a capitalizzare il valore della rendita posticipata per un periodo $(1+i)$:
- **Valore Attuale:** $\ddot{a}_{\overline{n}|i}=a_{\overline{n}|i}\cdot(1+i)$
- **Montante:** $\ddot{s}_{\overline{n}|i}=s_{\overline{n}|i}\cdot(1+i)$

### Rendite Differite
Se l'inizio della rendita è posticipato di $k$ periodi nel futuro, il suo valore attuale all'epoca zero si ottiene scontando il valore $a_{\overline{n}|i}$ per i $k$ periodi di inattività:
$$V_{0}=R\cdot a_{\overline{n}|i}\cdot(1+i)^{-k}$$

### Rendite Perpetue
Se il numero di rate tende all'infinito, calcoliamo il limite per $n \to +\infty$ del valore attuale. Poiché il termine $(1+i)^{-n}$ tende a zero, si ottiene:
- **Perpetua Posticipata:** $V_{0}=\lim_{n\to+\infty}R\cdot\frac{1-(1+i)^{-n}}{i}=\frac{R}{i}$
- **Perpetua Anticipata:** $V_{0}=\frac{R}{i}\cdot(1+i)$

## 4. Rendite Frazionate

Se la rata annuale $R_{tot}$ viene frazionata in $m$ pagamenti sub-annuali di importo $R=\frac{R_{tot}}{m}$ (es. rate mensili, $m=12$), la valutazione richiede il tasso effettivo frazionato $i_{1/m}$:
$$V_{0}=R\cdot a_{\overline{n\cdot m}|i_{1/m}}=R\cdot\frac{1-(1+i_{1/m})^{-n\cdot m}}{i_{1/m}}$$

Esiste una relazione diretta per esprimere il valore della rendita frazionata in funzione del tasso effettivo annuo $i$ e del tasso nominale convertibile $j(m)$, introducendo il **coefficiente di conversione** $\frac{i}{j(m)}$:
$$V_{0}=R_{tot}\cdot a_{\overline{n}|i}\cdot\frac{i}{j(m)}$$