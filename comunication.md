# Model komunikacji client server

Ten plik zawiera sposób komunikacji client - server podczas gry w prawo dżungli

## komunikacja client -> server:

1. logowanie się do gry {18 bajty}
   - numer pokoju [4 bajty]
   - nazwa [14 bitów] (w przypadku krótszej nazwy reszta spacji)
2. wzięcie totemu {1 bajtów}
   - wysłanie pojedynczego znaku 't' [1 bajtów]
3. odsłonięcie swojej karty {1 bajtów}
   - jeden znak 'c' [1 bajtów]

## komunikacja server -> client:

1. odpowiedź servera na logowanie {1 bajtów}
   - 0 jeśli nastąpił błąd (pokój jest pełen)
   - 1-8 pozycja gracza na planszy
2. stan gry {260 bajtówów}
   - bajtów wyniku gry [1 bajtów]
     - 0 - gra w toku
     - 1-7 - wygrał dany gracz
   - ilość graczy liczba od 1-7 [1 bajtów]
   - kogo ruch liczba od 0-7 [1 bajtów]
   - komunikat [1 bajtów]
     - 0 - brak komunikatu
     - 1 - udało się wyrwać totem
     - 2 - ktoś wyrwał ci totem
     - 3 - niestety to nie te same karty

dla każdego gracza (8 razy)

- nazwa gracza [26 bajtówów] (dopełnione spacjami)
- liczba kart zakrytych [2 bajty]
- liczba kart odkrytych [2 bajty]
- numer karty na wierzchu [2 bajty]
