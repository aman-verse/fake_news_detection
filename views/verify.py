import streamlit as st

from nlp.preprocessing import clean_text
from nlp.claim_extractor import extract_claims
from models.predictor import predict_news
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

    # =========================================================
    # INPUT
    # =========================================================

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

    # =========================================================
    # TEXT
    # =========================================================

    if input_mode == "📝 Paste Article":

        st.subheader("Paste the news article")

        article_text = st.text_area(
            "Article",
            placeholder=(
                "Paste the complete news article or claim here..."
            ),
            height=280,
            label_visibility="collapsed"
        )

        st.caption(
            f"{len(article_text):,} characters"
        )

    # =========================================================
    # IMAGE
    # =========================================================

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
                    "OCR will extract the text "
                    "from this image."
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
                                    "No readable text was found."
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

    # =========================================================
    # SETTINGS
    # =========================================================

    st.subheader(
        "2. Verification settings"
    )

    setting_col1, setting_col2 = st.columns(2)

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

    st.divider()

    # =========================================================
    # VERIFY
    # =========================================================

    verify_clicked = st.button(
        "🔍 Verify This News",
        type="primary",
        use_container_width=True
    )

    if verify_clicked:

        verification_text = ""

        # -----------------------------------------------------
        # GET TEXT
        # -----------------------------------------------------

        if input_mode == "📝 Paste Article":

            if article_text.strip():

                verification_text = clean_text(
                    article_text
                )

            else:

                st.warning(
                    "Please paste an article first."
                )

        else:

            verification_text = st.session_state.get(
                "extracted_text",
                ""
            )

            if not verification_text:

                st.warning(
                    "Please extract text from the image first."
                )

        # -----------------------------------------------------
        # RUN COMPLETE PIPELINE
        # -----------------------------------------------------

        if verification_text:

            with st.spinner(
                "Verifi is analyzing the claim and searching evidence..."
            ):

                # =============================================
                # 1. MODEL PREDICTION
                # =============================================

                prediction = predict_news(
                    verification_text
                )

                # =============================================
                # 2. CLAIM EXTRACTION
                # =============================================

                claims = extract_claims(
                    verification_text
                )
                print("\n" + "=" * 70)
                print("VERIFI ACTUAL IMAGE CLAIMS")
                print("=" * 70)

                for i, claim in enumerate(claims, 1):
                    print(f"CLAIM {i}: {claim}")
                    
                claim_results = []

                # =============================================
                # 3. EVIDENCE FOR EACH CLAIM
                # =============================================

                for claim in claims:

                    if search_depth == "Deep investigation":

                        evidence = collect_evidence(
                            claim,
                            max_results_per_query=10,
                            max_evidence=20,
                            deep=True,
                            source_scope=source_scope
                        )

                    else:

                        evidence = collect_evidence(
                            claim,
                            max_results_per_query=5,
                            max_evidence=10,
                            deep=False,
                            source_scope=source_scope
                        )

                    # =========================================
                    # 4. NLI
                    # =========================================

                    analyzed_evidence = analyze_evidence(
                        claim,
                        evidence
                    )

                    # =========================================
                    # 5. CLAIM VERDICT
                    # =========================================

                    claim_verdict = calculate_claim_verdict(
                        analyzed_evidence
                    )

                    if claim_verdict["verdict"] == "Supported":
                        binary_claim_verdict = "REAL"
                    elif claim_verdict["verdict"] == "Contradicted":
                        binary_claim_verdict = "FAKE"
                    else:
                        binary_claim_verdict = predict_news(
                            claim
                        ).upper()

                    claim_results.append(
                        {
                            "claim": claim,

                            "binary_verdict": binary_claim_verdict,

                            "verdict": claim_verdict[
                                "verdict"
                            ],

                            "confidence": claim_verdict[
                                "confidence"
                            ],

                            "support_score": claim_verdict[
                                "support_score"
                            ],

                            "contradiction_score": claim_verdict[
                                "contradiction_score"
                            ],

                            "supporting_sources": claim_verdict.get(
                                "supporting_sources",
                                0
                            ),

                            "contradicting_sources": claim_verdict.get(
                                "contradicting_sources",
                                0
                            ),

                            "independent_sources": claim_verdict.get(
                                "independent_sources",
                                0
                            ),

                            "evidence": analyzed_evidence
                        }
                    )

                # =============================================
                # 6. OVERALL VERDICT
                # =============================================

                overall = calculate_overall_verdict(
                    claim_results,
                    prediction
                )

            # -------------------------------------------------
            # SAVE RESULT
            # -------------------------------------------------

            st.session_state.verification_input = (
                verification_text
            )

            st.session_state.prediction = (
                prediction
            )

            st.session_state.claim_results = (
                claim_results
            )

            st.session_state.overall_verdict = (
                overall
            )


            save_verification(
                verification_text,
                overall,
                claim_results
            )
            st.session_state.verification_started = True

    # =========================================================
    # RESULTS
    # =========================================================

    if st.session_state.get(
        "verification_started",
        False
    ):

        prediction = st.session_state.get(
            "prediction",
            None
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

        # =====================================================
        # OVERALL VERDICT
        # =====================================================

        overall_verdict = overall.get(
            "verdict",
            prediction.upper() if prediction else "FAKE"
        )

        if overall_verdict not in {
            "REAL",
            "FAKE"
        }:
            overall_verdict = (
                prediction.upper()
                if prediction
                else "FAKE"
            )

        overall_confidence = overall.get(
            "confidence",
            0.0
        )

        if overall_verdict == "REAL":

            st.success(
                "🟢 REAL"
            )

        else:

            st.error(
                "🔴 FAKE"
            )

        st.metric(
            "Evidence Confidence",
            f"{overall_confidence * 100:.1f}%"
        )

        if overall.get("decision_basis") == "model":
            st.caption(
                "Source evidence was unavailable or evenly balanced; "
                "the classifier supplied the binary verdict."
            )


        # =====================================================
        # CLAIMS
        # =====================================================

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
                    result["claim"]
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
                        "Supporting",
                        supporting
                    )

                with m2:

                    st.metric(
                        "Contradicting",
                        contradicting
                    )

                with m3:

                    st.metric(
                        "Independent Sources",
                        independent
                    )
                
                verdict = result.get(
                    "binary_verdict"
                )

                if verdict not in {
                    "REAL",
                    "FAKE"
                }:
                    evidence_verdict = result.get(
                        "verdict"
                    )
                    if evidence_verdict == "Supported":
                        verdict = "REAL"
                    elif evidence_verdict == "Contradicted":
                        verdict = "FAKE"
                    else:
                        verdict = predict_news(
                            result["claim"]
                        ).upper()

                confidence = result[
                    "confidence"
                ]

                if verdict == "REAL":

                    st.success(
                        f"🟢 REAL — "
                        f"{confidence * 100:.1f}%"
                    )

                else:

                    st.error(
                        f"🔴 FAKE — "
                        f"{confidence * 100:.1f}%"
                    )

                # =================================================
                # EVIDENCE
                # =================================================

                st.write(
                    "Evidence"
                )

                evidence = result.get(
                    "evidence",
                    []
                )

                if not evidence:
                    st.info(
                        "No relevant source passages were found for this claim."
                    )

                for evidence_number, item in enumerate(
                    evidence[:5],
                    start=1
                ):

                    with st.expander(
                        f"{evidence_number}. "
                        f"{item.get('title', 'Source')}"
                    ):

                        st.write(
                            f"**Source:** "
                            f"{item.get('domain', '')}"
                        )

                        st.write(
                            f"**Type:** "
                            f"{item.get('source_type', '')}"
                        )

                        relationship = item.get(
                            "relationship",
                            "neutral"
                        )
                        relationship_label = {
                            "entailment": "Supports this claim",
                            "contradiction": "Contradicts this claim"
                        }.get(
                            relationship,
                            "No clear relation"
                        )

                        st.write(
                            f"**Relation:** {relationship_label}"
                        )

                        st.write(
                            f"**NLI confidence:** "
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
                            st.write(passage)

                        st.markdown(
                            f"[Open source]({item.get('url', '')})"
                        )

        if not claim_results:
            st.info(
                "No claims or source passages were available; "
                "the binary result uses the article classifier."
            )

        # =====================================================
        # ANALYZED CONTENT
        # =====================================================

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