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

## Generator
### [Rozkład wykładniczy](/generators/exp_random_generator.py)

Użycie: `$ python exp_random_generator_run.py <shard_count> [filename]`, np. 
- `$ python exp_random_generator_run.py 30 result.txt` → zapisanie wyniku do pliku
- `$ python exp_random_generator_run.py 30` → wypisanie wyniku na konsoli

### [Generator sparametryzowany](/generators/parametrized_generator.py)

Użycie: `$ python parametrized_generator.py <shard_count> [filename]`, np. 
- `$ python parametrized_generator.py 30 result.txt` → zapisanie wyniku do pliku
- `$ python parametrized_generator.py 30` → wypisanie wyniku na konsoli

## Zadania

- [Zadanie 1](/tasks/task_1/description.md)

Użycie (wywołanie z głównego katalogu):
- `$ python -m tasks.task_1.main generate` → wygenerowanie nowych losowych danych
- `$ python -m tasks.task_1.main load ./tasks/task_1/input_files/data` → wczytanie danych z pliku


## Skład zespoły

- [Kamil Suwiczak](https://github.com/kamilsuwiczak)
- [PMigaj](https://github.com/patromi)
- [Konrad](https://github.com/Aviuss)
- [Teodor](https://github.com/Teodor11)
