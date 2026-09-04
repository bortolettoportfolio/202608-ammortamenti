# CALCOLATORE FRAZIONAMENTO TASSO D'INTERESSE
''' 
Quando l'anno (unità di tempo di riferimento) viene suddiviso in 'm' parti uguali di ampiezza
'1/m', occorre misurare il rendimento effettivo su tale sotto-periodo.

A seconda del regime finanziario in cui si opera, la relazione tra tasso annuo 'i' e il 
tasso frazionato '1/m' varia strutturalmente.
'''

## definizione delle variabili
i = float(input("Inserisci il tasso di interesse (in formato decimale): ")) ### tasso di interesse unità di riferimento
m = int(input("Inserisci il frazionamento: ")) ### frazionoamento unità di riferimento

## funzione per il calcolatore frazionamento
def frazionamento(i, m):
    print(" ")
    print("###################################################################")
    print("CALCOLATORE FRAZIONAMENTO INTERESSE NEI REGIMI CLASSICI")
    print("###################################################################")
    print(" ")
    print(f"Tasso interesse riferito a unità di tempo da frazionare: {i*100} %")
    print(f"Frazionamento dell'unità temporale: {m}")
    print(" ")
    print("-------------------------------------------------------------------")
    print(" ")

    ### nel regime ad interesse SEMPLICE
    i_m_RIS = i/m
    ### nel regime ad interesse COMPOSTO
    i_m_RIC = ((1+i)**(1/m))-1

    ### OUTPUT
    print("Risultato del frazionamento nei due regimi:")
    print(f"- Regime semplice: {round(i_m_RIS*100, 4)} %")
    print(f"- Regime composto: {round(i_m_RIC*100, 4)} %")
    print(" ")
    print("###################################################################")

## DEBUG
frazionamento(i,m)