import re

def clean_claim(claim):

    return re.sub(
        r"\s+",
        " ",
        claim.strip()
    )

def build_search_queries(
    claim,
    deep=False
):

    if not claim:
        return []

    claim = clean_claim(claim)

    lower = claim.lower()

    queries = [
        claim,
        f'"{claim}"'
    ]

    if any(
        word in lower
        for word in [
            "water",
            "temperature",
            "freezes",
            "freezing",
            "earth",
            "sun",
            "moon",
            "gravity",
            "planet",
            "ocean",
            "mount everest"
        ]
    ):

        queries.extend([
            claim + " scientific source",
            claim + " official source",
            claim + " NASA",
            claim + " NOAA"
        ])

    if (
        "water" in lower
        and any(
            word in lower
            for word in [
                "freeze",
                "freezes",
                "freezing"
            ]
        )
    ):

        queries.extend([
            "freezing point of pure water Celsius NIST",
            "water freezing point standard pressure NIST",
            "water freezes 0 Celsius NIST",
            "water freezing point 32 Fahrenheit",
            "water freezing point standard atmospheric pressure",
            "site:nist.gov water freezing point",
            "site:usgs.gov water freezing point"
        ])

    if (
        "earth" in lower
        and "sun" in lower
    ):

        queries.extend([
            "Earth revolves around Sun NASA",
            "Earth orbits the Sun NASA",
            "Earth revolution around Sun scientific source",
            "Earth orbit Sun official"
        ])

    if "everest" in lower:

        queries.extend([
            "Mount Everest highest mountain above sea level NOAA",
            "Mount Everest highest elevation above sea level",
            "Mount Everest highest mountain official",
            "Mount Everest height NOAA",
            "Mount Everest highest point sea level Britannica"
        ])

    if "ocean" in lower:

        queries.extend([
            claim + " NOAA",
            claim + " official source",
            "Pacific Ocean largest ocean NOAA",
            "largest ocean on Earth official"
        ])

    if (
        "population" in lower
        or "populous" in lower
    ):

        queries.extend([
            claim + " UN population",
            claim + " official population",
            claim + " population latest",
            claim + " population ranking"
        ])

    if any(
        word in lower
        for word in [
            "founded",
            "established",
            "created",
            "discovered",
            "born",
            "died"
        ]
    ):

        queries.extend([
            claim + " official source",
            claim + " history",
            claim + " historical source"
        ])

    if "united nations" in lower:

        queries.extend([
            "United Nations founded 1945 official",
            "United Nations established 1945 UN",
            "United Nations Charter 1945",
            "United Nations history founding date"
        ])

    if re.search(
        r"\d+(?:\.\d+)?",
        claim
    ):

        queries.extend([
            claim + " official data",
            claim + " authoritative source",
            claim + " fact check"
        ])

    if any(
        word in lower
        for word in [
            "will",
            "by 2030",
            "by 2040",
            "by 2050",
            "future",
            "prediction",
            "forecast"
        ]
    ):

        queries.extend([
            claim + " projection",
            claim + " forecast",
            claim + " scientific projection",
            claim + " official report"
        ])

    queries.extend([
        claim + " official source",
        claim + " reliable source",
        claim + " evidence",
        claim + " fact check"
    ])

    if deep:

        queries.extend([
            claim + " Reuters",
            claim + " AP News",
            claim + " BBC",
            claim + " fact check",
            claim + " official report"
        ])

    unique = []
    seen = set()

    for query in queries:

        normalized = query.lower().strip()

        if normalized in seen:
            continue

        seen.add(normalized)

        unique.append(query)

    return unique
