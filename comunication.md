# Model komunikacji client server

Ten plik zawiera sposób komunikacji client - server podczas gry w prawo dżungli

## komunikacja client -> server:

1. logowanie się do gry {32 bity}
   - numer pokoju [6 bity]
   - nazwa [14 bitów] (w przypadku krótszej nazwy reszta spacji)
2. wzięcie totemu {1 bit}
   - wysłanie pojedynczego znaku 't' [1 bit]
3. odsłonięcie swojej karty {1 bit}
   - jeden znak 'k' [1 bit]

## komunikacja server -> client:

1. stan gry {260 bitów}
   - bit wyniku gry [1 bit]
     - 0 - przegrana
     - 1 - gra nadal trwa
     - 2 - wygrana
   - ilość graczy liczba od 1-8 [1 bit]
   - kogo ruch liczba od 0-7 [1 bit]
   - komunikat [1 bit]
     - 0 - brak komunikatu
     - 1 - udało się wyrwać totem
     - 2 - ktoś wyrwał ci totem
     - 3 - niestety to nie te same karty

dla każdego gracza (8 razy)

- nazwa gracza [26 bitów] (dopełnione spacjami)
- liczba kart zakrytych [2 bity]
- liczba kart odkrytych [2 bity]
- numer karty na wierzchu [2 bity]
