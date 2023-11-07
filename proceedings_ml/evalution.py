import json
from pathlib import Path

import spacy
from spacy.tokens import Span


def evaluate(model: str | Path, validation_data: str | Path) -> tuple[float, float, float]:
    """Evaluate a model on a validation set. Returns the precision, recall, and F1-score for the model.

    - Precision: The fraction of true positive spans (correctly predicted) out of all predicted spans.
    - Recall: The fraction of true positive spans out of all actual spans.
    - F1-Score: The harmonic mean of precision and recall, often used when there's an imbalance between classes.

    Args:
        model (str | Path): Name of the model to evaluate.
        validation_data (str | Path): Path to the validation data.

    Returns:
        tuple[float, float, float]: Precision, recall, and F1-score.

    Example:

        >>> from proceedings_ml.evalution import evaluate
        >>> evaluate("model", "validation_data.jsonl")
        Precision: 1.0
        Recall: 1.0
        F1-Score: 1.0
        (1.0, 1.0, 1.0)
    """
    nlp = spacy.load(model)

    with open(validation_data, "r", encoding="utf-8") as file:
        data = [json.loads(line) for line in file]

    # Initialize counters for metrics
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for example in data:
        doc = nlp(example["text"])
        annotated_spans = [
            Span(doc, span["token_start"], span["token_end"] + 1, label=span["label"]) for span in example["spans"]
        ]

        predicted_spans = [span for span in doc.spans["sc"]]

        # Calculate metrics
        for span in annotated_spans:
            if span in predicted_spans:
                true_positives += 1
            else:
                false_negatives += 1

        for span in predicted_spans:
            if span not in annotated_spans:
                false_positives += 1

    # Calculate precision, recall, and F1-score
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    f1_score = 2 * (precision * recall) / (precision + recall)

    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1-Score: {f1_score}")

    return precision, recall, f1_score


# FIXME: Remove this function and make evaluate() more generic instead
def evaluate_span(
    model: str | Path, validation_data: str | Path, label: str
) -> tuple[float, float, float]:
    """Evaluate a model on a validation set. Returns the precision, recall, and F1-score for spans with label `label`.

    - Precision: The fraction of true positive spans (correctly predicted) out of all predicted spans.
    - Recall: The fraction of true positive spans out of all actual spans.
    - F1-Score: The harmonic mean of precision and recall, often used when there's an imbalance between classes.

    Args:
        model (str | Path): Name of the model to evaluate.
        validation_data (str | Path): Path to the validation data.
        label (str): The label of the span to evaluate.

    Returns:
        tuple[float, float, float]: _description_

    Example:

        >>> from proceedings_ml.evalution import evaluate_span
        >>> evaluate_span("model", "validation_data.jsonl", "ORG")
        Label: ORG
        True positives: 1
        False positives: 0
        False negatives: 0
        Precision: 1.0
        Recall: 1.0
        F1-Score: 1.0
        (1.0, 1.0, 1.0)
    """
    nlp = spacy.load(model)

    with open(validation_data, "r", encoding="utf-8") as file:
        data = [json.loads(line) for line in file]

    # Initialize counters for metrics
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for example in data:
        doc = nlp(example["text"])
        annotated_spans = [
            Span(doc, span["token_start"], span["token_end"] + 1, label=span["label"])
            for span in example["spans"]
            if span["label"] == label
        ]

        predicted_spans = [span for span in doc.spans["sc"] if span.label_ == label]

        # Calculate metrics
        for span in annotated_spans:
            if span in predicted_spans:
                true_positives += 1
            else:
                false_negatives += 1

        for span in predicted_spans:
            if span not in annotated_spans:
                false_positives += 1

    # Calculate precision, recall, and F1-score
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    f1_score = 2 * (precision * recall) / (precision + recall)

    print(f"Label: {label}")

    print(f"True positives: {true_positives}")
    print(f"False positives: {false_positives}")
    print(f"False negatives: {false_negatives}")

    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1-Score: {f1_score}")

    return precision, recall, f1_score


if __name__ == "__main__":
    pass
