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
from models.predictor import predict_news_detailed
from nlp.claim_extractor import extract_claims

test_query = "virat kohli married with anushka sharma"
print(f"Testing claim: '{test_query}'")

t0 = time.time()
model_res = predict_news_detailed(test_query)
t_model = time.time() - t0
print(f"Model prediction: {model_res['prediction']} ({model_res['confidence']*100:.1f}%) in {t_model:.2f}s")

t0 = time.time()
claims = extract_claims(test_query)
if not claims:
    claims = [test_query]
t_claims = time.time() - t0
print(f"Claims extracted: {claims} in {t_claims:.2f}s")

t0 = time.time()
evidence = collect_evidence(claims[0], max_results_per_query=4, max_evidence=8, deep=False)
t_ev = time.time() - t0
print(f"Collected {len(evidence)} evidence items in {t_ev:.2f}s")

t0 = time.time()
analyzed = analyze_evidence(claims[0], evidence)
t_an = time.time() - t0
print(f"Analyzed evidence in {t_an:.2f}s")

claim_verdict = calculate_claim_verdict(analyzed)
print(f"Claim verdict: {claim_verdict}")
