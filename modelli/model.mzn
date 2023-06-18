include "globals.mzn"; 

int: num_nodi;
int: max_step;   %numero massimo di passi (elevato)

int: ufficio_postale;
int: dim_borsa;    %assumo che la borsa sia almeno grande quanto il max num di lettere per un indirizzo

array [1..num_nodi] of int: elenco_lettere;
array [1..num_nodi, 1..num_nodi] of int: distanze;

%VARIABILI

array [1..max_step] of var 0..num_nodi: percorso;
var int: costo;

%CONSTRAINT

%partenza dall'ufficio postale
constraint percorso[1] = ufficio_postale; 

%terminazione all'ufficio postale
constraint exists(i in 1..max_step)(percorso[i] == ufficio_postale /\ forall (j in i+1..max_step)(percorso[j] == 0));

%consegna di tutte le lettere
constraint forall(i in 1..num_nodi where elenco_lettere[i] > 0)(exists(j in 1..max_step)(percorso[j] == i));

%limite della capienza della borsa del postino
constraint forall(i in 1..max_step-1 where percorso[i] == ufficio_postale /\ percorso[i+1] != 0)
                  (exists(j in i+1..max_step where percorso[j] == ufficio_postale)
                    (sum(k in i..j where not exists(z in 1..k-1)(percorso[z] == percorso[k])) %considero solo i nodi non ancora visitati
                      ((elenco_lettere[percorso[k]])) <= dim_borsa));

%calcolo del costo
constraint costo = sum(i in 1..max_step-1 where percorso[i+1] != 0)(distanze[percorso[i],percorso[i+1]]);

solve minimize costo;
