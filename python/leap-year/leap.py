"""
A leap day calculator!

The year can be evenly divided by 4, is a leap year, unless:
The year can be evenly divided by 100, it is NOT a leap year, unless:
The year is also evenly divisible by 400. Then it is a leap year.

The years 2000 and 2400 are leap years, while 1800, 1900, 2100, 2200, 2300 and 2500 are NOT leap years.


"""
from functools import reduce

def is_leap(year):
    leap = False
    divisor=[4,100,400]
    result=[]

    for _ in divisor:
        result.append(year % _)

    sum=reduce(lambda x,y: x+y, result)
    if sum == 0: leap=True

    return leap

def main():
    
    year = int(input())
    print(f"Leap year is {is_leap(year)}")

if __name__ == "__main__":
    main()