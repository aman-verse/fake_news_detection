import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from evidence.query_builder import build_search_queries
from evidence.evidence_engine import collect_evidence
from evidence.evidence_analyzer import analyze_evidence
from evidence.verdict_engine import calculate_claim_verdict

claim = (
    "China is currently the world's most populous country, "
    "ahead of India."
)

print("=" * 70)
print("VERIFI FALSE CLAIM PIPELINE DIAGNOSTIC")
print("=" * 70)

print("\nCLAIM:")
print(claim)

queries = build_search_queries(
    claim,
    deep=False
)

print("\n" + "=" * 70)
print("GENERATED QUERIES")
print("=" * 70)

for i, query in enumerate(
    queries,
    1
):
    print(
        f"{i}. {query}"
    )

evidence = collect_evidence(
    claim,
    max_results_per_query=5,
    max_evidence=10,
    deep=False,
    source_scope="Trusted news + official sources"
)

print("\n" + "=" * 70)
print("RETURNED EVIDENCE")
print("=" * 70)

print(
    "Total:",
    len(evidence)
)

for i, item in enumerate(
    evidence,
    1
):

    print(
        f"\n--- Evidence {i} ---"
    )

    print(
        "Title:",
        item.get("title", "")
    )

    print(
        "Domain:",
        item.get("domain", "")
    )

    print(
        "Source type:",
        item.get("source_type", "")
    )

    print(
        "Source score:",
        item.get("source_score", 0)
    )

    print(
        "Relevance:",
        item.get("relevance_score", 0)
    )

    print(
        "Final score:",
        item.get("final_score", 0)
    )

    print(
        "Evidence text:"
    )

    print(
        item.get(
            "evidence_text",
            ""
        )[:1000]
    )

analyzed = analyze_evidence(
    claim,
    evidence
)

print("\n" + "=" * 70)
print("NLI RESULTS")
print("=" * 70)

for i, item in enumerate(
    analyzed,
    1
):

    print(
        f"\n--- Evidence {i} ---"
    )

    print(
        "Domain:",
        item.get("domain", "")
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

result = calculate_claim_verdict(
    analyzed
)

print("\n" + "=" * 70)
print("VERDICT")
print("=" * 70)

print(
    "Verdict:",
    result.get("verdict")
)

print(
    "Confidence:",
    result.get("confidence")
)

print(
    "Support:",
    result.get("support_score")
)

print(
    "Contradiction:",
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
