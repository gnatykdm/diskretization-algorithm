# 🌟 Algorytm Dyskretyzacji Atrybutu Ciągłego

Implementacja **algorytmu dyskretyzacji zstępującej z kryterium zachłannym**, który maksymalizuje liczbę par obiektów o różnych etykietach (klasach) rozdzielonych przez podział.

---

## 🚀 Jak to działa?

Algorytm wykonuje następujące kroki:

1. **Wczytanie danych**: Plik CSV z danymi wejściowymi.
2. **Analiza atrybutu ciągłego**:
    - Generowanie wszystkich możliwych punktów podziału (średnich między unikalnymi wartościami).
    - Obliczanie liczby par obiektów z różnych klas, które zostają odseparowane dla każdego punktu.
    - Wybór punktu z maksymalnym "zyskiem" separacyjnym.
3. **Rekurencja**: Powtarzanie procesu w podprzedziałach, aż osiągnięta zostanie zadana liczba przedziałów (`n_bins`).
4. **Zapis wyniku**: Tworzenie nowego pliku CSV z dyskretyzowanymi wartościami.

---

## 🧪 Przykład

### Wejściowy plik CSV (`test_data_large.csv`):

```csv
distance,label
3.75,near
9.51,far
...
```

### Uruchomienie algorytmu (dla 3 przedziałów):

```bash
python main.py
```

### Wynik w terminalu:

```
2025-05-03 15:52:44 - INFO - Selected split 3.95 with gain 12
2025-05-03 15:52:44 - INFO - Selected split 7.8 with gain 12
...
```

### Wyjściowy plik CSV: `diskretized_test_data.csv`

---

## 🛠️ Struktura projektu

```
📂 Projekt
├── main.py                   # Główny plik uruchamiający algorytm
├── utils.py                  # Funkcje pomocnicze: logowanie, I/O, mierzenie czasu
├── test_data.csv             # Przykładowy mały zestaw danych
├── test_data_large.csv       # Wygenerowany większy zbiór danych do testów
├── diskretized_test_data.csv # Wynik działania algorytmu
```

---

## ⚙️ Jak używać?

1. Umieść swój plik CSV w folderze projektu.
2. Upewnij się, że kolumny `distance` i `label` istnieją (lub dostosuj swoje w kodzie `main.py`).
3. Uruchom algorytm:

    ```bash
    python main.py
    ```

4. Możesz zmienić liczbę przedziałów (`n_bins`) w funkcji `discretization_alg()`.

---

## 📄 Licencja

Projekt stworzony do celów edukacyjnych. Możesz go dowolnie modyfikować i używać. 🌱