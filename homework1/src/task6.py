# check word count in a text file 

def word_count(filename):
    textFile = open(filename, "r")
    totalWords = 0
    text = textFile.read().split()
    for i in range(len(text)):
        totalWords +=1
    print(totalWords, end = "")
