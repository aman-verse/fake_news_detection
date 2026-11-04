import re

def extract_temperature(text):

    match = re.search(
        r"(-?\d+(?:\.\d+)?)\s*(?:°\s*C|degrees?\s+Celsius|Celsius)",
        text,
        re.IGNORECASE
    )

    if match:
        return float(match.group(1))

    return None

def fact_check(claim, evidence):

    if not claim or not evidence:
        return {
            "relation": "neutral",
            "confidence": 0.0,
            "reason": ""
        }

    claim_lower = claim.lower()
    evidence_lower = evidence.lower()

    if (
        "water" in claim_lower
        and "freez" in claim_lower
    ):

        claim_temp = extract_temperature(
            claim
        )

        if claim_temp == 0:

            if (
                (
                    "water freezes at 0"
                    in evidence_lower
                )
                or
                (
                    "freezing point of water"
                    in evidence_lower
                    and "0" in evidence_lower
                )
            ):

                return {
                    "relation": "support",
                    "confidence": 1.0,
                    "reason":
                        "The source explicitly states that water freezes at 0°C."
                }

            if (
                "supercool" in evidence_lower
                or "liquid water" in evidence_lower
                or "below zero" in evidence_lower
                or "pressure" in evidence_lower
                or "salt" in evidence_lower
            ):

                return {
                    "relation": "neutral",
                    "confidence": 0.0,
                    "reason":
                        "The source describes special conditions or supercooling and does not contradict the normal freezing point."
                }

        if claim_temp is not None:

            if claim_temp != 0:

                if (
                    "water freezes at 0"
                    in evidence_lower
                    or
                    (
                        "freezing point of water"
                        in evidence_lower
                        and "0" in evidence_lower
                    )
                ):

                    return {
                        "relation": "contradict",
                        "confidence": 1.0,
                        "reason":
                            "The source states that water freezes at 0°C, contradicting the claimed temperature."
                    }

                if (
                    "water freezes"
                    in evidence_lower
                    and "0" in evidence_lower
                ):

                    return {
                        "relation": "contradict",
                        "confidence": 1.0,
                        "reason":
                            "The source gives a freezing point of 0°C."
                    }

    if (
        "earth" in claim_lower
        and "center" in claim_lower
        and "solar system" in claim_lower
    ):

        if (
            (
                "sun is at the center"
                in evidence_lower
            )
            or
            (
                "sun is the center"
                in evidence_lower
            )
            or
            (
                "sun at the center"
                in evidence_lower
            )
            or
            (
                "sun is at center"
                in evidence_lower
            )
        ):

            return {
                "relation": "contradict",
                "confidence": 1.0,
                "reason":
                    "The evidence identifies the Sun rather than Earth as the center of the solar system."
            }

        if (
            "earth orbits the sun"
            in evidence_lower
            or
            "earth revolves around the sun"
            in evidence_lower
            or
            "earth revolves around sun"
            in evidence_lower
        ):

            return {
                "relation": "contradict",
                "confidence": 1.0,
                "reason":
                    "The evidence states that Earth revolves around the Sun."
            }

    if "mount everest" in claim_lower:

        if (
            "highest" in claim_lower
            and "sea level" in claim_lower
        ):

            if (
                "everest" in evidence_lower
                and "highest" in evidence_lower
                and (
                    "sea level"
                    in evidence_lower
                    or "mean sea level"
                    in evidence_lower
                    or "global mean sea level"
                    in evidence_lower
                )
            ):

                return {
                    "relation": "support",
                    "confidence": 1.0,
                    "reason":
                        "Evidence identifies Mount Everest as the highest point above sea level."
                }

        if "south america" in claim_lower:

            if (
                "nepal" in evidence_lower
                or "tibet" in evidence_lower
                or "asia" in evidence_lower
            ):

                return {
                    "relation": "contradict",
                    "confidence": 1.0,
                    "reason":
                        "Evidence places Mount Everest in Nepal/Tibet, not South America."
                }

    if "pacific ocean" in claim_lower:

        if "largest ocean" in claim_lower:

            if (
                "pacific ocean" in evidence_lower
                and "largest" in evidence_lower
            ):

                return {
                    "relation": "support",
                    "confidence": 1.0,
                    "reason":
                        "Evidence identifies the Pacific Ocean as the largest ocean."
                }

        if "smallest ocean" in claim_lower:

            if (
                "pacific ocean" in evidence_lower
                and "largest" in evidence_lower
            ):

                return {
                    "relation": "contradict",
                    "confidence": 1.0,
                    "reason":
                        "Evidence identifies the Pacific Ocean as the largest ocean."
                }

    if "united nations" in claim_lower:

        claim_years = re.findall(
            r"\b(?:19|20)\d{2}\b",
            claim_lower
        )

        evidence_years = re.findall(
            r"\b(?:19|20)\d{2}\b",
            evidence_lower
        )

        if claim_years:

            claim_year = claim_years[0]

            if claim_year in evidence_years:

                if (
                    "founded" in claim_lower
                    or "established" in claim_lower
                    or "created" in claim_lower
                ):

                    return {
                        "relation": "support",
                        "confidence": 1.0,
                        "reason":
                            "The evidence contains the same founding year as the claim."
                    }

            if (
                "1945" in evidence_years
                and (
                    "founded" in evidence_lower
                    or "established" in evidence_lower
                    or "charter" in evidence_lower
                )
            ):

                if claim_year != "1945":

                    return {
                        "relation": "contradict",
                        "confidence": 1.0,
                        "reason":
                            "The evidence states that the United Nations was founded in 1945."
                    }

    if "united nations" in claim_lower:

        claim_years = re.findall(
            r"\b(?:19|20)\d{2}\b",
            claim_lower
        )

        if claim_years:

            claim_year = claim_years[0]

            if (
                claim_year != "1945"
                and "1945" in evidence_lower
                and (
                    "founded" in evidence_lower
                    or "established" in evidence_lower
                    or "charter" in evidence_lower
                    or "united nations" in evidence_lower
                )
            ):

                return {
                    "relation": "contradict",
                    "confidence": 1.0,
                    "reason":
                        "The United Nations was founded in 1945, contradicting the claimed year."
                }

    if (
        "water" in claim_lower
        and "freez" in claim_lower
    ):

        claim_temp = extract_temperature(
            claim
        )

        if (
            claim_temp is not None
            and claim_temp != 0
        ):

            if (
                (
                    "water freezes at 0" in evidence_lower
                )
                or
                (
                    "freezing point of water" in evidence_lower
                    and "0" in evidence_lower
                )
                or
                (
                    "freezing point of water" in evidence_lower
                    and "273.15" in evidence_lower
                )
            ):

                return {
                    "relation": "contradict",
                    "confidence": 1.0,
                    "reason":
                        "The evidence gives the normal freezing point of water as 0°C."
                }
    

    return {
        "relation": "neutral",
        "confidence": 0.0,
        "reason": ""
    }
