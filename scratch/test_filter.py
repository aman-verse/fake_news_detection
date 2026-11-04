import time
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from evidence.web_search import search_web
from evidence.source_ranker import rank_sources
from evidence.evidence_engine import filter_sources

results = search_web("virat kohli married with anushka sharma", max_results=6)
ranked = rank_sources(results)
print("Ranked before filter:")
for r in ranked:
    print(r.get("domain"), "->", r.get("source_type"), r.get("source_score"))

filtered = filter_sources(ranked, "Trusted news + official sources")
print("\nAfter filter:", len(filtered), "sources")

