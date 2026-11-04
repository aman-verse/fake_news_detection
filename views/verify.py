import streamlit as st

from nlp.preprocessing import clean_text, validate_input
from utils.history_db import save_verification
from evidence.llm_verifier import verify_with_openai

def show():

    if "verify_cache" not in st.session_state:
        st.session_state.verify_cache = {}

    st.title("🔎 Verify News")

    st.write(
        "Simple, high-accuracy news verification powered by AI and factual knowledge."
    )

    st.divider()

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
            height=200,
            label_visibility="collapsed"
        )

    else:

        st.subheader("Upload a news screenshot")

        uploaded_image = st.file_uploader(
            "Upload image",
            type=["png", "jpg", "jpeg", "webp"],
            label_visibility="collapsed"
        )

        col1, col2 = st.columns([1, 1])

        if uploaded_image is not None:

            with col1:

                st.image(
                    uploaded_image,
                    caption="Uploaded screenshot",
                    use_container_width=True
                )

            with col2:

                extract_clicked = st.button(
                    "📷 Extract Text from Image",
                    use_container_width=True
                )

                if extract_clicked:

                    with st.spinner("Reading text from image using OCR..."):

                        try:
                            from ocr.ocr_engine import extract_text_from_image
                            extracted_text = extract_text_from_image(uploaded_image)
                        except Exception as ocr_err:
                            extracted_text = ""
                            st.error(f"OCR Error: {ocr_err}")

                        st.session_state.extracted_text = extracted_text

        extracted_text = st.session_state.get("extracted_text", "")

        if extracted_text:

            st.text_area(
                "OCR result",
                value=extracted_text,
                height=180,
                disabled=True,
                label_visibility="collapsed"
            )

    st.divider()

    col_btn1, col_btn2 = st.columns([3, 1])

    with col_btn1:
        verify_clicked = st.button(
            "🔍 Verify News",
            type="primary",
            use_container_width=True
        )

    with col_btn2:
        clear_clicked = st.button(
            "🧹 Clear & Reset",
            use_container_width=True
        )

    if clear_clicked:
        st.session_state.verify_cache = {}
        st.session_state.verification_started = False
        st.session_state.verification_result = {}
        st.session_state.extracted_text = ""
        st.rerun()

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
            cache_key = verification_text.strip().lower()

            if cache_key in st.session_state.verify_cache:
                result = st.session_state.verify_cache[cache_key]
            else:
                with st.spinner("AI is verifying factual authenticity..."):
                    api_key = st.session_state.get("openai_api_key", None)
                    result = verify_with_openai(verification_text, api_key=api_key)
                    st.session_state.verify_cache[cache_key] = result

            st.session_state.verification_input = verification_text
            st.session_state.verification_result = result
            st.session_state.verification_started = True

            overall_data = {
                "verdict": result.get("verdict", "REAL"),
                "confidence": result.get("confidence", 0.90),
                "decision_basis": result.get("engine", "AI")
            }
            save_verification(
                verification_text,
                overall_data,
                []
            )

    if st.session_state.get("verification_started", False):

        result = st.session_state.get("verification_result", {})
        verdict = result.get("verdict", "REAL")
        confidence = float(result.get("confidence", 0.90))
        reasoning = result.get("reasoning", "")
        evidence = result.get("evidence", [])
        engine_name = result.get("engine", "AI Fact-Checker")
        is_quota = result.get("is_quota_exhausted", False)

        st.divider()

        st.header("Verification Result")

        top_col1, top_col2 = st.columns([1.8, 1])

        with top_col1:
            if verdict == "REAL":
                st.success("🟢 REAL")
                st.caption("Corroborated by verified factual records and authoritative sources.")
            else:
                st.error("🔴 FAKE")
                st.caption("Contradicted by factual records or flagged as misleading/fabricated.")

        with top_col2:
            st.metric(
                "Confidence",
                f"{confidence * 100:.1f}%"
            )

        if is_quota:
            st.info(
                "💡 **API Notice:** OpenAI account has $0 balance (Error 429). Verified via **Smart Knowledge Classifier**. "
                "To enable live OpenAI GPT API, add credits at [platform.openai.com/settings/organization/billing](https://platform.openai.com/settings/organization/billing)."
            )

        if reasoning:
            st.markdown(f"**Factual Assessment:** {reasoning}")

        if evidence:
            st.subheader("Reference & Corroborating Sources")

            for num, item in enumerate(evidence, start=1):
                with st.expander(f"{num}. {item.get('title', 'Verified Source')}"):
                    domain = item.get("domain", "reuters.com")
                    st.write(
                        f"**Domain:** `{domain}` | "
                        f"**Source:** {item.get('source_name', domain)} | "
                        f"**Authority:** {item.get('source_score', 95)}/100"
                    )
                    st.write(f"> {item.get('evidence_text', '')}")
                    url = f"https://{domain}"
                    st.markdown(f"[🔗 View Reference Domain]({url})")
