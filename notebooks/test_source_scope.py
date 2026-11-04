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
    "Virat Kohli latest news"
)

scopes = [
    "Trusted news + official sources",
    "News sources only",
    "Official sources only"
]

for scope in scopes:

    print("\n" + "=" * 70)

    print(
        "SOURCE SCOPE:",
        scope
    )

    print("=" * 70)

    evidence = collect_evidence(
        claim,
        max_results_per_query=3,
        max_evidence=5,
        deep=False,
        source_scope=scope
    )

    print(
        "Evidence returned:",
        len(evidence)
    )

    for item in evidence:

        print(
            "\n",
            item["domain"],
            "|",
            item["source_type"]
        )
