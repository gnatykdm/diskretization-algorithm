# 🌟 Continuous Attribute Discretization Algorithm

Implementation of a **top-down discretization algorithm with a greedy criterion**, which maximizes the number of object pairs with different labels (classes) separated by the split.

---

## 🚀 How does it work?

The algorithm performs the following steps:

1. **Data loading**: Input CSV file.
2. **Continuous attribute analysis**:
    - Generate all possible split points (averages between unique values).
    - Calculate the number of object pairs from different classes that are separated for each split point.
    - Select the split point with the maximum "separation gain."
3. **Recursion**: Repeat the process in subintervals until the desired number of intervals (`n_bins`) is reached.
4. **Save the result**: Create a new CSV file with discretized values.

---

## 🧪 Example

### Input CSV file (`test_data_large.csv`):

```csv
distance,label
3.75,near
9.51,far
...
```

### Running the algorithm (for 3 intervals):

```bash
python main.py
```

### Terminal output:

```
2025-05-03 15:52:44 - INFO - Selected split 3.95 with gain 12
2025-05-03 15:52:44 - INFO - Selected split 7.8 with gain 12
...
```

### Output CSV file: `diskretized_test_data.csv`

---

## 🛠️ Project structure

```
📂 Project
├── main.py                   # Main file to run the algorithm
├── utils.py                  # Helper functions: logging, I/O, timing
├── test_data.csv             # Example small dataset
├── test_data_large.csv       # Generated larger dataset for testing
├── diskretized_test_data.csv # Algorithm output
```

---

## ⚙️ How to use?

1. Place your CSV file in the project folder.
2. Ensure the `distance` and `label` columns exist (or adjust them in `main.py`).
3. Run the algorithm:

    ```bash
    python main.py
    ```

4. You can change the number of intervals (`n_bins`) in the `discretization_alg()` function.

---

## 📄 License

Project created for educational purposes. You are free to modify and use it. 🌱