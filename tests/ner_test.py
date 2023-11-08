import pytest
import spacy


def get_entities_with_pos(text, nlp):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_, ent.start_char, ent.end_char))
    return entities


def test_ner_entities_using_en_core_web_lg_are_as_expected():
    nlp = spacy.load("en_core_web_lg")
    text = "M. Camille HUYSMANS (Belgium) (Chairman of the Credentials Committee) (Translation):"

    entities = get_entities_with_pos(text, nlp)

    expected = [
        ("M. Camille HUYSMANS", "PERSON", 0, 19),
        ("Belgium", "GPE", 21, 28),
        ("the Credentials Committee", "ORG", 43, 68),
    ]

    assert entities == expected


@pytest.mark.skip(reason="not applicable")
def test_spans_using_model_best_are_as_expected():
    nlp = spacy.load("training/model-best")
    text = "M. Camille HUYSMANS (Belgium) (Chairman of the Credentials Committee) (Translation):"

    doc = nlp(text)
    spans = list(doc.spans["sc"])
    result = [(span.text, span.label_, span.start_char, span.end_char) for span in spans]

    expected = [("Belgium", "COUNTRY", 21, 28)]

    assert result == expected
