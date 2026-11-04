import re
from functools import lru_cache

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

from evidence.fact_checker import (
    fact_check
)

MODEL_NAME = "cross-encoder/nli-MiniLM2-L6-H768"

@lru_cache(maxsize=1)
def get_nli_components():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    model.eval()

    labels = {}
    for index, label in model.config.id2label.items():
        label = label.lower()
        if not label.startswith("label_"):
            labels[index] = label

    return tokenizer, model, labels

def normalize_claim(claim):

    if not claim:
        return ""

    return re.sub(
        r"\s+",
        " ",
        claim.strip()
    )

def analyze_claim_against_evidence(
    claim,
    evidence_text
):

    if not claim or not evidence_text:

        return {
            "label": "neutral",
            "confidence": 0.0,
            "entailment": 0.0,
            "contradiction": 0.0,
            "neutral": 0.0,
            "directness": 0.0
        }

    claim = normalize_claim(
        claim
    )

    evidence_text = evidence_text.strip()

    tokenizer, model, model_labels = get_nli_components()

    inputs = tokenizer(
        evidence_text,
        claim,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.no_grad():

        outputs = model(
            **inputs
        )

    probabilities = torch.softmax(
        outputs.logits,
        dim=1
    )[0]

    entailment_index = None
    contradiction_index = None
    neutral_index = None

    for index, label in model_labels.items():

        if "entail" in label:
            entailment_index = index

        elif "contrad" in label:
            contradiction_index = index

        elif "neutral" in label:
            neutral_index = index

    if (
        entailment_index is None
        or contradiction_index is None
        or neutral_index is None
    ):

        contradiction_index = 0
        entailment_index = 1
        neutral_index = 2

    entailment = float(
        probabilities[
            entailment_index
        ]
    )

    contradiction = float(
        probabilities[
            contradiction_index
        ]
    )

    neutral = float(
        probabilities[
            neutral_index
        ]
    )

    scores = {
        "entailment": entailment,
        "contradiction": contradiction,
        "neutral": neutral
    }

    label = max(
        scores,
        key=scores.get
    )

    confidence = scores[label]

    return {
        "label": label,
        "confidence": round(
            confidence,
            4
        ),
        "entailment": round(
            entailment,
            4
        ),
        "contradiction": round(
            contradiction,
            4
        ),
        "neutral": round(
            neutral,
            4
        ),
        "directness": 0.0
    }

def analyze_evidence(
    claim,
    evidence
):

    analyzed = []

    for item in evidence:

        evidence_text = item.get(
            "evidence_text",
            ""
        )

        nli = analyze_claim_against_evidence(
            claim,
            evidence_text
        )

        structured = fact_check(
            claim,
            evidence_text
        )

        relationship = nli["label"]

        directness = 0.0

        if structured["relation"] == "support":

            relationship = "entailment"
            directness = 1.0

        elif structured["relation"] == "contradict":

            relationship = "contradiction"
            directness = 1.0

        else:

            if (
                nli["label"] == "entailment"
                and nli["entailment"] >= 0.75
            ):

                directness = 0.5

            elif (
                nli["label"] == "contradiction"
                and nli["contradiction"] >= 0.75
            ):

                directness = 0.5

            else:

                relationship = "neutral"

        analyzed.append({

            **item,

            "relationship":
                relationship,

            "nli_confidence":
                nli["confidence"],

            "entailment_probability":
                nli["entailment"],

            "contradiction_probability":
                nli["contradiction"],

            "neutral_probability":
                nli["neutral"],

            "directness":
                directness,

            "structured":
                structured["relation"]
                != "neutral",

            "fact_relation":
                structured["relation"],

            "fact_confidence":
                structured["confidence"],

            "fact_reason":
                structured["reason"]
        })

    return analyzed

def summarize_evidence(
    analyzed_evidence
):

    supporting = 0
    contradicting = 0
    neutral = 0

    supporting_weight = 0.0
    contradicting_weight = 0.0
    neutral_weight = 0.0

    for item in analyzed_evidence:

        source_score = float(
            item.get(
                "source_score",
                0
            )
        )

        source_weight = (
            source_score / 100
        )

        entailment = float(
            item.get(
                "entailment_probability",
                0
            )
        )

        contradiction = float(
            item.get(
                "contradiction_probability",
                0
            )
        )

        neutral_probability = float(
            item.get(
                "neutral_probability",
                0
            )
        )

        if item.get(
            "fact_relation"
        ) == "support":

            supporting += 1
            supporting_weight += (
                source_weight
            )

        elif item.get(
            "fact_relation"
        ) == "contradict":

            contradicting += 1
            contradicting_weight += (
                source_weight
            )

        elif item.get(
            "relationship"
        ) == "entailment":

            supporting += 1

            supporting_weight += (
                entailment
                * source_weight
            )

        elif item.get(
            "relationship"
        ) == "contradiction":

            contradicting += 1

            contradicting_weight += (
                contradiction
                * source_weight
            )

        else:

            neutral += 1

            neutral_weight += (
                neutral_probability
                * source_weight
            )

    return {

        "supporting":
            supporting,

        "contradicting":
            contradicting,

        "neutral":
            neutral,

        "supporting_weight":
            round(
                supporting_weight,
                3
            ),

        "contradicting_weight":
            round(
                contradicting_weight,
                3
            ),

        "neutral_weight":
            round(
                neutral_weight,
                3
            )
    }
