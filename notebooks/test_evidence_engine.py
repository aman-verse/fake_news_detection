import sys
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from evidence.evidence_engine import (
    collect_evidence
)

claim = (
    "The Government of India announced "
    "a new education policy"
)

print("=" * 70)
print("VERIFI FULL EVIDENCE ENGINE TEST")
print("=" * 70)

print("\nClaim:")
print(claim)

print("\nSearching for evidence...")

evidence = collect_evidence(
    claim,
    max_results_per_query=5,
    max_evidence=10
)

print(
    "\nTotal evidence sources:",
    len(evidence)
)

for number, item in enumerate(
    evidence,
    start=1
):

    print(
        "\n" + "-" * 70
    )

    print(
        f"Evidence {number}"
    )

    print(
        "Title:",
        item["title"]
    )

    print(
        "Domain:",
        item["domain"]
    )

    print(
        "Type:",
        item["source_type"]
    )

    print(
        "Source score:",
        item["source_score"]
    )

    print(
        "Relevance:",
        item["relevance_score"]
    )

    print(
        "Final score:",
        item["final_score"]
    )

    print(
        "URL:",
        item["url"]
    )
