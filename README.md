# Projekt bazy danych semestr 5

## Założenia do projektu

Celem projektu jest porównanie wybranych metod alokacji shardów równoważących obciążenie rozproszonej bazy danych w chmurze obliczeniowej.

## Kontekst

Dana chmura obliczeniowa z rozproszoną bazą danych. Chmura składa się z N węzłów, na których alokowane jest M shardów danych bazy danych. Przyjmujemy, że M>>N, bo każdy z węzłów chmury składuje kilkanaście – kilkadziesiąt shardów. Średnia liczba shardów składowanych na poszczególnych węzłach wynosi M/N. 

Dzięki predykcji obciążenia chmury dane są K wymiarowe wektory przyszłych obciążeń dla każdego z shardów w kolejnych przedziałach czasu. Wartości składowane w poszczególnych składowych wektorów reprezentują średnie obciążenie w kolejnych przedziałach czasu. Możemy sobie wyobrazić 24 wymiarowe wektory (K=24), dla których wartość każdej składowej reprezentuje średnie obciążenie w kolejnych godzinach doby.

Zadaniem algorytmów alokacji shardów jest minimalizacja opóźnień w dostępie do danych poprzez równomierne obciążenie węzłów w poszczególnych przedziałach czasowych. Problem obliczeniowy rozwiązywany przez proponowane algorytmy polega na takiej alokacji shardów żeby sumaryczne obciążenie shardów na każdym z węzłów było jak najbardziej podobne do uśrednionego obciążenia całej chmury. Dzięki temu sumaryczne obciążenia chmur dla kolejnych przedziałów czasowych będą podobne do siebie. 

## Opis eksperymentu

Należy skonstruować sparametryzowany generator przewidywanego obciążenia dla każdego z shardów. Generowane wektory obciążenia będą przynależeć do jednego z kilku klastrów. Przebiegi obciążenia shardów w pojedynczym klastrze mają być skorelowane. Jednymi z parametrów generatora mają być korelacje przebiegów obciążenia wewnątrz klastrów i między klastrami.
Zbiór wygenerowanych wektorów ma być następnie alokowanych przez wybrane algorytmy. Ocena działania algorytmów będzie polegać na porównaniu błędu średniokwadratowego odstępstw sumarycznych obciążeń węzłów od uśrednionego obciążenia całej chmury.

## Zadania

- [zadanie 1](/tasks/task%201/description.md)


## Skład zespoły

- tutaj możecie się wpisać, nie wiem czy chcecie imie i nazwisko, czy inaczej
- [Konrad](https://github.com/Aviuss)
