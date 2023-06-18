%--------- INIZIO -------------------

1{postino(X, 1): node(X)}1 :- ufficio_postale(X).

%--------- TERMINAZIONE -------------

%Terminazione all'Ufficio Postale, se il time non è valido e il precedente si, allora la posizione deve
%essere quella dell'ufficio postale

postino(X, T1) :- not time(T2), time(T1), T2 = T1+1, ufficio_postale(X).

%---------- SPOSTAMENTO ------------

%Ad un determinato tempo T, postino può essere in una sola posizione
:- node(X), node(Y), time(T), postino(X,T), postino(Y,T), X < Y.

%Per ogni tempo, deve esistere un postino
1{postino(X,T): node(X)}1 :- time(T).

%---------- CONSEGNA DI TUTTE LE LETTERE ------------

%Devo visitare tutti gli indirizzi di consegna
1{postino(N, T): time(T)} :- lettere(N, Q), node(N), Q > 0.

%----------- DIMENSIONE BUSTA -------------
%non deve esistere un contabuste con dimensione maggiore della dimensione della busta
%:- contabuste(S, T1, T2), dim_borsa(N), S > N, time(T1), time(T2).

%verifica se il nodo X è stato visitato tra il T1 e il T2
visited(X, T1, T2) :- time(T1), time(T2), time(T3), postino(X,T3), T1 < T3 < T2.

%definizione del predicato contabuste
contabuste(S, T1) :- time(T1), postino(Y, T1), ufficio_postale(Y), 
                  S = #sum{N: not visited(X, 1, T2), postino(X,T2), lettere(X, N), node(X) , time(T2), T2 < T1}.

%conta il numero di buste consegnate tra T1 e T2
%consegnate(S, T) :- time(T), ufficio_postale(Y), postino(Y,T), S = #sum{N: not visited(X, 1, T3), postino(X,T3), lettere(X, N), node(X), time(T3), T3 < T}. %rimosso  time(T5), T5 < T3,

:- time(T1), time(T2), contabuste(S1, T1), contabuste(S2, T2), dim_borsa(K), K < (S2 - S1). 

%----------- CALCOLO COSTO ----------------

%Costo
score(S) :- S = #sum{N, T, T+1: postino(X,T), postino(Y,T+1), costo_arco(X,Y,N), node(X), node(Y), time(T)}.

#minimize {S: score(S)}.

#show postino/2.
#show score/1.
%#show contabuste/3.
#show ufficio_postale/1.
%#show visited/3.

