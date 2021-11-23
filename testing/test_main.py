from main import *


def test_get_none():
    assert get_none() is None


def test_flatten_dict():
    assert isinstance(flatten_dict({"a": 42, "b": 3.14}), list)
    assert flatten_dict({"a": 42, "b": 3.14}) == [42, 3.14]
    assert flatten_dict({"a": [42, 350], "b": 3.14}) == [[42, 350], 3.14]
    assert flatten_dict({"a": {"inner_a": 42, "inner_b": 350}, "b": 3.14}) == [
        {"inner_a": 42, "inner_b": 350},
        3.14,
    ]


def test_flatten_nested_dict():
    assert isinstance(flatten_nested_dict({"a": 42, "b": 3.14}))
    assert flatten_nested_dict({"a": {"inner_a": 41, "inner_b": 350}, "b": 3.14}) == [
        41,
        350,
        3.14,
    ]
