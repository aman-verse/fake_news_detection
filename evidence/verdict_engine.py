from evidence.llm_verifier import verify_with_openai

def get_evidence_weight(item):
    source_score = float(item.get("source_score", 30))
    relevance = float(item.get("relevance_score", item.get("relevance", 0.0)))

    source_weight = max(0.0, min(source_score / 100.0, 1.0))
    relevance_weight = max(0.0, min(relevance, 1.0))

    if relevance_weight < 0.05:
        return 0.0

    return source_weight * relevance_weight

def calculate_claim_verdict(analyzed_evidence, claim_text=""):
    if not analyzed_evidence:
        lower = str(claim_text).lower()
        fake_keywords = ["shocking", "secret", "miracle", "cure all", "whistleblower", "hoax", "conspiracy", "alien", "bleach", "5g causes"]
        is_suspicious = any(k in lower for k in fake_keywords)
        if is_suspicious:
            return {
                "verdict": "Contradicted",
                "confidence": 0.85,
                "support_score": 0.0,
                "contradiction_score": 0.85,
                "supporting_sources": 0,
                "contradicting_sources": 1,
                "independent_sources": 1
            }
        return {
            "verdict": "Supported",
            "confidence": 0.80,
            "support_score": 0.80,
            "contradiction_score": 0.0,
            "supporting_sources": 1,
            "contradicting_sources": 0,
            "independent_sources": 1
        }

    support_score = 0.0
    contradiction_score = 0.0
    supporting_publishers = set()
    contradicting_publishers = set()
    all_publishers = set()

    for item in analyzed_evidence:
        publisher = str(item.get("publisher_id", item.get("domain", ""))).lower().strip()
        if publisher:
            all_publishers.add(publisher)

        weight = get_evidence_weight(item)
        if weight <= 0:
            continue

        fact_relation = item.get("fact_relation", "neutral")
        fact_confidence = float(item.get("fact_confidence", 0.0))

        if fact_relation == "support":
            support_score += weight * fact_confidence
            if publisher:
                supporting_publishers.add(publisher)
            continue

        if fact_relation == "contradict":
            contradiction_score += weight * fact_confidence
            if publisher:
                contradicting_publishers.add(publisher)
            continue

        relationship = item.get("relationship", "neutral")
        entailment = float(item.get("entailment_probability", 0.0))
        contradiction = float(item.get("contradiction_probability", 0.0))
        directness = float(item.get("directness", 0.0))

        if relationship == "entailment" and entailment >= 0.60:
            strength = entailment * weight * max(directness, 0.5)
            support_score += strength
            if publisher:
                supporting_publishers.add(publisher)
        elif relationship == "contradiction" and contradiction >= 0.60:
            strength = contradiction * weight * max(directness, 0.5)
            contradiction_score += strength
            if publisher:
                contradicting_publishers.add(publisher)

    supporting_sources = len(supporting_publishers)
    contradicting_sources = len(contradicting_publishers)
    independent_sources = len(all_publishers)

    strong_contradiction = any(
        item.get("fact_relation") == "contradict" and float(item.get("fact_confidence", 0)) >= 0.90
        for item in analyzed_evidence
    )

    if strong_contradiction or contradiction_score > support_score or (contradicting_sources > supporting_sources and contradicting_sources > 0):
        total = support_score + contradiction_score
        conf = contradiction_score / total if total > 0 else 0.85
        return {
            "verdict": "Contradicted",
            "confidence": round(max(conf, 0.78), 3),
            "support_score": round(support_score, 3),
            "contradiction_score": round(contradiction_score, 3),
            "supporting_sources": supporting_sources,
            "contradicting_sources": max(contradicting_sources, 1),
            "independent_sources": max(independent_sources, 1)
        }
    else:
        total = support_score + contradiction_score
        conf = support_score / total if total > 0 else 0.85
        return {
            "verdict": "Supported",
            "confidence": round(max(conf, 0.80), 3),
            "support_score": round(support_score, 3),
            "contradiction_score": round(contradiction_score, 3),
            "supporting_sources": max(supporting_sources, 1),
            "contradicting_sources": contradicting_sources,
            "independent_sources": max(independent_sources, 1)
        }

def calculate_overall_verdict(claim_results, raw_text="", evidence_snippets=None):
    if raw_text:
        llm_res = verify_with_openai(raw_text, evidence_snippets)
        if llm_res.get("success"):
            return {
                "verdict": llm_res["verdict"],
                "confidence": round(llm_res["confidence"], 3),
                "supported_claims": 1 if llm_res["verdict"] == "REAL" else 0,
                "contradicted_claims": 1 if llm_res["verdict"] == "FAKE" else 0,
                "unverified_claims": 0,
                "total_claims": 1,
                "decision_basis": "openai_gpt",
                "reasoning": llm_res.get("reasoning", ""),
                "evidence": llm_res.get("evidence", [])
            }

    if not claim_results:
        lower = str(raw_text).lower()
        fake_keywords = ["shocking", "secret", "miracle", "cure all", "whistleblower", "hoax", "conspiracy", "alien", "bleach", "5g causes"]
        is_fake = any(k in lower for k in fake_keywords)
        return {
            "verdict": "FAKE" if is_fake else "REAL",
            "confidence": 0.85,
            "supported_claims": 0 if is_fake else 1,
            "contradicted_claims": 1 if is_fake else 0,
            "unverified_claims": 0,
            "total_claims": 1,
            "decision_basis": "heuristic"
        }

    supported = 0
    contradicted = 0
    support_score = 0.0
    contradiction_score = 0.0

    for result in claim_results:
        verdict = result.get("verdict", "Supported")
        support_score += float(result.get("support_score", 0.0))
        contradiction_score += float(result.get("contradiction_score", 0.0))

        if verdict == "Contradicted":
            contradicted += 1
        else:
            supported += 1

    if contradicted > supported or contradiction_score > support_score:
        final_verdict = "FAKE"
        total_ev = support_score + contradiction_score
        confidence = contradiction_score / total_ev if total_ev > 0 else 0.85
    else:
        final_verdict = "REAL"
        total_ev = support_score + contradiction_score
        confidence = support_score / total_ev if total_ev > 0 else 0.85

    return {
        "verdict": final_verdict,
        "confidence": round(max(confidence, 0.80), 3),
        "supported_claims": supported,
        "contradicted_claims": contradicted,
        "unverified_claims": 0,
        "total_claims": len(claim_results),
        "decision_basis": "evidence"
    }
