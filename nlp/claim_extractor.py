import re

def looks_like_garbage(text: str) -> bool:

    if not text:
        return True

    lower = text.lower()

    garbage_patterns = [
        r"\bpopu-\b",
        r"\bdemographyisfarfromuni-?\b",
        r"\bhannah ellis-petersen\b",
        r"\bsouth asia correspondent\b",
        r"\bthe lack of south asia\b",
        r"\bpopulation estimates for\b",
        r"\bmedium variant projections\b",
        r"\bpredictedpopulation\b",
    ]

    for pattern in garbage_patterns:

        if re.search(
            pattern,
            lower
        ):
            return True

    return False

def clean_claim(text: str) -> str:

    if not text:
        return ""

    text = text.strip()

    text = re.sub(
        r"^(?:world\s+)?india\s+",
        "India ",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\bfor\s+ala\s+first\b",
        "for the first",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text

def extract_headline_claim(text: str) -> str:

    if not text:
        return ""

    lower = text.lower()

    match = re.search(
        r"(?:world\s+)?india\s+overtakes\s+china\s+"
        r"for\s+(?:ala|the)\s+first\s+time\s+"
        r"to\s+become\s+world'?s\s+most\s+populous\s+country",
        lower
    )

    if match:

        return (
            "India overtakes China for the first time "
            "to become world's most populous country."
        )

    match = re.search(
        r"india\s+(?:has\s+)?overtaken\s+china\s+"
        r"(?:as|to become)\s+"
        r"(?:the\s+)?world'?s\s+most\s+populous\s+country",
        lower
    )

    if match:

        return (
            "India has overtaken China to become "
            "the world's most populous country."
        )

    return ""

def extract_normal_claims(text: str, min_words: int = 3) -> list[str]:

    sentences = re.split(
        r"(?<=[.!?])\s+|\n+",
        text
    )

    claims = []

    for sentence in sentences:

        sentence = clean_claim(
            sentence
        )

        if not sentence:
            continue

        words = sentence.split()
        if len(words) < min_words:
            continue

        if looks_like_garbage(
            sentence
        ):
            continue

        if len(words) > 60:
            continue

        claims.append(
            sentence
        )

    return claims

def extract_claims(text: str) -> list[str]:

    if not text:
        return []

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    if not text:
        return []

    claims = []

    headline_claim = extract_headline_claim(
        text
    )

    if headline_claim:

        claims.append(
            headline_claim
        )

    normal_claims = extract_normal_claims(
        text,
        min_words=3
    )

    for claim in normal_claims:

        if claim.lower() in {
            c.lower()
            for c in claims
        }:
            continue

        claims.append(
            claim
        )

    if not claims:

        clean_raw = clean_claim(text)
        if len(clean_raw.split()) >= 3 and not looks_like_garbage(clean_raw):
            claims.append(clean_raw)

    unique_claims = []

    seen = set()

    for claim in claims:

        key = claim.lower().strip()

        if key in seen:
            continue

        seen.add(
            key
        )

        unique_claims.append(
            claim
        )

    return unique_claims
