import time
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from evidence.web_search import search_web
from evidence.source_ranker import rank_sources
from evidence.fact_checker import fact_check

def fast_collect_and_verify(claim: str):
    t0 = time.time()
    # 1 search query
    results = search_web(claim, max_results=6)
    t_search = time.time() - t0
    print(f"Search took: {t_search:.2f}s, got {len(results)} results")
    
    ranked = rank_sources(results)
    
    supporting = []
    contradicting = []
    
    for r in ranked:
        snippet = (r.get("title", "") + ". " + r.get("description", "")).strip()
        fc = fact_check(claim, snippet)
        rel = fc.get("relation", "neutral")
        conf = fc.get("confidence", 0.0)
        source_name = r.get("source_name", r.get("domain", "Unknown"))
        print(f"[{source_name}] ({rel}, conf={conf}): {snippet[:80]}...")
        if rel == "support":
            supporting.append((source_name, snippet, conf))
        elif rel == "contradict":
            contradicting.append((source_name, snippet, conf))
            
    print(f"\nTotal time: {time.time()-t0:.2f}s")
    print(f"Supporting: {len(supporting)}, Contradicting: {len(contradicting)}")

fast_collect_and_verify("virat kohli married with anushka sharma")

