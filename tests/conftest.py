import pytest


@pytest.fixture
def long_number():
    return '736541084301358743000'

@pytest.fixture
def short_number():
    return '700792289606361'

@pytest.fixture
def empty_str():
    return ''
