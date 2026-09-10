
# integer test
def test_task2_output1(capsys):
    # Importing main function from task1.py
    from src.task2 import int_stuff
    
    # Call the function
    int_stuff()
    # Capture the output
    captured = capsys.readouterr()
    # Check the stdout output against the correct string
    assert captured.out == "55"

# Floating point test
def test_task2_output2(capsys):
    # Importing main function from task1.py
    from src.task2 import flt_stuff
    # Call the function
    flt_stuff()
    # Capture the output
    captured = capsys.readouterr()
    # Check the stdout output against the correct string
    assert captured.out == "2.0"

# String test
def test_task2_output3(capsys):
    # Importing main function from task1.py
    from src.task2 import str_stuff
    # Call the function
    str_stuff()
    # Capture the output
    captured = capsys.readouterr()
    # Check the stdout output against the correct string
    assert captured.out == "Hello, World!"

# Boolean test
def test_task2_output4(capsys):
    # Importing main function from task1.py
    from src.task2 import bool_stuff
    # Call the function
    bool_stuff()
    # Capture the output
    captured = capsys.readouterr()
    # Check the stdout output against the correct string
    assert captured.out == "False"