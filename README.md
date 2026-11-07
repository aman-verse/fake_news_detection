# Verifi — AI-Powered Fake News Detection & Verification Platform

Verifi is a multi-tier Fake News Detection and Verification application built with Python and Streamlit. Unlike traditional systems that rely solely on surface-level keyword classification, Verifi combines **calibrated linguistic machine learning** with **live multi-source authoritative web evidence verification** and **Natural Language Inference (NLI)**.

---

## 🌟 Key Features

1. **Leak-Free Machine Learning Model:**
   - Trained on cleaned news articles with wire-service dateline leakage (e.g. `(Reuters) -`, `WASHINGTON (Reuters) -`) and scraping boilerplate explicitly stripped.
   - Uses a **Calibrated Linear Support Vector Classifier (Platt Scaling)** with TF-IDF representations (unigrams & bigrams, sublinear term frequency).
   - Generates calibrated probability estimates ($P(\text{Real})$ and $P(\text{Fake})$) rather than uncalibrated arbitrary scores.

2. **Configurable Decision Threshold & Uncertainty Handling:**
   - Adjustable decision threshold slider (0.30 to 0.70) in the user interface.
   - Built-in **Uncertain / Inconclusive category** for low-confidence predictions near the decision boundary.
   - Comprehensive input validation rejecting empty, degenerate, or purely numeric strings.

3. **Multi-Source Evidence Gathering:**
   - Automatically breaks articles into verifiable factual propositions.
   - Searches authoritative sources via DuckDuckGo:
     - Established global and national news agencies (Reuters, AP, BBC, The Hindu, etc.)
     - Official governmental and scientific institutions (NASA, NOAA, NIST, UN, WHO)
     - Independent fact-checking organizations (Snopes, PolitiFact, FactCheck.org)

4. **Semantic Natural Language Inference (NLI):**
   - Evaluates retrieved source passages against claims using `cross-encoder/nli-MiniLM2-L6-H768`.
   - Classifies relationships as **Entailment (Supports)**, **Contradiction**, or **Neutral**.

5. **Optical Character Recognition (OCR):**
   - Built-in screenshot and poster text extraction powered by EasyOCR.

6. **Full Verification History:**
   - Local SQLite database logging past investigations, claim breakdowns, and evidence metrics.

---

## 📊 Model Evaluation Results

Evaluation performed on a held-out test partition of 2,000 independent articles:

| Metric | Score |
| :--- | :--- |
| **Accuracy** | **96.30%** |
| **Precision (Macro Avg)** | **96.28%** |
| **Recall (Macro Avg)** | **96.30%** |
| **F1-Score (Macro Avg)** | **96.29%** |
| **ROC-AUC** | **98.93%** |
| **Brier Calibration Score** | **0.0262** *(lower is better calibrated)* |

### Confusion Matrix

| | Predicted Fake | Predicted Real | Total |
| :--- | :---: | :---: | :---: |
| **Actual Fake** | 912 | 35 | 947 |
| **Actual Real** | 39 | 1014 | 1053 |

---

## 🚀 Running on Windows

### 1. Prerequisites
- Python 3.10 – 3.13 (64-bit)
- PowerShell or Windows Command Prompt

### 2. Environment Setup
```powershell
# Navigate to the project root
cd "C:\path\to\Verifi"

# Activate your virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Launch Application
```powershell
# Launch Streamlit app
streamlit run app.py
```
Open `http://localhost:8501` in your web browser.

---

## ⚠️ Important Limitations & Ethical Transparency

- **Stylistic vs. Factual Assessment:** The machine learning model analyzes writing style, rhetoric, and lexical patterns. An isolated NLP model cannot determine real-time worldly truth or verify breaking news events without external corroboration.
- **Evidence Dependence:** Authoritative verification relies on live web queries. If an obscure claim has no published reporting, Verifi flags it as **UNVERIFIED / INCONCLUSIVE** rather than forcing a misleading binary verdict.
- **OCR Quality:** Image text extraction depends on screenshot resolution and typography. Clean, high-contrast images yield optimal results.


