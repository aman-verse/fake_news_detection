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
    "Virat Kohli was found dead in a river"
)

print("=" * 70)
print("VERIFI DEEP INVESTIGATION TEST")
print("=" * 70)

print("\nClaim:")
print(claim)

print("\nRunning deep investigation...")

evidence = collect_evidence(
    claim,
    max_results_per_query=10,
    max_evidence=20,
    deep=True
)

print(
    "\nTotal evidence:",
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
