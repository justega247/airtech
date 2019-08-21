from django.test import TestCase

# Create your tests here.


def add(a, b):
    return a + b


def test_add_function():
    assert add(3, 7) == 10
