from src.task6 import word_count

# test the length of a book
def test_book_slice(capsys):
    word_count("./homework1/src/task6_read_me.txt")
    captured = capsys.readouterr()
    assert captured.out == "104"