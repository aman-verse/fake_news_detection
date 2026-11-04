import streamlit as st
import json

from utils.history_db import (
    get_history,
    delete_history_item
)


def show():

    st.title("📚 Verification History")

    st.write(
        "Review your previous news verification results."
    )

    st.divider()

    history = get_history()

    if not history:

        st.info(
            "No verification history yet."
        )

        st.write(
            "Verify your first article to see "
            "the result here."
        )

        return

    st.caption(
        f"{len(history)} verification(s) recorded"
    )

    st.divider()

    # =====================================================
    # HISTORY LIST
    # =====================================================

    for item in history:

        (
            verification_id,
            created_at,
            input_text,
            verdict,
            confidence,
            supported,
            contradicted,
            unverified,
            total_claims,
            claims_data
        ) = item

        # -------------------------------------------------
        # VERDICT DISPLAY
        # -------------------------------------------------

        if verdict == "REAL":

            verdict_text = "🟢 REAL"
            binary_verdict = "REAL"

        elif verdict == "FAKE":

            verdict_text = "🔴 FAKE"
            binary_verdict = "FAKE"

        else:
            from models.predictor import predict_news

            binary_verdict = predict_news(
                input_text
            ).upper()
            verdict_text = (
                "🟢 REAL"
                if binary_verdict == "REAL"
                else "🔴 FAKE"
            )

        # -------------------------------------------------
        # HISTORY CARD
        # -------------------------------------------------

        with st.container(
            border=True
        ):

            top_col1, top_col2 = st.columns(
                [4, 1]
            )

            with top_col1:

                st.subheader(
                    verdict_text
                )

                st.caption(
                    created_at
                )

            with top_col2:

                st.metric(
                    "Confidence",
                    f"{confidence * 100:.1f}%"
                )

            # -------------------------------------------------
            # INPUT PREVIEW
            # -------------------------------------------------

            preview = input_text.replace(
                "\n",
                " "
            )

            if len(preview) > 250:

                preview = (
                    preview[:250]
                    + "..."
                )

            st.write(
                preview
            )

            # -------------------------------------------------
            # CLAIM SUMMARY
            # -------------------------------------------------

            claim_col1, claim_col2, claim_col3 = st.columns(3)

            with claim_col1:

                st.metric(
                    "Supported",
                    supported
                )

            with claim_col2:

                st.metric(
                    "Contradicted",
                    contradicted
                )

            with claim_col3:

                st.metric(
                    "Evidence gaps",
                    unverified
                )

            # -------------------------------------------------
            # DETAILS
            # -------------------------------------------------

            with st.expander(
                "View verification details"
            ):

                st.write(
                    "**Full submitted content**"
                )

                st.write(
                    input_text
                )

                st.write(
                    "**Claims**"
                )

                try:

                    claims = json.loads(
                        claims_data
                    )

                except Exception:

                    claims = []

                for number, claim in enumerate(
                    claims,
                    start=1
                ):

                    st.markdown(
                        f"**Claim {number}**"
                    )

                    st.write(
                        claim.get(
                            "claim",
                            ""
                        )
                    )

                    claim_verdict = claim.get(
                        "binary_verdict"
                    )

                    if claim_verdict not in {
                        "REAL",
                        "FAKE"
                    }:
                        legacy_verdict = claim.get(
                            "verdict",
                            ""
                        )
                        claim_verdict = {
                            "Supported": "REAL",
                            "Contradicted": "FAKE"
                        }.get(
                            legacy_verdict,
                            binary_verdict
                        )

                    claim_confidence = claim.get(
                        "confidence",
                        0.0
                    )

                    st.write(
                        f"Result: **{claim_verdict}**"
                    )

                    st.write(
                        "Confidence: "
                        f"{claim_confidence * 100:.1f}%"
                    )

            # -------------------------------------------------
            # DELETE
            # -------------------------------------------------

            if st.button(
                "Delete",
                key=f"delete_{verification_id}"
            ):

                delete_history_item(
                    verification_id
                )

                st.rerun()