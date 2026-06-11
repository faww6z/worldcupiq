from __future__ import annotations

from dataclasses import dataclass
from math import exp, factorial


@dataclass(frozen=True)
class ScorelineProbability:
    score_a: int
    score_b: int
    probability: float


def poisson_probability(goals: int, expected_goals: float) -> float:
    if goals < 0:
        raise ValueError("goals must be non-negative")
    if expected_goals <= 0:
        raise ValueError("expected_goals must be positive")
    return (expected_goals**goals * exp(-expected_goals)) / factorial(goals)


def scoreline_probabilities(
    expected_goals_a: float,
    expected_goals_b: float,
    max_goals: int = 6,
) -> list[ScorelineProbability]:
    raw: list[ScorelineProbability] = []
    for score_a in range(max_goals + 1):
        prob_a = poisson_probability(score_a, expected_goals_a)
        for score_b in range(max_goals + 1):
            prob_b = poisson_probability(score_b, expected_goals_b)
            raw.append(ScorelineProbability(score_a=score_a, score_b=score_b, probability=prob_a * prob_b))

    total = sum(scoreline.probability for scoreline in raw)
    return [
        ScorelineProbability(
            score_a=scoreline.score_a,
            score_b=scoreline.score_b,
            probability=scoreline.probability / total,
        )
        for scoreline in raw
    ]


def result_probabilities(scorelines: list[ScorelineProbability]) -> tuple[float, float, float]:
    team_a_win = sum(scoreline.probability for scoreline in scorelines if scoreline.score_a > scoreline.score_b)
    draw = sum(scoreline.probability for scoreline in scorelines if scoreline.score_a == scoreline.score_b)
    team_b_win = sum(scoreline.probability for scoreline in scorelines if scoreline.score_a < scoreline.score_b)
    return team_a_win, draw, team_b_win

