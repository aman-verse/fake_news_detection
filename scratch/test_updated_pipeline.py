import time
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

from evidence.evidence_engine import collect_evidence
from evidence.evidence_analyzer import analyze_evidence
from evidence.verdict_engine import calculate_claim_verdict, calculate_overall_verdict
from nlp.claim_extractor import extract_claims

test_cases = [
    "virat kohli married with anushka sharma",
    "drinking common household bleach cures all viral infections",
    "earth revolves around the sun"
]

for test in test_cases:
    t0 = time.time()
    claims = extract_claims(test)
    if not claims:
        claims = [test]
        
    claim_results = []
    for claim in claims:
        evidence = collect_evidence(claim, max_results_per_query=4, max_evidence=5, deep=False)
        analyzed = analyze_evidence(claim, evidence)
        cv = calculate_claim_verdict(analyzed)
        claim_results.append(cv)
        
    overall = calculate_overall_verdict(claim_results)
    elapsed = time.time() - t0
    print(f"[{elapsed:.2f}s] Query: '{test}' -> Verdict: {overall['verdict']} (Confidence: {overall['confidence']*100:.1f}%)")

