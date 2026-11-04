with open("views/verify.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update top columns
old_top_cols = '''        top_col1, top_col2, top_col3 = st.columns([1.5, 1, 1])

        with top_col1:
            if overall_verdict == "REAL":
                st.success("🟢 REAL")
                if decision_basis == "evidence":
                    st.caption("Corroborated by independent reputable sources.")
                else:
                    st.caption("Linguistic style consistent with authentic reporting (no counter-evidence found).")
            elif overall_verdict == "FAKE":
                st.error("🔴 FAKE")
                if decision_basis == "evidence":
                    st.caption("Contradicted by credible primary or authoritative sources.")
                else:
                    st.caption("Linguistic patterns strongly characteristic of fabricated news.")
            else:
                st.warning("⚪ UNVERIFIED / INCONCLUSIVE")
                st.caption("External source evidence is insufficient or inconclusive to confirm this claim.")

        with top_col2:
            st.metric(
                "Evidence Confidence",
                f"{overall_confidence * 100:.1f}%"
            )

        with top_col3:
            ml_pred = model_result.get("prediction", "N/A")
            ml_conf = model_result.get("confidence", 0.0)
            st.metric(
                "ML Stylistic Indicator",
                f"{ml_pred} ({ml_conf * 100:.1f}%)"
            )'''

new_top_cols = '''        top_col1, top_col2 = st.columns([1.8, 1])

        with top_col1:
            if overall_verdict == "REAL":
                st.success("🟢 REAL")
                st.caption("Corroborated by authoritative independent sources.")
            elif overall_verdict == "FAKE":
                st.error("🔴 FAKE")
                st.caption("Contradicted by credible primary or authoritative sources.")
            else:
                st.warning("⚪ UNVERIFIED / INCONCLUSIVE")
                st.caption("External source evidence is insufficient or inconclusive to confirm this claim.")

        with top_col2:
            st.metric(
                "Confidence",
                f"{overall_confidence * 100:.1f}%"
            )'''

if old_top_cols in content:
    content = content.replace(old_top_cols, new_top_cols)
    print("Replaced top_cols")
else:
    print("old_top_cols not exact match")

# 2. Update claim metrics columns (m1, m2, m3, m4 -> m1, m2, m3)
old_claim_metrics = '''                m1, m2, m3, m4 = st.columns(4)

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

                with m4:
                    claim_ml = result.get("model_prediction", "N/A")
                    claim_conf = result.get("model_confidence", 0.0)
                    st.metric(
                        "Stylistic Model",
                        f"{claim_ml} ({claim_conf * 100:.0f}%)"
                    )'''

new_claim_metrics = '''                m1, m2, m3 = st.columns(3)

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
                    )'''

if old_claim_metrics in content:
    content = content.replace(old_claim_metrics, new_claim_metrics)
    print("Replaced claim_metrics")
else:
    print("old_claim_metrics not exact match")

with open("views/verify.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated views/verify.py successfully")

