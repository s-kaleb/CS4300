import pytest

# using capsys because we only want to capture stdout
def test_task1_output(capsys):
    # Importing main function from task1.py
    from src.task1 import main
    
    # Call the function
    main()
    
    # Capture the output
    captured = capsys.readouterr()

    # Check the stdout output against the correct string
    assert captured.out == "Hello, World!"