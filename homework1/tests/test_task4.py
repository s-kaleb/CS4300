from src.task4 import calculate_discount


def test_discount_int(capsys):
    calculate_discount(100, 85)
    captured = capsys.readouterr()
    assert captured.out == "15.0"

def test_discount_float(capsys):
    calculate_discount(100.0, 85.0)
    captured = capsys.readouterr()
    assert captured.out == "15.0"

def test_discount_neg(capsys):
    calculate_discount(100, -85)
    captured = capsys.readouterr()
    assert captured.out == "185.0"

def test_discount_float_int(capsys):
    calculate_discount(100.0, 85)
    captured = capsys.readouterr()
    assert captured.out == "15.0"

def test_discount_int_float(capsys):
    calculate_discount(100, 85.0)
    captured = capsys.readouterr()
    assert captured.out == "15.0"
