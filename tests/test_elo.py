import pytest

from elo_rating import Elo


def test_two_players():
    elo_sys = Elo()
    elo_sys.add_match("p1", "p2", 1, k=0.3)

    assert elo_sys.rating("p1") == pytest.approx(0.15)
    assert elo_sys.rating("p2") == pytest.approx(-0.15)
    assert elo_sys.ranking("p1") == 0
    assert elo_sys.ranking("p2") == 1


def test_rankings_and_ratings_and_items():
    elo_sys = Elo()
    elo_sys.add_match("p1", "p2", 1, k=0.3)

    assert elo_sys.rankings() == {"p1": 0, "p2": 1}
    assert elo_sys.ratings() == {"p1": pytest.approx(0.15), "p2": pytest.approx(-0.15)}
    assert sorted(elo_sys.items()) == sorted(["p1", "p2"])


def test_add_matches():
    elo_sys = Elo()
    elo_sys.add_matches([("p1", "p2", 1), ("p1", "p2", 0.5)])

    assert sorted(elo_sys.items()) == sorted(["p1", "p2"])
    assert elo_sys.rating("p1") == pytest.approx(0.04750208)
    assert elo_sys.rating("p2") == pytest.approx(-0.04750208)


def test_add_matches_with_unseen_item():
    elo_sys = Elo()
    elo_sys.add_matches([("p1", "p2", 1), ("p1", "p2", 0.5)])

    elo_sys.add_match("p2", "p3", 1.0)
    assert "p3" in elo_sys.items()
    assert elo_sys.rating("p3") == pytest.approx(-0.0511873)


def test_default_rating():
    elo_sys = Elo()
    elo_sys.add_matches([("p1", "p2", 1), ("p1", "p2", 0.5)])

    elo_sys.add_match("p2", "p3", 1.0, default_rating=100)
    assert elo_sys.rating("p3") == pytest.approx(99.9)


def test_custom_denominator():
    elo_sys = Elo(denom=400)
    elo_sys.add_match("p1", "p2", 1, k=30, default_rating=1400)

    assert elo_sys.rating("p1") == pytest.approx(1415)
    assert elo_sys.rating("p2") == pytest.approx(1385)
