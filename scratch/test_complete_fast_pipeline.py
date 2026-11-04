import time
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from evidence.web_search import search_web
from evidence.source_ranker import rank_sources
from evidence.evidence_analyzer import analyze_evidence
from evidence.verdict_engine import calculate_claim_verdict, calculate_overall_verdict
from nlp.claim_extractor import extract_claims

def test_full_pipeline(claim_text):
    t_start = time.time()
    print(f"\n--- Testing: '{claim_text}' ---")
    
    t0 = time.time()
    claims = extract_claims(claim_text)
    if not claims:
        claims = [claim_text]
    print(f"1. Claim Extractor took {time.time()-t0:.2f}s: {claims}")
    
    # 2. Fast Evidence Collection (Snippets from 1-2 searches)
    t0 = time.time()
    all_results = search_web(claims[0], max_results=6)
    ranked = rank_sources(all_results)
    
    evidence = []
    for r in ranked:
        snippet = (r.get("title", "") + ". " + r.get("description", "")).strip()
        if len(snippet.split()) >= 6:
            evidence.append({
                "url": r.get("url", ""),
                "title": r.get("title", ""),
                "domain": r.get("domain", ""),
                "source_name": r.get("source_name", r.get("domain", "")),
                "source_score": r.get("source_score", 50),
                "source_tier": r.get("source_tier", "mainstream_news"),
                "publisher_id": r.get("publisher_id", r.get("domain", "")),
                "evidence_text": snippet,
                "relevance_score": 0.85,
                "relevance": 0.85
            })
    print(f"2. Search & snippet packaging took {time.time()-t0:.2f}s (found {len(evidence)} items)")
    
    # 3. Analyze top 4 evidence items
    t0 = time.time()
    analyzed = analyze_evidence(claims[0], evidence[:4])
    print(f"3. NLI Analysis took {time.time()-t0:.2f}s")
    
    # 4. Calculate verdict
    t0 = time.time()
    claim_verdict = calculate_claim_verdict(analyzed)
    overall = calculate_overall_verdict([claim_verdict])
    print(f"4. Verdict Engine took {time.time()-t0:.3f}s: Verdict={overall['verdict']} (Confidence={overall['confidence']*100:.1f}%)")
    print(f"TOTAL PIPELINE TIME: {time.time()-t_start:.2f}s")

test_full_pipeline("virat kohli married with anushka sharma")

