import streamlit as st

def show():

    st.title("ℹ️ About Verifi")

    st.write(
        "Verifi is an AI-powered fake news verification platform designed to combine "
        "calibrated linguistic machine learning with multi-source authoritative web evidence."
    )

    st.divider()

    st.subheader("🏛️ System Architecture")

    st.markdown(
        """
        Verifi operates on an **Evidence-First Multi-Tier Pipeline**:
        
        1. **Input Normalization & Guardrails:** Validates submitted text or extracts clean text from screenshots using Optical Character Recognition (EasyOCR). Rejects empty, purely numerical, or degenerate input.
        2. **Leak-Free Linguistic Machine Learning:** Analyzes text styling, sensationalist vocabulary, and clickbait patterns using a calibrated Linear Support Vector Classifier with TF-IDF representations. Wire dateline leakage has been stripped so the model does not rely on memorized publisher tags.
        3. **Claim Decomposition:** Isolates distinct factual propositions from the article or headline for targeted investigation.
        4. **Multi-Source Evidence Retrieval:** Queries trusted news organizations (Reuters, AP, BBC, The Hindu, etc.), official scientific/government bodies (NASA, NOAA, NIST, UN), and independent fact-checkers (Snopes, PolitiFact, FactCheck.org) via DuckDuckGo.
        5. **Natural Language Inference (NLI):** Uses a cross-encoder model (`cross-encoder/nli-MiniLM2-L6-H768`) alongside deterministic domain rules to evaluate whether retrieved source passages *Entail*, *Contradict*, or are *Neutral* toward each claim.
        6. **Synthesized Verdict & Confidence:** Computes source-weighted evidence corroboration and produces an explainable, transparent assessment.
        """
    )

    st.divider()

    st.subheader("🛡️ Machine Learning Limitations & Transparency")

    st.info(
        """
        **Critical Distinction: Linguistic Prediction vs. Factual Verification**
        
        - **What the ML Model Does:** Evaluates writing style, lexical frequency, and rhetorical framing. It estimates the likelihood that a text exhibits the linguistic characteristics of authentic journalism versus fabricated news.
        - **What the ML Model Cannot Do:** An isolated natural language processing model has no real-time awareness of ongoing worldly events. It cannot independently determine whether a historical fact, election outcome, or breaking news development is factually true.
        - **How Verifi Resolves This:** Verifi does not force an unsubstantiated binary decision when evidence is lacking. When external sources cannot be found, Verifi marks the claim as **UNVERIFIED / INCONCLUSIVE**, clearly showing the model's stylistic confidence while emphasizing the need for corroborating primary reporting.
        """
    )

    st.divider()

    st.subheader("📋 Specifications & Credits")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            - **Platform Version:** 1.1 (Production-Ready)
            - **Classifier:** Calibrated LinearSVC (Platt Scaling)
            - **Text Vectorizer:** TF-IDF (15,000 features, Unigrams & Bigrams)
            - **Semantic NLI:** Cross-Encoder MiniLM-L6
            - **OCR Engine:** EasyOCR (Deep Learning Text Detection)
            """
        )

    with c2:
        st.markdown(
            """
            - **Developer:** Satyam Verma
            - **Institution:** BIT Mesra
            - **Framework:** Python, Streamlit, Scikit-Learn, PyTorch
            - **Deployment Target:** Windows / Linux / macOS
            """
        )
