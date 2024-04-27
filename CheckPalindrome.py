str1 = input("Enter a string:")
str2 = str1[::-1]

if str1 == str2:
    print(f"{str1} is a palindrome")
else:
    print(f"{str1} is not a palindrome")
