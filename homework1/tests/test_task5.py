from src.task5 import book_slice, student_database

# test the book_slice function
def test_book_slice(capsys):
    book_slice()
    captured = capsys.readouterr()
    assert captured.out == "['Harry Potter: J.K. Rowling', 'The Hunger Games: - Suzanne Collins', 'The Old Man and the Sea : Ernest Hemingway']\n"

#test the student_database function
def test_student_database(capsys):
    for index in range(1,8):
        student_database(index)
    
    captured = capsys.readouterr()
    assert captured.out == "['Kaleb Stamey', '1']\n['Belak Yemats', '2']\n['Charles Button', '3']\n['Sam Jo Belson', '4']\n['Coro Art', '5']\n['Castle Beleney', '6']\n['Uncla Johnson', '7']\n"
