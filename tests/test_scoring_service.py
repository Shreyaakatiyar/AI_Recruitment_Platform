import pytest

from app.services.scoring_service import compute_experience_score
from app.utils.math_utils import cosine_similarity


def test_cosine_similarity_identical_vectors():
    assert cosine_similarity([1, 0, 0], [1, 0, 0]) == pytest.approx(1.0)


def test_cosine_similarity_orthogonal_vectors():
    assert cosine_similarity([1, 0], [0, 1]) == pytest.approx(0.0)


def test_experience_score_meets_requirement():
    assert compute_experience_score(3, 5) == 1.0


def test_experience_score_below_requirement():
    assert compute_experience_score(4, 2) == pytest.approx(0.5)


def test_experience_score_no_requirement_specified():
    assert compute_experience_score(None, 0) == 1.0


def test_experience_score_missing_candidate_data():
    assert compute_experience_score(3, None) == 0.0