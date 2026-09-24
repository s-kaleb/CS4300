from src.task7 import array_multiplication, matrix_multiplication, matrix_shape

# test output of each function 
def test_array_multiplication(capsys):
    array_multiplication()
    captured = capsys.readouterr()
    assert captured.out == "[  1   4   9  16  25  36  49  64  81 100]\n"

def test_matrix_multiplication(capsys):
    matrix_multiplication()
    captured = capsys.readouterr()
    assert captured.out == "[[14  8]\n [14  8]]\n"

def test_matrix_shape(capsys):
    matrix_shape()
    captured = capsys.readouterr()
    assert captured.out == "(2, 4)\n"