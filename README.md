Simulazione Piani di Ammortamento Classici
Questa repository ospita un set di algoritmi in Python dedicati alla simulazione, all'analisi comparativa e alla visualizzazione grafica dei principali modelli di ammortamento per prestiti. Le logiche implementate riflettono fedelmente le specifiche matematiche e finanziarie documentate nel file di riferimento "piani_ammortamento_classici.pdf".
📌 Descrizione del Progetto
Costruire il piano di ammortamento di un prestito significa redigere il prospetto temporale attraverso il quale il debitore rimborsa il capitale e liquida gli interessi al creditore. 
La suite di script automatizza la creazione di questi prospetti, calcolando per ogni periodo il sistema ricorsivo fondamentale:
• Rata (R_s): La somma matematica della quota capitale e della quota interessi al periodo s (R_s = C_s + I_s).
• Quota Interessi (I_s): La frazione di remunerazione, calcolata applicando il tasso contrattuale i al debito residuo del periodo precedente (I_s = i \cdot D_{s-1}).
• Debito Residuo (D_s): La porzione di debito ancora da rimborsare, decrescente in funzione della quota capitale versata (D_s = D_{s-1} - C_s).
⚙️ Modelli Implementati
La repository fornisce moduli indipendenti per i seguenti regimi di ammortamento:
• Ammortamento Francese (ammortamento_francese.py)
 • Caratteristiche: Prevede il pagamento di una rata periodica invariata per tutta la durata del contratto (R_s = R).
 • Dinamica: La quota interessi decresce nel tempo, mentre la quota di capitale cresce in progressione geometrica.
• Ammortamento Italiano (ammortamento_italiano.py)
 • Caratteristiche: Il debito viene abbattuto in modo lineare tramite una quota capitale costante (C_s = C = \frac{D_0}{n}).
 • Dinamica: Genera una rata di periodo decrescente nel tempo.
• Ammortamento Bullet (ammortamento_bullet.py)
 • Caratteristiche: Il debitore corrisponde esclusivamente le quote interessi per tutta la durata del prestito.
 • Dinamica: Il rimborso integrale del capitale avviene in un'unica soluzione alla scadenza finale (C_n = D_0).
• Simulatore Comparativo Globale
 • Uno script aggregato che elabora simultaneamente i tre modelli, offrendo un'analisi visiva della distribuzione percentuale tra quota capitale e quota interessi.
🛠 Funzionalità Tecniche
Per ogni modello eseguito, gli script Python integrano le seguenti pipeline di output:
1. Generazione del DataFrame: Costruzione matriciale del piano contenente Periodo, Rata, Quota Interessi, Quota Capitale e Debito Residuo.
2. Esportazione Dati: Salvataggio opzionale del prospetto generato in formato CSV (strutturato con separatore ; e decimale , per la compatibilità europea).
3. Data Visualization: Creazione ed esportazione di grafici a barre impilate (tramite matplotlib) per visualizzare l'evoluzione temporale delle quote e l'impatto degli interessi sul debito.
🚀 Utilizzo
Assicurati di disporre di un ambiente Python configurato con le librerie pandas e matplotlib.
Avvia lo script desiderato tramite terminale. Ad esempio, per simulare un piano a rate costanti:
python ammortamento_francese.py
Il sistema richiederà in input i seguenti parametri strettamente positivi per l'elaborazione:
1. Capitale da finanziare (es. 12000 )
2. Tasso di interesse (preferibile un TAN adeguato) in formato decimale (es. 0.05 per indicare il 5%)
3. Numero totale di rate (es. 36)
