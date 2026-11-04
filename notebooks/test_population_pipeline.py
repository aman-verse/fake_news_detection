import sys
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from evidence.evidence_engine import collect_evidence
from evidence.evidence_analyzer import analyze_evidence
from evidence.verdict_engine import calculate_claim_verdict

claim = (
    "India has overtaken China to become "
    "the world's most populous country."
)

print("=" * 70)
print("VERIFI POPULATION CLAIM DIAGNOSTIC")
print("=" * 70)

print("\nCLAIM:")
print(claim)

print("\n" + "=" * 70)
print("STEP 1: COLLECTING EVIDENCE")
print("=" * 70)

evidence = collect_evidence(
    claim,
    max_results_per_query=5,
    max_evidence=10,
    deep=False,
    source_scope="Trusted news + official sources"
)

print(
    "\nEvidence returned:",
    len(evidence)
)

for i, item in enumerate(
    evidence,
    start=1
):

    print(
        f"\n--- Evidence {i} ---"
    )

    print(
        "Title:",
        item.get(
            "title",
            ""
        )
    )

    print(
        "Domain:",
        item.get(
            "domain",
            ""
        )
    )

    print(
        "Source type:",
        item.get(
            "source_type",
            ""
        )
    )

    print(
        "Source score:",
        item.get(
            "source_score",
            0
        )
    )

    print(
        "Relevance:",
        item.get(
            "relevance_score",
            0
        )
    )

print("\n" + "=" * 70)
print("STEP 2: NLI ANALYSIS")
print("=" * 70)

analyzed = analyze_evidence(
    claim,
    evidence
)

for i, item in enumerate(
    analyzed,
    start=1
):

    print(
        f"\n--- Evidence {i} ---"
    )

    print(
        "Domain:",
        item.get(
            "domain",
            ""
        )
    )

    print(
        "Relationship:",
        item.get(
            "relationship",
            ""
        )
    )

    print(
        "NLI confidence:",
        item.get(
            "nli_confidence",
            0
        )
    )

    print(
        "Relevance:",
        item.get(
            "relevance_score",
            0
        )
    )

    print(
        "Source score:",
        item.get(
            "source_score",
            0
        )
    )

print("\n" + "=" * 70)
print("STEP 3: CLAIM VERDICT")
print("=" * 70)

result = calculate_claim_verdict(
    analyzed
)

print(
    "\nVerdict:",
    result.get(
        "verdict"
    )
)

print(
    "Confidence:",
    result.get(
        "confidence"
    )
)

print(
    "Support score:",
    result.get(
        "support_score"
    )
)

print(
    "Contradiction score:",
    result.get(
        "contradiction_score"
    )
)

print(
    "Supporting sources:",
    result.get(
        "supporting_sources"
    )
)

print(
    "Contradicting sources:",
    result.get(
        "contradicting_sources"
    )
)

print(
    "Independent sources:",
    result.get(
        "independent_sources"
    )
)

print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70)
