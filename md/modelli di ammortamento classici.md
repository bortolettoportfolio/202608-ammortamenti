---
up: "[[piani di ammortamento prestiti]]"
link:
  - "[[rendite finanziarie - definizioni e calcolo]]"
tipo: modello
ambito: quantitativo
tips:
  - Nella modellizzazione di algoritmi in Python per le simulazioni dei flussi di cassa, vettorializza le quote capitale del piano Francese sfruttando la progressione geometrica, mentre per l'Italiano sfrutta array lineari.
---
# PIANI DI AMMORTAMENTO CLASSICI
*Figura 1*
![[pieplot_struttura_rata.png|550]]
## 1. Ammortamento a Rate Costanti (Modello Francese)

>algoritmo: [[ammortamento_francese.py]]

Il piano di ammortamento francese è la struttura caratterizzata dal pagamento di una rata periodica invariata per tutta la durata del contratto ($R_{s}=R$ per $s=1,2,\dots,n$).

Per il principio di chiusura finanziaria, la rata costante si determina rapportando il debito iniziale al fattore di valore attuale di una rendita unitaria:
$$R = \frac{D_{0}}{a_{\overline{n}|i}}$$

### Dinamica delle Quote
* Poiché la rata è fissa e il debito residuo decresce, la quota interessi diminuisce nel tempo, mentre la quota capitale aumenta.
* Le quote di capitale crescono in progressione geometrica di ragione $(1+i)$:
$$C_{t} = C_{t-1}(1+i) \quad \implies \quad C_{t+s} = C_{t}(1+i)^{s}$$

Formule dirette per qualsiasi epoca $s$ ( ponendo il fattore di sconto $v = \frac{1}{1+i} = (1+i)^{-1}$):
* Prima quota capitale: $C_{1} = R \cdot v^{n}$.
* Quota capitale al tempo $s$: $C_{s} = R \cdot v^{n-s+1}$.
* Quota interessi al tempo $s$: $I_{s} = R \cdot [1 - v^{n-s+1}]$.

*Figura 2*
![[ammortamento_francese.png|550]]
## 2. Ammortamento a Quote di Capitale Costanti (Modello Italiano)

>algoritmo: [[ammortamento_italiano.py]]

Il piano di ammortamento italiano prevede che il debito venga abbattuto in modo lineare, con quota capitale fissa pari a:
$$C_{s} = C = \frac{D_{0}}{n}$$

### Dinamica delle Rate e degli Interessi
* Debito Residuo: $D_{s} = \frac{D_{0}}{n} \cdot (n-s)$.
* Quota Interessi: $I_{s} = \frac{D_{0}}{n} \cdot [n - (s-1)] \cdot i$.
* Rata di periodo: $R_{s} = \frac{D_{0}}{n} \cdot [1 + (n-s+1) \cdot i]$.

*Figura 3*
![[ammortamento_italiano.png|550]]
## 3. Ammortamento a Quote di Interessi Costanti (Modello Bullet)

>algoritmo: [[ammortamento_bullet.py]]

Nel modello a scadenza (Bullet), il debitore corrisponde unicamente le quote interessi durante la vita del prestito, mentre l'intero capitale viene rimborsato alla scadenza $n$.
* Quote Capitale: $C_{s} = 0$ per $s=1,2,\dots,n-1$ e $C_{n} = D_{0}$.
* Rate Intermedie: $R_{s} = D_{0} \cdot i$ per $s=1,2,\dots,n-1$.
* Rata Finale: $R_{n} = D_{0} \cdot i + D_{0} = D_{0}(1+i)$.

*Figura 4*
![[ammortamento_bullet.png|550]]
## 4. Piani ad Interessi Anticipati

Nei piani ad interessi anticipati, la liquidazione dell'interesse di un periodo viene computata e incassata all'inizio del periodo. La quota interessi si calcola applicando il tasso di sconto al debito residuo:
$$I_{s} = D_{s} \cdot \frac{i}{1+i}$$

---
Altri dettagli:
[Ammortamento Bullet](https://www.borsaitaliana.it/borsa/glossario/bullet.html)