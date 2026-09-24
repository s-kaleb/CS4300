from src.task3 import num_sign, print_primes, sum_100

# Functions for testing the sign
def test_sign_positive(capsys):
    num_sign(1)
    captured = capsys.readouterr()
    assert captured.out == "Positive"

def test_sign_negative(capsys):
    num_sign(-1)
    captured = capsys.readouterr()
    assert captured.out == "Negative"


def test_sign_zero(capsys):
    num_sign(0)
    captured = capsys.readouterr()
    assert captured.out == "Zero"


# Function for testing the first 10 primes calculation
def test_print_primes(capsys):
    print_primes()
    captured = capsys.readouterr()
    # to compare output against
    correct = "2\n3\n5\n7\n11\n13\n17\n19\n23\n29\n"
    assert captured.out == correct

#For testing the sum of 1 to 100
def test_sum_100(capsys):
    sum_100()
    captured = capsys.readouterr()
    
    assert captured.out == "5050"