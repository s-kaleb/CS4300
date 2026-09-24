
#List slice for books list
def book_slice():
    bookList = ["Harry Potter: J.K. Rowling", 
        "The Hunger Games: - Suzanne Collins", 
        "The Old Man and the Sea : Ernest Hemingway"]
    
    #prints up to and including the third book
    print(bookList[:3])

#dictionary database
def student_database(studentId):
    students = {
        "1" : ["Kaleb Stamey", "1"],
        "2" : ["Belak Yemats", "2"],
        "3" : ["Charles Button", "3"],
        "4" : ["Sam Jo Belson", "4"],
        "5" : ["Coro Art", "5"],
        "6" : ["Castle Beleney", "6"],
        "7" : ["Uncla Johnson", "7"]

    }
    print(students[str(studentId)])
