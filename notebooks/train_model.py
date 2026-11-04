import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import sys
import re
import time
import json
import gc
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    brier_score_loss,
    classification_report,
    confusion_matrix
)

def clean_news_text(text: str) -> str:
    if not text or not isinstance(text, str):
        return ""
    
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    
    text = re.sub(r"<.*?>", " ", text)
    
    text = re.sub(r"^[A-Z\s,]+(?:\s*\([A-Za-z\s]+\)\s*)?\s*[-–—]{1,2}\s*", " ", text)
    
    text = re.sub(r"\(reuters\)", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\breuters\b", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bassociated press\b", " ", text, flags=re.IGNORECASE)
    
    text = re.sub(r"\[(?:video|image|photo|audio|graphic)\]", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\((?:video|image|photo|audio|graphic)\)", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bfeatured image via\b.*", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bimage via\b.*", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bread more:?.*", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bwatch (?:the )?video\b.*", " ", text, flags=re.IGNORECASE)
    
    text = re.sub(r"\s+", " ", text)
    
    return text.strip().lower()

def load_dataset_split(filename: str, max_samples=None):
    print(f"Loading {filename} (max={max_samples})...")
    path = hf_hub_download("GonzaloA/fake_news", filename=filename, repo_type="dataset")
    pf = pq.ParquetFile(path)
    
    texts = []
    labels = []
    
    for batch in pf.iter_batches(batch_size=1000, columns=["title", "text", "label"]):
        d = batch.to_pydict()
        for ttl, txt, lbl in zip(d["title"], d["text"], d["label"]):
            sub_txt = str(txt or "")[:800]
            clean = clean_news_text(str(ttl or "") + " " + sub_txt)
            if clean:
                texts.append(clean)
                labels.append(int(lbl))
            if max_samples and len(texts) >= max_samples:
                break
        if max_samples and len(texts) >= max_samples:
            break
                
    return texts, np.array(labels, dtype=int)

def main():
    print("=" * 70)
    print("VERIFI ML PIPELINE TRAINING & BENCHMARKING")
    print("=" * 70)
    
    X_train_raw, y_train = load_dataset_split("data/train-00000-of-00001.parquet", max_samples=10000)
    print(f"Train set: {len(X_train_raw)} articles (Class 0: {(y_train == 0).sum()}, Class 1: {(y_train == 1).sum()})")
    
    print("\nFitting TF-IDF Vectorizer on training data...")
    t0 = time.time()
    vectorizer = TfidfVectorizer(
        max_features=15000,
        ngram_range=(1, 2),
        sublinear_tf=True,
        min_df=3,
        max_df=0.85
    )
    X_train = vectorizer.fit_transform(X_train_raw)
    del X_train_raw
    gc.collect()
    print(f"TF-IDF feature matrix created in {time.time()-t0:.2f}s. Shape: {X_train.shape}")
    
    X_val_raw, y_val = load_dataset_split("data/validation-00000-of-00001.parquet", max_samples=2000)
    print(f"Val set:   {len(X_val_raw)} articles (Class 0: {(y_val == 0).sum()}, Class 1: {(y_val == 1).sum()})")
    X_val = vectorizer.transform(X_val_raw)
    del X_val_raw
    gc.collect()
    
    candidates = {
        "Calibrated LinearSVC (Platt Scaling)": CalibratedClassifierCV(
            LinearSVC(C=1.0, random_state=42),
            method="sigmoid",
            cv=3
        ),
        "Logistic Regression (C=2.0)": LogisticRegression(
            C=2.0,
            max_iter=1000,
            class_weight="balanced",
            solver="liblinear",
            random_state=42
        ),
        "Multinomial Naive Bayes (alpha=0.1)": MultinomialNB(
            alpha=0.1
        )
    }
    
    results = {}
    best_model_name = None
    best_f1 = -1.0
    
    print("\n" + "=" * 70)
    print("MODEL COMPARISON ON VALIDATION SET")
    print("=" * 70)
    
    for name, model in candidates.items():
        print(f"\nTraining {name}...")
        t_start = time.time()
        model.fit(X_train, y_train)
        train_time = time.time() - t_start
        
        val_pred = model.predict(X_val)
        val_proba = model.predict_proba(X_val)[:, 1] if hasattr(model, "predict_proba") else None
        
        acc = accuracy_score(y_val, val_pred)
        prec = precision_score(y_val, val_pred)
        rec = recall_score(y_val, val_pred)
        f1 = f1_score(y_val, val_pred)
        roc = roc_auc_score(y_val, val_proba) if val_proba is not None else 0.0
        brier = brier_score_loss(y_val, val_proba) if val_proba is not None else 1.0
        
        results[name] = {
            "model": model,
            "train_time": train_time,
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1": f1,
            "roc_auc": roc,
            "brier_score": brier
        }
        
        print(f"Results for {name}:")
        print(f"  Training Time: {train_time:.2f}s")
        print(f"  Accuracy:      {acc*100:.2f}%")
        print(f"  Precision:     {prec*100:.2f}%")
        print(f"  Recall:        {rec*100:.2f}%")
        print(f"  F1 Score:      {f1*100:.2f}%")
        print(f"  ROC-AUC:       {roc*100:.2f}%")
        print(f"  Brier Score:   {brier:.4f} (lower is better calibrated)")
        
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            
    print("\n" + "=" * 70)
    print(f"SELECTED BEST MODEL: {best_model_name} (Validation F1: {best_f1*100:.2f}%)")
    print("=" * 70)
    
    best_model = results[best_model_name]["model"]
    
    del X_val, y_val
    gc.collect()
    
    X_test_raw, y_test = load_dataset_split("data/test-00000-of-00001.parquet", max_samples=2000)
    print(f"\nTest set:  {len(X_test_raw)} articles (Class 0: {(y_test == 0).sum()}, Class 1: {(y_test == 1).sum()})")
    X_test = vectorizer.transform(X_test_raw)
    del X_test_raw
    gc.collect()
    
    print("\n" + "=" * 70)
    print("EVALUATION ON HELD-OUT TEST SET (2,000 articles)")
    print("=" * 70)
    
    test_pred = best_model.predict(X_test)
    test_proba = best_model.predict_proba(X_test)[:, 1]
    
    test_acc = accuracy_score(y_test, test_pred)
    test_prec = precision_score(y_test, test_pred)
    test_rec = recall_score(y_test, test_pred)
    test_f1 = f1_score(y_test, test_pred)
    test_roc = roc_auc_score(y_test, test_proba)
    test_cm = confusion_matrix(y_test, test_pred)
    
    print(f"\nTest Accuracy:  {test_acc*100:.2f}%")
    print(f"Test Precision: {test_prec*100:.2f}%")
    print(f"Test Recall:    {test_rec*100:.2f}%")
    print(f"Test F1 Score:  {test_f1*100:.2f}%")
    print(f"Test ROC-AUC:   {test_roc*100:.2f}%")
    
    print("\nConfusion Matrix (Rows: True [Fake, Real], Cols: Predicted [Fake, Real]):")
    print(test_cm)
    print(f"  True Fake  correctly predicted: {test_cm[0, 0]} / {(y_test == 0).sum()}")
    print(f"  False Real (Fake called Real):  {test_cm[0, 1]}")
    print(f"  False Fake (Real called Fake):  {test_cm[1, 0]}")
    print(f"  True Real  correctly predicted: {test_cm[1, 1]} / {(y_test == 1).sum()}")
    
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, test_pred, target_names=["Fake (0)", "Real (1)"], digits=4))
    
    print("\n" + "=" * 70)
    print("INSPECTING TOP LEARNED FEATURES (Linguistic Verification)")
    print("=" * 70)
    
    feature_names = np.array(vectorizer.get_feature_names_out())
    if hasattr(best_model, "coef_"):
        weights = best_model.coef_[0]
    elif hasattr(best_model, "calibrated_classifiers_"):
        weights = np.mean([clf.estimator.coef_[0] for clf in best_model.calibrated_classifiers_], axis=0)
    else:
        weights = None
        
    if weights is not None:
        top_real_idx = np.argsort(weights)[-25:][::-1]
        top_fake_idx = np.argsort(weights)[:25]
        
        print("\nTop 25 REAL (Class 1) Indicators:")
        for idx in top_real_idx:
            print(f"  +{weights[idx]:.4f} : {feature_names[idx]}")
            
        print("\nTop 25 FAKE (Class 0) Indicators:")
        for idx in top_fake_idx:
            print(f"  {weights[idx]:.4f} : {feature_names[idx]}")
            
    output_dir = PROJECT_ROOT / "models"
    output_dir.mkdir(exist_ok=True)
    
    model_path = output_dir / "fake_news_model.pkl"
    vec_path = output_dir / "tfidf_vectorizer.pkl"
    meta_path = output_dir / "model_metadata.json"
    
    joblib.dump(best_model, model_path)
    joblib.dump(vectorizer, vec_path)
    
    metadata = {
        "model_name": best_model_name,
        "vectorizer_type": "TfidfVectorizer",
        "ngram_range": [1, 2],
        "max_features": 15000,
        "classes": ["Fake", "Real"],
        "class_mapping": {"0": "Fake", "1": "Real"},
        "test_metrics": {
            "accuracy": round(float(test_acc), 4),
            "precision": round(float(test_prec), 4),
            "recall": round(float(test_rec), 4),
            "f1_score": round(float(test_f1), 4),
            "roc_auc": round(float(test_roc), 4),
            "confusion_matrix": test_cm.tolist()
        },
        "training_samples": int(X_train.shape[0]),
        "validation_samples": 2000,
        "test_samples": int(X_test.shape[0]),
        "trained_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
        
    print(f"\nArtifacts successfully saved to {output_dir}:")
    print(f"  - Model:      {model_path} ({model_path.stat().st_size / 1024:.1f} KB)")
    print(f"  - Vectorizer: {vec_path} ({vec_path.stat().st_size / (1024*1024):.1f} MB)")
    print(f"  - Metadata:   {meta_path}")
    print("\nTraining completed successfully!")

if __name__ == "__main__":
    main()
