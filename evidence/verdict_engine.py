def get_evidence_weight(item):

    source_score = float(
        item.get(
            "source_score",
            30
        )
    )

    relevance = float(
        item.get(
            "relevance_score",
            item.get(
                "relevance",
                0.0
            )
        )
    )

    source_weight = max(
        0.0,
        min(
            source_score / 100.0,
            1.0
        )
    )

    relevance_weight = max(
        0.0,
        min(
            relevance,
            1.0
        )
    )

    if relevance_weight < 0.08:
        return 0.0

    return (
        source_weight
        * relevance_weight
    )

def calculate_claim_verdict(
    analyzed_evidence
):

    if not analyzed_evidence:

        return {
            "verdict": "Unverified",
            "confidence": 0.0,
            "support_score": 0.0,
            "contradiction_score": 0.0,
            "supporting_sources": 0,
            "contradicting_sources": 0,
            "independent_sources": 0
        }

    support_score = 0.0
    contradiction_score = 0.0

    supporting_publishers = set()
    contradicting_publishers = set()
    all_publishers = set()

    for item in analyzed_evidence:

        publisher = str(
            item.get(
                "publisher_id",
                item.get(
                    "domain",
                    ""
                )
            )
        ).lower().strip()

        if publisher:

            all_publishers.add(
                publisher
            )

        weight = get_evidence_weight(
            item
        )

        if weight <= 0:
            continue

        fact_relation = item.get(
            "fact_relation",
            "neutral"
        )

        fact_confidence = float(
            item.get(
                "fact_confidence",
                0.0
            )
        )

        if fact_relation == "support":

            support_score += (
                weight
                * fact_confidence
            )

            if publisher:
                supporting_publishers.add(
                    publisher
                )

            continue

        if fact_relation == "contradict":

            contradiction_score += (
                weight
                * fact_confidence
            )

            if publisher:
                contradicting_publishers.add(
                    publisher
                )

            continue

        relationship = item.get(
            "relationship",
            "neutral"
        )

        entailment = float(
            item.get(
                "entailment_probability",
                0.0
            )
        )

        contradiction = float(
            item.get(
                "contradiction_probability",
                0.0
            )
        )

        directness = float(
            item.get(
                "directness",
                0.0
            )
        )

        if (
            relationship == "entailment"
            and entailment >= 0.65
        ):

            strength = (
                entailment
                * weight
                * max(
                    directness,
                    0.5
                )
            )

            support_score += strength

            if publisher:
                supporting_publishers.add(
                    publisher
                )

        elif (
            relationship == "contradiction"
            and contradiction >= 0.65
        ):

            strength = (
                contradiction
                * weight
                * max(
                    directness,
                    0.5
                )
            )

            contradiction_score += strength

            if publisher:
                contradicting_publishers.add(
                    publisher
                )

    supporting_sources = len(
        supporting_publishers
    )

    contradicting_sources = len(
        contradicting_publishers
    )

    independent_sources = len(
        all_publishers
    )

    strong_support = any(
        item.get("fact_relation")
        == "support"
        and float(
            item.get(
                "fact_confidence",
                0
            )
        ) >= 0.95
        for item in analyzed_evidence
    )

    strong_contradiction = any(
        item.get("fact_relation")
        == "contradict"
        and float(
            item.get(
                "fact_confidence",
                0
            )
        ) >= 0.95
        for item in analyzed_evidence
    )

    if strong_support and not strong_contradiction:

        total = (
            support_score
            + contradiction_score
        )

        confidence = (
            support_score / total
            if total > 0
            else 1.0
        )

        return {
            "verdict": "Supported",
            "confidence": round(
                max(
                    confidence,
                    0.80
                ),
                3
            ),
            "support_score": round(
                support_score,
                3
            ),
            "contradiction_score": round(
                contradiction_score,
                3
            ),
            "supporting_sources":
                supporting_sources,
            "contradicting_sources":
                contradicting_sources,
            "independent_sources":
                independent_sources
        }

    if strong_contradiction and not strong_support:

        total = (
            support_score
            + contradiction_score
        )

        confidence = (
            contradiction_score / total
            if total > 0
            else 1.0
        )

        return {
            "verdict": "Contradicted",
            "confidence": round(
                max(
                    confidence,
                    0.80
                ),
                3
            ),
            "support_score": round(
                support_score,
                3
            ),
            "contradiction_score": round(
                contradiction_score,
                3
            ),
            "supporting_sources":
                supporting_sources,
            "contradicting_sources":
                contradicting_sources,
            "independent_sources":
                independent_sources
        }

    if (
        support_score < 0.05
        and contradiction_score < 0.05
    ):

        return {
            "verdict": "Unverified",
            "confidence": 0.0,
            "support_score": round(
                support_score,
                3
            ),
            "contradiction_score": round(
                contradiction_score,
                3
            ),
            "supporting_sources":
                supporting_sources,
            "contradicting_sources":
                contradicting_sources,
            "independent_sources":
                independent_sources
        }

    if (
        supporting_sources > 0
        and contradicting_sources > 0
    ):

        total = (
            support_score
            + contradiction_score
        )

        if total > 0:

            difference = abs(
                support_score
                - contradiction_score
            )

            if (
                difference / total
                < 0.15
            ):

                return {
                    "verdict": "Unverified",
                    "confidence": 0.0,
                    "support_score": round(
                        support_score,
                        3
                    ),
                    "contradiction_score": round(
                        contradiction_score,
                        3
                    ),
                    "supporting_sources":
                        supporting_sources,
                    "contradicting_sources":
                        contradicting_sources,
                    "independent_sources":
                        independent_sources
                }

    if support_score > contradiction_score:

        total = (
            support_score
            + contradiction_score
        )

        confidence = (
            support_score / total
        )

        return {
            "verdict": "Supported",
            "confidence": round(
                confidence,
                3
            ),
            "support_score": round(
                support_score,
                3
            ),
            "contradiction_score": round(
                contradiction_score,
                3
            ),
            "supporting_sources":
                supporting_sources,
            "contradicting_sources":
                contradicting_sources,
            "independent_sources":
                independent_sources
        }

    if contradiction_score > support_score:

        total = (
            support_score
            + contradiction_score
        )

        confidence = (
            contradiction_score / total
        )

        return {
            "verdict": "Contradicted",
            "confidence": round(
                confidence,
                3
            ),
            "support_score": round(
                support_score,
                3
            ),
            "contradiction_score": round(
                contradiction_score,
                3
            ),
            "supporting_sources":
                supporting_sources,
            "contradicting_sources":
                contradicting_sources,
            "independent_sources":
                independent_sources
        }

    return {
        "verdict": "Unverified",
        "confidence": 0.0,
        "support_score": round(
            support_score,
            3
        ),
        "contradiction_score": round(
            contradiction_score,
            3
        ),
        "supporting_sources":
            supporting_sources,
        "contradicting_sources":
            contradicting_sources,
        "independent_sources":
            independent_sources
    }

def calculate_overall_verdict(
    claim_results,
    fallback_verdict="UNVERIFIED",
    fallback_confidence=0.0
):

    fallback_verdict = str(fallback_verdict or "UNVERIFIED").strip().upper()

    if fallback_verdict not in {"REAL", "FAKE", "UNCERTAIN", "UNVERIFIED"}:
        fallback_verdict = "UNVERIFIED"

    if not claim_results:

        return {
            "verdict": fallback_verdict,
            "confidence": round(float(fallback_confidence), 3),
            "supported_claims": 0,
            "contradicted_claims": 0,
            "unverified_claims": 0,
            "total_claims": 0,
            "decision_basis": "model"
        }

    supported = 0
    contradicted = 0
    unverified = 0
    support_score = 0.0
    contradiction_score = 0.0

    for result in claim_results:

        verdict = result.get(
            "verdict",
            "Unverified"
        )

        support_score += float(
            result.get(
                "support_score",
                0.0
            )
        )

        contradiction_score += float(
            result.get(
                "contradiction_score",
                0.0
            )
        )

        if verdict == "Supported":
            supported += 1
        elif verdict == "Contradicted":
            contradicted += 1
        else:
            unverified += 1

    if support_score > contradiction_score and support_score >= 0.15:
        final_verdict = "REAL"
        decision_basis = "evidence"
        total_ev = support_score + contradiction_score
        confidence = support_score / total_ev if total_ev > 0 else 0.85
    elif contradiction_score > support_score and contradiction_score >= 0.15:
        final_verdict = "FAKE"
        decision_basis = "evidence"
        total_ev = support_score + contradiction_score
        confidence = contradiction_score / total_ev if total_ev > 0 else 0.85
    elif supported > 0 and contradicted == 0:
        final_verdict = "REAL"
        decision_basis = "evidence"
        confidence = 0.80
    elif contradicted > 0 and supported == 0:
        final_verdict = "FAKE"
        decision_basis = "evidence"
        confidence = 0.80
    elif supported > 0 and contradicted > 0:
        if supported > contradicted:
            final_verdict = "REAL"
            decision_basis = "evidence_split"
            confidence = round(supported / (supported + contradicted), 3)
        elif contradicted > supported:
            final_verdict = "FAKE"
            decision_basis = "evidence_split"
            confidence = round(contradicted / (supported + contradicted), 3)
        else:
            final_verdict = "UNVERIFIED"
            decision_basis = "evidence_conflict"
            confidence = 0.0
    else:
        final_verdict = "UNVERIFIED"
        decision_basis = "insufficient_evidence"
        confidence = 0.0

    return {
        "verdict": final_verdict,
        "confidence": round(confidence, 3),
        "supported_claims": supported,
        "contradicted_claims": contradicted,
        "unverified_claims": unverified,
        "total_claims": len(claim_results),
        "decision_basis": decision_basis
    }
