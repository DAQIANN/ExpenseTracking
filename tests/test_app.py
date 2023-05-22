from ExpenseTracker.app import greeting

def test_name():
    assert greeting("Daniel") == "Hello, Daniel"

def test_empty():
    assert greeting("") == "Hello, stranger"

def test_first():
    "An initial test for the app"
    assert 1 + 1 == 2
