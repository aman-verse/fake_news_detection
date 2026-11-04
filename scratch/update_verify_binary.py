with open("views/verify.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add cache at the top
if "_VERIFY_CACHE = {}" not in content:
    content = "_VERIFY_CACHE = {}\n\n" + content

# Update binary verdict mapping in claim loop
old_claim_mapping = '''                    if claim_verdict["verdict"] == "Supported":
                        claim_binary = "REAL"
                    elif claim_verdict["verdict"] == "Contradicted":
                        claim_binary = "FAKE"
                    else:
                        claim_binary = "UNVERIFIED"'''

new_claim_mapping = '''                    if claim_verdict.get("verdict") == "Contradicted":
                        claim_binary = "FAKE"
                    else:
                        claim_binary = "REAL"'''

content = content.replace(old_claim_mapping, new_claim_mapping)

# Update overall verdict call
old_overall_call = '''                overall = calculate_overall_verdict(
                    claim_results,
                    fallback_verdict=model_result.get("prediction", "UNVERIFIED"),
                    fallback_confidence=model_result.get("confidence", 0.0)
                )'''

new_overall_call = '''                all_snippets = [
                    item.get("evidence_text", "")
                    for cres in claim_results
                    for item in cres.get("evidence", [])
                    if item.get("evidence_text")
                ]
                overall = calculate_overall_verdict(
                    claim_results,
                    raw_text=verification_text,
                    evidence_snippets=all_snippets
                )'''

content = content.replace(old_overall_call, new_overall_call)

# Update UI top block to be strictly binary REAL or FAKE
old_top_ui = '''        with top_col1:
            if overall_verdict == "REAL":
                st.success("🟢 REAL")
                st.caption("Corroborated by authoritative independent sources.")
            elif overall_verdict == "FAKE":
                st.error("🔴 FAKE")
                st.caption("Contradicted by credible primary or authoritative sources.")
            else:
                st.warning("⚪ UNVERIFIED / INCONCLUSIVE")
                st.caption("External source evidence is insufficient or inconclusive to confirm this claim.")'''

new_top_ui = '''        with top_col1:
            if overall_verdict == "REAL":
                st.success("🟢 REAL")
                st.caption("Corroborated by independent authoritative sources.")
            else:
                st.error("🔴 FAKE")
                st.caption("Contradicted by verified sources or flagged as fabricated.")'''

content = content.replace(old_top_ui, new_top_ui)

# Update Claim card display to be strictly binary
old_claim_card_ui = '''                if verdict == "REAL":
                    st.success(
                        f"🟢 REAL (Supported by sources — {confidence * 100:.1f}%)"
                    )
                elif verdict == "FAKE":
                    st.error(
                        f"🔴 FAKE (Contradicted by sources — {confidence * 100:.1f}%)"
                    )
                else:
                    st.warning(
                        "⚪ UNVERIFIED (No definitive corroboration found in queried sources)"
                    )'''

new_claim_card_ui = '''                if verdict == "FAKE":
                    st.error(
                        f"🔴 FAKE (Flagged as misleading or contradictory — {confidence * 100:.1f}%)"
                    )
                else:
                    st.success(
                        f"🟢 REAL (Supported by authoritative reports — {confidence * 100:.1f}%)"
                    )'''

content = content.replace(old_claim_card_ui, new_claim_card_ui)

with open("views/verify.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated views/verify.py for strict binary REAL/FAKE")

