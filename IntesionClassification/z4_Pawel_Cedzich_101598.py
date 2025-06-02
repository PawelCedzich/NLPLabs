import json
import csv
import random
import numpy as np

from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import LabelEncoder


def seed_everything(seed=42):
    random.seed(seed)
    np.random.seed(seed)


def load_data(json_path: str):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Diagnostyka formatu pliku JSON
    if isinstance(data, list):
        print("BŁĄD: Plik JSON jest listą, a nie słownikiem. Przykładowy element:", data[0])
        raise ValueError("Plik JSON powinien być słownikiem z kluczami: 'train', 'val', 'test', 'oos_test', a nie listą!")

    if not all(k in data for k in ["train", "val", "test", "oos_test"]):
        print("BŁĄD: Brakuje wymaganych kluczy w pliku JSON. Klucze znalezione:", list(data.keys()))
        raise ValueError("Plik JSON musi zawierać klucze: 'train', 'val', 'test', 'oos_test'.")

    # Dodaj diagnostykę zawartości split
    def extract(split):
        # Obsługa listy list [text, intent]
        if not isinstance(split, list):
            print("BŁĄD: Oczekiwano listy, otrzymano:", type(split), "Zawartość:", split)
            raise ValueError("Każdy split (train/val/test/oos_test) powinien być listą!")
        if not all(isinstance(item, (list, dict)) for item in split):
            print("BŁĄD: Oczekiwano listy list lub słowników, przykładowy element:", split[0])
            raise ValueError("Każdy split powinien być listą dwuelementowych list lub słowników!")
        # Obsługa obu formatów
        if all(isinstance(item, dict) for item in split):
            texts = [item["text"] for item in split]
            intents = [item["intent"] for item in split]
        elif all(isinstance(item, list) and len(item) == 2 for item in split):
            texts = [item[0] for item in split]
            intents = [item[1] for item in split]
        else:
            print("BŁĄD: Split zawiera nieobsługiwany format, przykładowy element:", split[0])
            raise ValueError("Split powinien być listą słowników lub listą dwuelementowych list!")
        return texts, intents

    train_texts, train_labels = extract(data["train"])
    val_texts, val_labels = extract(data["val"])
    test_texts, test_labels = extract(data["test"])
    oos_texts, oos_labels = extract(data.get("oos_test", data.get("oos_val", [])))

    return train_texts, train_labels, val_texts, val_labels, test_texts, test_labels, oos_texts, oos_labels


def save_predictions(texts: List[str], predictions: List[str], path: str):
    with open(path, mode="w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "predicted"])
        writer.writeheader()
        for text, pred in zip(texts, predictions):
            writer.writerow({"text": text, "predicted": pred})


def save_metrics(y_true: List[str], y_pred: List[str], path: str):
    accuracy = accuracy_score(y_true, y_pred)
    precision_macro = precision_score(y_true, y_pred, average="macro", zero_division=0)
    recall_macro = recall_score(y_true, y_pred, average="macro", zero_division=0)
    f1_macro = f1_score(y_true, y_pred, average="macro", zero_division=0)

    precision_weighted = precision_score(y_true, y_pred, average="weighted", zero_division=0)
    recall_weighted = recall_score(y_true, y_pred, average="weighted", zero_division=0)
    f1_weighted = f1_score(y_true, y_pred, average="weighted", zero_division=0)

    # In-scope accuracy (bez OOS)
    in_scope_idx = [i for i, label in enumerate(y_true) if label != "oos"]
    if in_scope_idx:
        in_scope_true = [y_true[i] for i in in_scope_idx]
        in_scope_pred = [y_pred[i] for i in in_scope_idx]
        in_scope_accuracy = accuracy_score(in_scope_true, in_scope_pred)
    else:
        in_scope_accuracy = None

    # OOS recall (procent prawdziwych OOS rozpoznanych jako OOS)
    oos_idx = [i for i, label in enumerate(y_true) if label == "oos"]
    if oos_idx:
        oos_true = [y_true[i] for i in oos_idx]
        oos_pred = [y_pred[i] for i in oos_idx]
        # policz ile z oos_true zostało poprawnie rozpoznanych jako "oos"
        oos_correct = sum(1 for t, p in zip(oos_true, oos_pred) if p == "oos")
        oos_recall = oos_correct / len(oos_true) if oos_true else 0.0
    else:
        oos_recall = None

    fieldnames = [
        "accuracy",
        "precision_macro", "recall_macro", "f1_macro",
        "precision_weighted", "recall_weighted", "f1_weighted",
        "in_scope_accuracy", "oos_recall"
    ]
    with open(path, mode="w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
            "accuracy": round(accuracy, 4),
            "precision_macro": round(precision_macro, 4),
            "recall_macro": round(recall_macro, 4),
            "f1_macro": round(f1_macro, 4),
            "precision_weighted": round(precision_weighted, 4),
            "recall_weighted": round(recall_weighted, 4),
            "f1_weighted": round(f1_weighted, 4),
            "in_scope_accuracy": round(in_scope_accuracy, 4) if in_scope_accuracy is not None else "",
            "oos_recall": round(oos_recall, 4) if oos_recall is not None else ""
        })

def solution(
    json_path: str,
    predictions_csv_path: str,
    metrics_csv_path: str
) -> None:
    seed_everything(42)

    # Wczytaj dane
    train_texts, train_labels, val_texts, val_labels, test_texts, test_labels, oos_texts, oos_labels = load_data(json_path)

    # Połącz dane treningowe i walidacyjne
    all_train_texts = train_texts + val_texts
    all_train_labels = train_labels + val_labels

    # LabelEncoder (obsługuje OOS również)
    label_encoder = LabelEncoder()
    label_encoder.fit(all_train_labels + test_labels)  # nie kodujemy OOS jako label!

    y_train = label_encoder.transform(all_train_labels)
    y_test = label_encoder.transform(test_labels)

    # Wektoryzacja TF-IDF
    vectorizer = TfidfVectorizer()
    X_train = vectorizer.fit_transform(all_train_texts)
    X_test = vectorizer.transform(test_texts)
    X_oos = vectorizer.transform(oos_texts)

    # Trening modelu
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)

    # Predykcje
    y_pred_test = clf.predict(X_test)
    y_pred_test_labels = label_encoder.inverse_transform(y_pred_test)

    # OOS (traktujemy osobno)
    y_pred_oos = clf.predict(X_oos)
    y_pred_oos_labels = label_encoder.inverse_transform(y_pred_oos)

    # Zastępujemy predykcje na OOS etykietą "oos", jeśli model przewidział etykietę spoza 150 klas
    known_classes = set(label_encoder.classes_)
    final_oos_pred = ["oos" if pred not in known_classes else pred for pred in y_pred_oos_labels]

    # Połącz dane
    all_texts = test_texts + oos_texts
    all_predictions = list(y_pred_test_labels) + final_oos_pred
    all_true_labels = test_labels + ["oos"] * len(oos_labels)

    # Zapisz pliki wynikowe w folderze roboczym
    save_predictions(all_texts, all_predictions, predictions_csv_path)
    save_metrics(all_true_labels, all_predictions, metrics_csv_path)


# Przykładowe ścieżki do plików:
# json_path = r"C:\Users\cedpa\OneDrive\Documents\GitHub\oos-eval\data\data_full.json"
# predictions_csv_path = "predictions_JAN_KOWALSKI_123456.csv"
# metrics_csv_path = "results_JAN_KOWALSKI_123456.csv"

# Przykład wywołania:
solution(
    r"C:\Users\cedpa\OneDrive\Documents\GitHub\oos-eval\data\data_full.json",
    "predictions_pawel_Cedzich_101598.csv",
    "results_Pawel_Cedzich_101598.csv"
)
