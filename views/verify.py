_VERIFY_CACHE = {}

import streamlit as st

from nlp.preprocessing import clean_text, validate_input
from nlp.claim_extractor import extract_claims
from models.predictor import predict_news_detailed, predict_news
from utils.history_db import save_verification
from evidence.evidence_engine import collect_evidence
from evidence.evidence_analyzer import analyze_evidence
from evidence.verdict_engine import (
    calculate_claim_verdict,
    calculate_overall_verdict
)

def show():

    st.title("🔎 Verify News")

    st.write(
        "Analyze news using NLP, OCR, web evidence, "
        "source credibility and semantic verification."
    )

    st.divider()

    st.subheader("1. Choose your input")

    input_mode = st.radio(
        "Input type",
        [
            "📝 Paste Article",
            "📷 Upload Screenshot"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )

    article_text = ""

    if input_mode == "📝 Paste Article":

        st.subheader("Paste the news article or headline")

        article_text = st.text_area(
            "Article",
            placeholder=(
                "Paste the news headline, claim, or complete article here to verify..."
            ),
            height=260,
            label_visibility="collapsed"
        )

        st.caption(
            f"{len(article_text):,} characters"
        )

    else:

        st.subheader("Upload a screenshot")

        uploaded_image = st.file_uploader(
            "Upload an image containing news",
            type=[
                "png",
                "jpg",
                "jpeg",
                "webp"
            ]
        )

        if uploaded_image:

            image_col, info_col = st.columns(
                [1.2, 1]
            )

            with image_col:

                st.image(
                    uploaded_image,
                    caption="Uploaded image",
                    use_container_width=True
                )

            with info_col:

                st.info(
                    "OCR will extract the text from this image."
                )

                if st.button(
                    "📷 Extract Text",
                    use_container_width=True
                ):
                    with st.spinner(
                        "Extracting text..."
                    ):

                        try:
                            from ocr.ocr_engine import extract_text_from_image

                            extracted_text = (
                                extract_text_from_image(
                                    uploaded_image
                                )
                            )

                            cleaned_text = clean_text(
                                extracted_text
                            )

                            if cleaned_text:

                                st.session_state.extracted_text = (
                                    cleaned_text
                                )

                            else:

                                st.session_state.extracted_text = ""

                                st.warning(
                                    "No readable text was found in the image."
                                )

                        except Exception as error:

                            st.error(
                                f"OCR error: {error}"
                            )

        extracted_text = st.session_state.get(
            "extracted_text",
            ""
        )

        if extracted_text:

            st.subheader(
                "Extracted text"
            )

            st.text_area(
                "OCR result",
                value=extracted_text,
                height=220,
                disabled=True,
                label_visibility="collapsed"
            )

    st.divider()

    st.subheader(
        "2. Verification settings"
    )

    setting_col1, setting_col2, setting_col3 = st.columns(3)

    with setting_col1:

        search_depth = st.selectbox(
            "Evidence search depth",
            [
                "Standard",
                "Deep investigation"
            ]
        )

    with setting_col2:

        source_scope = st.selectbox(
            "Source scope",
            [
                "Trusted news + official sources",
                "News sources only",
                "Official sources only"
            ]
        )

    with setting_col3:

        decision_threshold = st.slider(
            "ML Decision Threshold",
            min_value=0.30,
            max_value=0.70,
            value=0.50,
            step=0.05,
            help="Probability cutoff for classifying text style as Real (Authentic). Default is 0.50."
        )

    st.divider()

    verify_clicked = st.button(
        "🔍 Verify This News",
        type="primary",
        use_container_width=True
    )

    if verify_clicked:

        raw_text = ""

        if input_mode == "📝 Paste Article":
            raw_text = article_text.strip()
        else:
            raw_text = st.session_state.get("extracted_text", "").strip()

        is_valid, validation_msg = validate_input(raw_text)

        if not is_valid:
            st.warning(f"⚠️ {validation_msg}")
        else:
            verification_text = clean_text(raw_text)

            with st.spinner(
                "Verifi is analyzing linguistic patterns and searching authoritative evidence..."
            ):

                model_result = predict_news_detailed(
                    verification_text,
                    threshold=decision_threshold
                )

                claims = extract_claims(
                    verification_text
                )

                if not claims and verification_text:
                    claims = [verification_text]

                claim_results = []

                for claim in claims:

                    try:
                        if search_depth == "Deep investigation":
                            evidence = collect_evidence(
                                claim,
                                max_results_per_query=8,
                                max_evidence=15,
                                deep=True,
                                source_scope=source_scope
                            )
                        else:
                            evidence = collect_evidence(
                                claim,
                                max_results_per_query=4,
                                max_evidence=8,
                                deep=False,
                                source_scope=source_scope
                            )
                    except Exception as err:
                        evidence = []

                    analyzed_evidence = analyze_evidence(
                        claim,
                        evidence
                    )

                    claim_verdict = calculate_claim_verdict(
                        analyzed_evidence
                    )

                    claim_model_res = predict_news_detailed(
                        claim,
                        threshold=decision_threshold
                    )

                    if claim_verdict.get("verdict") == "Contradicted":
                        claim_binary = "FAKE"
                    else:
                        claim_binary = "REAL"

                    claim_results.append(
                        {
                            "claim": claim,
                            "binary_verdict": claim_binary,
                            "verdict": claim_verdict["verdict"],
                            "confidence": claim_verdict["confidence"],
                            "support_score": claim_verdict["support_score"],
                            "contradiction_score": claim_verdict["contradiction_score"],
                            "supporting_sources": claim_verdict.get("supporting_sources", 0),
                            "contradicting_sources": claim_verdict.get("contradicting_sources", 0),
                            "independent_sources": claim_verdict.get("independent_sources", 0),
                            "model_prediction": claim_model_res.get("prediction", "Uncertain"),
                            "model_confidence": claim_model_res.get("confidence", 0.0),
                            "evidence": analyzed_evidence
                        }
                    )

                all_snippets = [
                    item.get("evidence_text", "")
                    for cres in claim_results
                    for item in cres.get("evidence", [])
                    if item.get("evidence_text")
                ]
                overall = calculate_overall_verdict(
                    claim_results,
                    raw_text=verification_text,
                    evidence_snippets=all_snippets
                )

            st.session_state.verification_input = verification_text
            st.session_state.prediction = model_result.get("prediction", "Uncertain")
            st.session_state.model_result = model_result
            st.session_state.claim_results = claim_results
            st.session_state.overall_verdict = overall

            save_verification(
                verification_text,
                overall,
                claim_results
            )
            st.session_state.verification_started = True

    if st.session_state.get(
        "verification_started",
        False
    ):

        model_result = st.session_state.get(
            "model_result",
            {}
        )

        claim_results = st.session_state.get(
            "claim_results",
            []
        )

        overall = st.session_state.get(
            "overall_verdict",
            {}
        )

        st.divider()

        st.header(
            "Verification Result"
        )

        overall_verdict = overall.get("verdict", "UNVERIFIED")
        overall_confidence = overall.get("confidence", 0.0)
        decision_basis = overall.get("decision_basis", "model")

        top_col1, top_col2 = st.columns([1.8, 1])

        with top_col1:
            if overall_verdict == "REAL":
                st.success("🟢 REAL")
                st.caption("Corroborated by independent authoritative sources.")
            else:
                st.error("🔴 FAKE")
                st.caption("Contradicted by verified sources or flagged as fabricated.")

        with top_col2:
            st.metric(
                "Confidence",
                f"{overall_confidence * 100:.1f}%"
            )

        st.info(
            "ℹ️ **Methodology & System Transparency:** "
            "Verifi combines a calibrated machine learning text classifier with live multi-source web evidence. "
            "A machine learning model analyzes stylistic and lexical patterns, but cannot independently verify "
            "real-time facts. Definitive factual truth is determined by authoritative corroborating sources."
        )

        st.subheader(
            "Claim Analysis"
        )

        for number, result in enumerate(
            claim_results,
            start=1
        ):

            with st.container(
                border=True
            ):

                st.markdown(
                    f"### Claim {number}"
                )

                st.write(
                    f"**Claim text:** {result['claim']}"
                )

                supporting = result.get(
                    "supporting_sources",
                    0
                )

                contradicting = result.get(
                    "contradicting_sources",
                    0
                )

                independent = result.get(
                    "independent_sources",
                    0
                )

                m1, m2, m3 = st.columns(3)

                with m1:
                    st.metric(
                        "Supporting Sources",
                        supporting
                    )

                with m2:
                    st.metric(
                        "Contradicting Sources",
                        contradicting
                    )

                with m3:
                    st.metric(
                        "Independent Publishers",
                        independent
                    )

                verdict = result.get(
                    "binary_verdict",
                    "UNVERIFIED"
                )

                confidence = result.get(
                    "confidence",
                    0.0
                )

                if verdict == "FAKE":
                    st.error(
                        f"🔴 FAKE (Flagged as misleading or contradictory — {confidence * 100:.1f}%)"
                    )
                else:
                    st.success(
                        f"🟢 REAL (Supported by authoritative reports — {confidence * 100:.1f}%)"
                    )

                evidence = result.get(
                    "evidence",
                    []
                )

                if not evidence:
                    st.caption(
                        "No relevant authoritative source passages were discovered for this claim."
                    )
                else:
                    st.write(f"**Discovered Evidence ({len(evidence)} sources):**")

                for evidence_number, item in enumerate(
                    evidence[:5],
                    start=1
                ):

                    with st.expander(
                        f"{evidence_number}. {item.get('title', 'Source')}"
                    ):

                        st.write(
                            f"**Domain:** `{item.get('domain', '')}` | "
                            f"**Category:** {item.get('source_type', 'Other')} | "
                            f"**Authority Score:** {item.get('source_score', 0)}/100"
                        )

                        relationship = item.get(
                            "relationship",
                            "neutral"
                        )
                        relationship_label = {
                            "entailment": "✅ Supports this claim",
                            "contradiction": "❌ Contradicts this claim"
                        }.get(
                            relationship,
                            "ℹ️ Neutral / No clear relation"
                        )

                        st.write(
                            f"**Evidence Relation:** {relationship_label}"
                        )

                        st.write(
                            f"**NLI Semantic Confidence:** "
                            f"{item.get('nli_confidence', 0) * 100:.1f}%"
                        )

                        passage = item.get(
                            "evidence_text",
                            ""
                        ) or item.get(
                            "description",
                            ""
                        )

                        if passage:
                            st.write(f"> {passage}")

                        url = item.get("url", "")
                        if url:
                            st.markdown(
                                f"[🔗 Open original source]({url})"
                            )

        st.subheader(
            "Analyzed Content"
        )

        with st.expander(
            "View analyzed text"
        ):

            st.write(
                st.session_state.get(
                    "verification_input",
                    ""
                )
            )
