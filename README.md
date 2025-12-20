# Porównanie Algorytmów Alokacji Shardów w Rozproszonej Bazie Danych

## Spis treści
- [O projekcie](#o-projekcie)
- [Kontekst](#kontekst)
- [Algorytmy](#algorytmy)
- [Generatory danych](#generatory-danych)
- [Instalacja](#instalacja)
- [Użycie](#użycie)
- [Struktura projektu](#struktura-projektu)
- [Wyniki i wizualizacje](#wyniki-i-wizualizacje)
- [Autorzy](#autorzy)

## O projekcie

Projekt porównuje różne metody alokacji shardów równoważących obciążenie rozproszonej bazy danych w chmurze obliczeniowej. Celem jest minimalizacja opóźnień w dostępie do danych poprzez optymalne rozmieszczenie shardów na węzłach.

### Cel
Porównanie algorytmów alokacji shardów w kontekście minimalizacji błędu średniokwadratowego (MSE) obciążenia węzłów.

## Kontekst

### Model systemu
- **N węzłów** w chmurze obliczeniowej
- **M shardów** bazy danych (M >> N)
- Każdy węzeł składuje kilkanaście-kilkadziesiąt shardów (średnio M/N)
- **Wektory obciążenia K-wymiarowe** (domyślnie K=24, reprezentujące 24 godziny doby)

### Problem do rozwiązania
Należy tak alokować shardy na węzłach, aby sumaryczne obciążenie każdego węzła było jak najbardziej zbliżone do uśrednionego obciążenia całej chmury. Minimalizujemy błąd średniokwadratowy (MSE) między obciążeniem poszczególnych węzłów a średnim obciążeniem.

## Algorytmy

Projekt implementuje cztery algorytmy alokacji shardów:

### 1. Random Allocation (Losowa alokacja)

**Opis:** Prosty algorytm bazowy przydzielający shardy losowo do węzłów na podstawie równomiernego rozkładu prawdopodobieństwa. Dla każdego shardu losuje indeks węzła z przedziału [0, N-1] z równym prawdopodobieństwem.

**Algorytm:**
1. Dla każdego shardu z listy wektorów obciążenia
2. Wylosuj równomiernie indeks węzła
3. Przydziel shard do wylosowanego węzła

**Złożoność:** O(M), gdzie M to liczba shardów

**Plik:** [random_allocation.py](algorithms/random_allocation.py)

### 2. Multiway Number Partitioning

**Opis:** Dwufazowy algorytm heurystyczny minimalizujący maksymalne obciążenie węzłów.

**Algorytm:**
1. **Sortowanie:** Posortuj wektory obciążenia malejąco według normy L∞:
   - $L_\infty = \max(|\max(W_i)|, |\min(W_i)|)$
   - Shardy o największym obciążeniu przetwarzane jako pierwsze

2. **Alokacja zachłanna:** Dla każdego wektora w kolejności:
   - Dla każdego węzła oblicz sumaryczny wektor po dodaniu shardu
   - Wyznacz maksymalną składową dla każdego potencjalnego węzła
   - Przydziel shard do węzła o najmniejszej wartości maksymalnej składowej
   - W przypadku remisu wybierz węzeł losowo

**Złożoność:** O(M log M + M·N·K), gdzie M to liczba shardów, N to liczba węzłów, K to wymiar wektorów

**Plik:** [multiway_number_partitioning.py](algorithms/multiway_number_partitioning.py)

### 3. Mean Squared Error Minimization

**Opis:** Algorytm alokujący shardy w sposób minimalizujący bezpośrednio błąd średniokwadratowy każdego węzła.

**Algorytm:**
1. **Sortowanie:** Posortuj wektory obciążenia malejąco według kwadratu normy L2:
   - $L_2^2 = \sum_{k=1}^{K} W_{i,k}^2$ (bez pierwiastkowania)
   - Shardy o największym obciążeniu przetwarzane jako pierwsze

2. **Alokacja optymalizująca MSE:** Dla każdego wektora:
   - Dla każdego węzła j oblicz:
     - $MSE_{before}$ - błąd średniokwadratowy węzła przed dodaniem shardu
     - $MSE_{after}$ - błąd średniokwadratowy węzła po dodaniu shardu
     - $\Delta_{MSE} = MSE_{before} - MSE_{after}$ - redukcja MSE
   - Przydziel shard do węzła maksymalizującego $\Delta_{MSE}$
   - W przypadku remisu:
     - Wybierz węzeł o mniejszym module sumarycznego wektora obciążenia
     - Jeśli nadal remis, wybierz losowo

**Złożoność:** O(M log M + M·N·K)

**Plik:** [mean_squared_error_minimization.py](algorithms/mean_squared_error_minimization.py)

### 4. SALP (Shard Allocation Load Prediction)

**Opis:** Zaawansowany algorytm zachłanny wykorzystujący predykcję obciążenia i miarę kąta między wektorami. Algorytm SALP optymalizuje alokację każdego kolejnego shardu na podstawie metryki SAM (Shard Allocation Metric), która uwzględnia zarówno kąt między wektorami obciążenia, jak i redukcję modułu wektora dopełnienia.

#### Pojęcia podstawowe:

- **Wi** - Wektor obciążenia pojedynczego shardu i, reprezentujący przewidywane obciążenie w kolejnych jednostkach czasu
- **WTS** - Sumaryczny wektor obciążenia dla całej chmury: $WTS = \sum_{i=1}^{F} W_i$
- **NWTS** - Znormalizowany wektor obciążenia (na jeden węzeł): $NWTS = \frac{1}{N} \cdot WTS$
- **TWSi** - Tymczasowy wektor obciążenia węzła i (suma wektorów alokowanych shardów)
- **WSi** - Ostateczny wektor obciążenia węzła i po zakończeniu alokacji
- **CVi** - Wektor dopełnienia węzła i: $CV_i = NWTS - TWS_i$
- **αCVi** - Kąt dopełnienia między wektorem CVi a wektorem NWTS (dziedzina: <0°, 180°>)

#### Metryka SAM (Shard Allocation Metric):

Algorytm przydziela kolejny shard do węzła maksymalizującego wartość metryki SAM:

$$SAM = \frac{\Delta\alpha_{CV_i} + 90°}{180°} \cdot \frac{\Delta|CV_i|}{|NWTS|}$$

gdzie:
- $\Delta\alpha_{CV_i} = \alpha_{CV_i, after} - \alpha_{CV_i, before}$ - zmiana kąta dopełnienia
- $\Delta|CV_i| = |CV_i|_{before} - |CV_i|_{after}$ - zmiana modułu wektora dopełnienia
- Dodatnie wartości $\Delta\alpha_{CV_i}$ oznaczają zmniejszenie kąta (poprawę)
- Normalizacja przez dodanie 90° pozwala na kompensację pogorszenia kąta przez znaczną redukcję modułu

#### Algorytm działania:

1. **Inicjalizacja:**
   - Oblicz sumaryczny wektor obciążenia: $WTS = \sum W_i$
   - Wyznacz znormalizowany wektor: $NWTS = \frac{1}{N} \cdot WTS$

2. **Sortowanie:**
   - Posortuj wektory obciążenia Wi malejąco według normy euklidesowej $L_2$
   - Umieść je na liście LW

3. **Przygotowanie węzłów:**
   - Dla każdego węzła utwórz:
     - Pusty podzbiór shardów FSi
     - Wektor obciążenia WSi (początkowo zerowy)
     - Wektor dopełnienia CVi = NWTS - WSi (początkowo równy NWTS)

4. **Alokacja:**
   - Dla każdego shardu Fi z listy LW:
     - Oblicz wartość SAM dla każdego węzła
     - Przydziel shard do węzła j maksymalizującego SAM
     - Aktualizuj: $WS_j = WS_j + W_i$
     - W przypadku remisu (ta sama wartość SAM) wybierz węzeł losowo

**Złożoność:** O(M log M + M·N·K)

**Status:** W trakcie implementacji

**Plik:** [salp.py](algorithms/salp.py)

## Generatory danych

### Generator z rozkładem wykładniczym
Generuje wektory obciążenia zgodnie z rozkładem wykładniczym (λ=1).

**Parametry:**
- `shard_count` - liczba shardów (wektorów)
- `dimensions` - wymiarowość wektorów (domyślnie 24)
- `lambda_value` - parametr rozkładu wykładniczego (domyślnie 1)

**Pliki:** 
- [exp_random_generator.py](generators/exp_random_generator.py)
- [exp_random_generator_run.py](generators/exp_random_generator_run.py)

### Generator sparametryzowany
Zaawansowany generator umożliwiający tworzenie skorelowanych wektorów obciążenia w klastrach.

**Parametry:**
- `S` - liczba shardów
- `N` - liczba węzłów
- `K` - liczba grup/klastrów
- `R` - amplituda
- `KO` - korelacja między klastrami
- `KI` - korelacja wewnątrz klastra
- `CN` - liczba cykli
- `D` - odchylenie standardowe rozmiarów grup
- `dimensions` - wymiarowość (domyślnie 24)

**Pliki:**
- [parametrized_generator.py](generators/parametrized_generator.py)
- [parametrized_generator_run.py](generators/parametrized_generator_run.py)

## Instalacja


### Instalacja zależności

```bash
pip install -r requirements.txt
```

## Użycie

### Uruchomienie głównego programu

#### Generowanie nowych danych losowych
```bash
python main.py generate
```

#### Wczytanie danych z pliku CSV
```bash
python main.py load <ścieżka_do_pliku.csv>
```

Przykład:
```bash
python main.py load ./input_files/exp_rand_50_data.csv
```

### Konfiguracja parametrów

W pliku [main.py](main.py) można zmienić następujące parametry:

```python
AVERAGE_SHARDS_PER_NODE = 10  # Średnia liczba shardów na węzeł
SHARD_COUNT = 54              # Całkowita liczba shardów
DIMENSIONS = 24               # Wymiarowość wektorów obciążenia
LAMBDA = 1                    # Parametr rozkładu wykładniczego
```

### Generowanie danych

#### Generator z rozkładem wykładniczym
```bash
python generators/exp_random_generator_run.py <liczba_shardów> [nazwa_pliku]
```

Przykłady:
```bash
python generators/exp_random_generator_run.py 30
python generators/exp_random_generator_run.py 30 output.csv
```

#### Generator sparametryzowany
```bash
python generators/parametrized_generator_run.py <liczba_shardów> [nazwa_pliku]
```

Przykłady:
```bash
python generators/parametrized_generator_run.py 30
python generators/parametrized_generator_run.py 30 output.csv
```

## Struktura projektu

```
.
├── main.py                          # Główny plik wykonawczy
├── README.md                        # Dokumentacja projektu
├── description.md                   # Szczegółowy opis etapów projektu
│
├── algorithms/                      # Implementacje algorytmów
│   ├── random_allocation.py         # Algorytm losowej alokacji
│   ├── multiway_number_partitioning.py
│   ├── mean_squared_error_minimization.py
│   ├── salp.py                      # SALP (w trakcie implementacji)
│   └── shard_algorithm.py           # Klasa bazowa dla algorytmów
│
├── generators/                      # Generatory danych
│   ├── exp_random_generator.py      # Generator z rozkładem wykładniczym
│   ├── exp_random_generator_run.py
│   ├── parametrized_generator.py    # Generator sparametryzowany
│   └── parametrized_generator_run.py
│
├── utils/                           # Narzędzia pomocnicze
│   ├── charts.py                    # Wizualizacje wyników
│   ├── dataobjects.py               # Struktury danych
│   ├── input_output.py              # Obsługa wejścia/wyjścia
│   ├── mean_squared_error.py        # Obliczanie MSE
│   ├── node.py                      # Reprezentacja węzła
│   └── vectors_utils.py             # Operacje na wektorach
│
├── input_files/                     # Pliki z danymi testowymi
│
└── graphs/                          # Folder na wykresy i wizualizacje
```

## Wyniki i wizualizacje

Program generuje następujące wyniki:

### Metryki dla każdego algorytmu:
- **Average MSE** - średni błąd średniokwadratowy
- **Median MSE** - mediana błędu średniokwadratowego
- **Max MSE** - maksymalny błąd średniokwadratowy

### Wizualizacje:
1. **Wykresy słupkowe** - pokazujące obciążenie poszczególnych węzłów
2. **Animacje GIF** - wizualizujące proces alokacji shardów krok po kroku
3. **Wykresy porównawcze MSE** - porównujące wydajność algorytmów

Wszystkie wizualizacje zapisywane są w folderze `graphs/`.

## Ocena algorytmów

Algorytmy oceniane są na podstawie błędu średniokwadratowego (MSE):

$$MSE_{węzeł} = \frac{1}{K} \sum_{k=1}^{K} (obciążenie_{węzeł,k} - średnie\_obciążenie_k)^2$$

gdzie:
- K - liczba przedziałów czasowych (wymiar wektorów)
- obciążenie_{węzeł,k} - obciążenie węzła w k-tym przedziale czasowym
- średnie_obciążenie_k - średnie obciążenie wszystkich węzłów w k-tym przedziale

Im niższy MSE, tym lepsze zrównoważenie obciążenia między węzłami.

## Autorzy

Zespół projektowy:
- [Kamil Suwiczak](https://github.com/kamilsuwiczak)
- [PMigaj](https://github.com/patromi)
- [Konrad](https://github.com/Aviuss)
- [Teodor](https://github.com/Teodor11)

---

**Projekt:** Bazy Danych - Semestr 5

**Uniwersytet:** Politechnika Poznańska

**Rok akademicki:** 2025/2026
