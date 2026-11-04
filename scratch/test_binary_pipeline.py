import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from evidence.evidence_engine import collect_evidence
from evidence.evidence_analyzer import analyze_evidence
from evidence.verdict_engine import calculate_claim_verdict, calculate_overall_verdict
from nlp.claim_extractor import extract_claims

test_cases = [
    "virat kohli married with anushka sharma",
    "drinking common household bleach cures all viral infections",
    "earth revolves around the sun",
    "shocking secret underground alien lab reveals aliens control government"
]

for test in test_cases:
    claims = extract_claims(test)
    if not claims:
        claims = [test]
    claim_results = []
    for claim in claims:
        evidence = collect_evidence(claim, max_results_per_query=4, max_evidence=5, deep=False)
        analyzed = analyze_evidence(claim, evidence)
        cv = calculate_claim_verdict(analyzed, claim_text=claim)
        claim_results.append(cv)
    all_snippets = [
        item.get("evidence_text", "")
        for cres in claim_results
        for item in cres.get("evidence", [])
        if item.get("evidence_text")
    ]
    overall = calculate_overall_verdict(claim_results, raw_text=test, evidence_snippets=all_snippets)
    print(f"Claim: '{test[:45]}...' -> Final Verdict: {overall['verdict']} ({overall['confidence']*100:.1f}%) [Basis: {overall['decision_basis']}]")

