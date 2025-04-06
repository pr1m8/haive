import pytest
from src.haive.tak.tools.corporate_bs_tool import get_random_corporate_bs


def test_get_random_corporate_bs():
    bs = get_random_corporate_bs()
    assert bs.phrase
    assert isinstance(bs.phrase, str)
    assert len(bs.phrase.split()) >= 3  # Buzzwords are never short ;)
