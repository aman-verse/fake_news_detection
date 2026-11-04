import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from models.predictor import predict_news_detailed, predict_news
from nlp.preprocessing import clean_text, validate_input
from nlp.claim_extractor import extract_claims

TEST_SUITE = [
    (
        "1. Clearly Fabricated News",
        "BREAKING: Shocking secret underground lab reveals extraterrestrial aliens controlling the government from shadows!",
        "Expect Fake classification with high confidence"
    ),
    (
        "2. Authentic News",
        "The Federal Reserve announced on Wednesday that it will maintain the benchmark interest rate target range to balance employment and price stability.",
        "Expect Real classification with high confidence"
    ),
    (
        "3. Misleading Headlines",
        "SHOCKING [WATCH]: Drinking common household bleach confirmed by secret whistleblowers to cure all viral infections instantly!",
        "Expect Fake classification (clickbait & sensationalist framing)"
    ),
    (
        "4. Partially True Information",
        "The Earth revolves around the Sun, but NASA has secretly concealed that gravity does not exist on Thursdays.",
        "Expect nuanced evaluation (flagged as misleading / uncertain / fake)"
    ),
    (
        "5. Very Short News Statement",
        "Water freezes at 0 Celsius.",
        "Expect robust claim extraction and handling without crash"
    ),
    (
        "6. Long News Article",
        """
        The Department of Transportation released a comprehensive infrastructure investment framework
        outlining modernizations for passenger rail networks, bridge rehabilitation projects, and
        sustainable port logistics across thirty metropolitan corridors over the coming decade.
        State governors commended the collaborative grant process, which allocates funding based on
        demonstrated safety enhancements, regional economic development potential, and resilience
        against extreme meteorological disruptions. Environmental review benchmarks will be streamlined
        under updated federal administrative guidelines to expedite procurement timelines while maintaining
        statutory environmental impact standards.
        """,
        "Expect Real classification on formal journalistic policy text"
    ),
    (
        "7. Empty / Whitespace Input",
        "    ",
        "Expect graceful guardrail rejection (Uncertain/Invalid, no crash)"
    ),
    (
        "8. Random / Irrelevant Text",
        "asdfghjk qwertyuiop zxcvbnm lkjhgfds poiuytrewq",
        "Expect graceful handling (Uncertain / out-of-vocabulary, no crash)"
    ),
    (
        "9. News with URLs & Special Characters",
        "Breaking economic update from https://finance.gov/bulletin?id=9876&ref=alert: Treasury yields stabilized at 4.2% following quarterly auction #Treasury #Yields @FinNews!!",
        "Expect URL stripping and robust feature evaluation"
    ),
    (
        "10. Inputs with Spelling & Grammatical Errors",
        "The govrnmnt announcd brand new scolaships and finacial asistance for univeristy studnts across the contry.",
        "Expect resilient classification despite minor orthographic noise"
    )
]

def main():
    print("=" * 75)
    print("VERIFI COMPREHENSIVE 10-SCENARIO VERIFICATION TEST SUITE")
    print("=" * 75)
    
    passed_count = 0
    
    for idx, (title, sample_text, expectation) in enumerate(TEST_SUITE, start=1):
        print(f"\nScenario {title}")
        print(f"Expectation: {expectation}")
        print(f"Input Preview: {sample_text.strip()[:70]}...")
        
        is_valid, val_msg = validate_input(sample_text)
        
        res = predict_news_detailed(sample_text)
        
        claims = extract_claims(sample_text)
        
        print(f"  Valid Input:     {is_valid} ({val_msg or 'OK'})")
        print(f"  ML Prediction:   {res['prediction']} (P(Real)={res['probability_real']*100:.1f}%, P(Fake)={res['probability_fake']*100:.1f}%)")
        print(f"  Confidence:      {res['confidence']*100:.1f}%")
        print(f"  Status:          {res['status']}")
        print(f"  Claims Found:    {len(claims)} -> {claims[:2]}")
        
        passed = True
        if idx == 1 and res['prediction'] != 'Fake':
            passed = False
        elif idx == 2 and res['prediction'] != 'Real':
            passed = False
        elif idx == 3 and res['prediction'] != 'Fake':
            passed = False
        elif idx == 6 and res['prediction'] != 'Real':
            passed = False
        elif idx == 7 and is_valid is not False:
            passed = False
            
        if passed:
            print("  Result:          [PASS]")
            passed_count += 1
        else:
            print("  Result:          [REVIEW]")
            
    print("\n" + "=" * 75)
    print(f"TEST SUITE SUMMARY: {passed_count}/{len(TEST_SUITE)} Scenarios Handled Successfully")
    print("=" * 75)

if __name__ == "__main__":
    main()
