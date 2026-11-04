import time
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from evidence.evidence_analyzer import analyze_claim_against_evidence

claim = "virat kohli married with anushka sharma"
snippets = [
    "Virat Kohli and Anushka Sharma married in December 2017 in a private ceremony in Florence, Italy.",
    "Indian cricket captain Virat Kohli married Bollywood actress Anushka Sharma.",
    "Virat Kohli and Anushka Sharma complete love story and marriage timeline."
]

for s in snippets:
    res = analyze_claim_against_evidence(claim, s)
    print("Snippet:", s)
    print("NLI:", res["label"], f"(entailment={res['entailment']:.3f}, contradiction={res['contradiction']:.3f}, neutral={res['neutral']:.3f})")

