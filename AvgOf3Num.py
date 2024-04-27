def calculate_avg(a, b, c):
    return (a + b + c) / 3

num1 = int(input("Enter 1st number: "))
num2 = int(input("Enter 2nd number: "))
num3 = int(input("Enter 3rd number: "))

average = calculate_avg(num1, num2, num3)
print("The average is:", average)
