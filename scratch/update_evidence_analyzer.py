with open("evidence/evidence_analyzer.py", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "def analyze_evidence("
end_marker = "return analyzed"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx) + len(end_marker)

new_func = '''def analyze_evidence(claim, evidence):
    analyzed = []
    top_items = evidence[:4]

    for item in top_items:
        evidence_text = item.get("evidence_text", "").strip()
        if not evidence_text:
            continue

        structured = fact_check(claim, evidence_text)
        if structured.get("relation") == "support":
            relationship = "entailment"
            directness = 1.0
            nli = {
                "label": "entailment",
                "confidence": structured.get("confidence", 0.95),
                "entailment": 0.95,
                "contradiction": 0.0,
                "neutral": 0.05
            }
        elif structured.get("relation") == "contradict":
            relationship = "contradiction"
            directness = 1.0
            nli = {
                "label": "contradiction",
                "confidence": structured.get("confidence", 0.95),
                "entailment": 0.0,
                "contradiction": 0.95,
                "neutral": 0.05
            }
        else:
            nli = analyze_claim_against_evidence(claim, evidence_text)
            relationship = nli["label"]
            directness = 0.0

            if nli["label"] == "entailment" and nli["entailment"] >= 0.65:
                directness = 0.6
                relationship = "entailment"
            elif nli["label"] == "contradiction" and nli["contradiction"] >= 0.65:
                directness = 0.6
                relationship = "contradiction"
            else:
                relationship = "neutral"

        analyzed.append({
            **item,
            "relationship": relationship,
            "nli_confidence": nli["confidence"],
            "entailment_probability": nli["entailment"],
            "contradiction_probability": nli["contradiction"],
            "neutral_probability": nli["neutral"],
            "directness": directness,
            "structured": structured["relation"] != "neutral",
            "fact_relation": structured["relation"],
            "fact_confidence": structured["confidence"],
            "fact_reason": structured["reason"]
        })

    return analyzed'''

updated = content[:start_idx] + new_func + content[end_idx:]

with open("evidence/evidence_analyzer.py", "w", encoding="utf-8") as f:
    f.write(updated)

print("Updated evidence/evidence_analyzer.py successfully")

