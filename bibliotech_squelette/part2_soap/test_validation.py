
import pytest

from db import validate_book


def test_valid_book():
    validate_book(1, "Clean Code", "Robert C. Martin", 5, 3.5)


def test_negative_stock():
    with pytest.raises(ValueError):
        validate_book(1, "Clean Code", "Robert C. Martin", -1, 3.5)


def test_negative_price():
    with pytest.raises(ValueError):
        validate_book(1, "Clean Code", "Robert C. Martin", 5, -1)


def test_invalid_id():
    with pytest.raises(ValueError):
        validate_book(0, "Clean Code", "Robert C. Martin", 5, 3.5)


def test_empty_title():
    with pytest.raises(ValueError):
        validate_book(1, "  ", "Robert C. Martin", 5, 3.5)


def test_empty_author():
    with pytest.raises(ValueError):
        validate_book(1, "Clean Code", "", 5, 3.5)
