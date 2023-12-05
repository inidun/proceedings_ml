from proceedings_ml.evalution import evaluate, evaluate_span


# FIXME: Create validation data with a subset of annotated data
def test_evaluate_returns_perfect_scores_for_subset_of_annotated_data_as_validation_data():
    validation_set = "tests/fixtures/validation_data_correct.jsonl"
    model = "training/model-last"

    precision, recall, f1_score = evaluate(model, validation_set)

    assert precision == 1.0
    assert recall == 1.0
    assert f1_score == 1.0


def test_evaluate_span_returns_perfect_scores_for_subset_of_annotated_data_as_validation_data():
    validation_set = "tests/fixtures/validation_data_correct.jsonl"
    model = "training/model-last"
    label = "COUNTRY"

    precision, recall, f1_score = evaluate_span(model, validation_set, label)

    assert precision == 1.0
    assert recall == 1.0
    assert f1_score == 1.0
