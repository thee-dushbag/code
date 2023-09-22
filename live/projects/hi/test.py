import hi
import pytest
from hi._hi import HI_FORMAT, NAME_KEY

NAME = "Simon"


def test_hi_default_format():
    assert hi.hi(NAME) == HI_FORMAT.format(**{NAME_KEY: NAME})


def test_hi_Hi_format():
    FORMAT = "Hi {name}"
    KEY = "name"
    assert hi.hi(NAME, format=FORMAT) == FORMAT.format(**{KEY: NAME})


def test_hi_invalid_key():
    FORMAT = "Invalid Key: {INVALID_KEY}"
    KEY = "NAME"
    with pytest.raises(KeyError):
        hi.hi(NAME, key=KEY, format=FORMAT)


def test_hi_key():
    KEY = "NAME"
    FORMAT = "Hello {NAME}"
    assert hi.hi(NAME, key=KEY, format=FORMAT) == FORMAT.format(**{KEY: NAME})


if __name__ == "__main__":
    exit(pytest.main([__file__]))
