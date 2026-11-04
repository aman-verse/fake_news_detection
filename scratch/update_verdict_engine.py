with open("evidence/verdict_engine.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace entailment threshold 0.85 with 0.65
content = content.replace("and entailment >= 0.85", "and entailment >= 0.65")
content = content.replace("and contradiction >= 0.85", "and contradiction >= 0.65")

# Replace support_score threshold 0.12 with 0.05
content = content.replace("support_score < 0.12\n        and contradiction_score < 0.12", "support_score < 0.05\n        and contradiction_score < 0.05")

# In calculate_overall_verdict fallback
old_fallback = '''    else:
        if fallback_verdict in {"REAL", "FAKE"}:
            final_verdict = fallback_verdict
            decision_basis = "model"
            confidence = round(float(fallback_confidence), 3)
        else:
            final_verdict = "UNVERIFIED"
            decision_basis = "no_evidence"
            confidence = 0.0'''

new_fallback = '''    else:
        final_verdict = "UNVERIFIED"
        decision_basis = "insufficient_evidence"
        confidence = 0.0'''

if old_fallback in content:
    content = content.replace(old_fallback, new_fallback)
    print("Replaced fallback logic")
else:
    print("old_fallback not exact match, checking normalized")

with open("evidence/verdict_engine.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated evidence/verdict_engine.py successfully")

