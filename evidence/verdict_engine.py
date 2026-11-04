# =========================================================
# VERIFI VERDICT ENGINE
# =========================================================


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


# =========================================================
# CLAIM VERDICT
# =========================================================

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

    # =====================================================
    # PROCESS EVIDENCE
    # =====================================================

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

        # =================================================
        # STRUCTURED FACT CHECK
        # =================================================

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

        # =================================================
        # NLI FALLBACK
        # =================================================

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

        # Generic NLI needs strong probability
        # and is deliberately weaker than structured facts.

        if (
            relationship == "entailment"
            and entailment >= 0.85
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
            and contradiction >= 0.85
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

    # =====================================================
    # COUNTS
    # =====================================================

    supporting_sources = len(
        supporting_publishers
    )

    contradicting_sources = len(
        contradicting_publishers
    )

    independent_sources = len(
        all_publishers
    )

    # =====================================================
    # STRONG STRUCTURED EVIDENCE
    # =====================================================

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

    # =====================================================
    # STRONG FACT HAS PRIORITY
    # =====================================================

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

    # =====================================================
    # NO STRONG EVIDENCE
    # =====================================================

    if (
        support_score < 0.12
        and contradiction_score < 0.12
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

    # =====================================================
    # CONFLICT
    # =====================================================

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

            # Only call it unresolved when
            # evidence is genuinely close.

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

    # =====================================================
    # FINAL COMPARISON
    # =====================================================

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


# =========================================================
# OVERALL VERDICT
# =========================================================

def calculate_overall_verdict(
    claim_results,
    fallback_verdict
):

    fallback_verdict = str(
        fallback_verdict
    ).strip().upper()

    if fallback_verdict not in {
        "REAL",
        "FAKE"
    }:

        raise ValueError(
            "fallback_verdict must be Real or Fake"
        )

    if not claim_results:

        return {
            "verdict": fallback_verdict,
            "confidence": 0.0,
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

        confidence = float(
            result.get(
                "confidence",
                0.0
            )
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

    if support_score > contradiction_score:
        final_verdict = "REAL"
        decision_basis = "evidence"
    elif contradiction_score > support_score:
        final_verdict = "FAKE"
        decision_basis = "evidence"
    elif supported > contradicted:
        final_verdict = "REAL"
        decision_basis = "evidence"
    elif contradicted > supported:
        final_verdict = "FAKE"
        decision_basis = "evidence"
    else:
        final_verdict = fallback_verdict
        decision_basis = "model"

    evidence_total = (
        support_score
        + contradiction_score
    )

    if evidence_total > 0:
        confidence = max(
            support_score,
            contradiction_score
        ) / evidence_total
    else:
        confidence_values = [
            float(result.get("confidence", 0.0))
            for result in claim_results
            if result.get("verdict") in {
                "Supported",
                "Contradicted"
            }
        ]
        confidence = (
            sum(confidence_values) / len(confidence_values)
            if confidence_values
            else 0.0
        )

    return {
        "verdict": final_verdict,
        "confidence": round(
            confidence,
            3
        ),
        "supported_claims":
            supported,
        "contradicted_claims":
            contradicted,
        "unverified_claims":
            unverified,
        "total_claims":
            len(claim_results),
        "decision_basis":
            decision_basis
    }