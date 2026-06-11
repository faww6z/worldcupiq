from app.ml.poisson import result_probabilities, scoreline_probabilities


def test_scoreline_matrix_sums_close_to_one() -> None:
    scorelines = scoreline_probabilities(1.5, 1.1)

    assert abs(sum(scoreline.probability for scoreline in scorelines) - 1) < 0.000001


def test_result_probabilities_sum_to_one() -> None:
    scorelines = scoreline_probabilities(1.5, 1.1)
    probabilities = result_probabilities(scorelines)

    assert abs(sum(probabilities) - 1) < 0.000001


def test_predicted_score_shape() -> None:
    scorelines = scoreline_probabilities(1.5, 1.1)
    predicted = max(scorelines, key=lambda scoreline: scoreline.probability)

    assert isinstance(predicted.score_a, int)
    assert isinstance(predicted.score_b, int)

