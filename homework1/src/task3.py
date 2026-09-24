#Comment test 2 

#Checking sign of a number
def num_sign(num):
    if (num == 0):
        print("Zero",end = "")
    elif (num > 0):
        print("Positive",end = "")
    else:
        print("Negative",end = "")

#AI Assisted function first 10 primes
def print_primes():
    increment = 0
    number = 2

    # increment ten times to produce 10 primes
    while increment < 10:
        
        isPrime = True

        #checks remainder of all divisions up to that number
        #will break if any of those divisions is not the number itself
        #will not break for 2 or number because its the range of numbers
        #between 2 and number that are being checked
        for i in range(2, number):
            if number % i == 0:
                #not prime
                isPrime = False
                break
        
        #if the previous for loop never broke that means the number is prime
        #and we can print it
        if isPrime:
            print(number)
            increment += 1
        
        number +=1

#sum all numbers 1 to 100
def sum_100():
    currentValue = 1
    total = 0
    while currentValue <= 100:
        total += currentValue
        currentValue += 1
    print(total, end = "")