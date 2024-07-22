def bmi():
    name = input("Enter your name: ")

    weight_input = input("Enter your weight in kg: ")
    height_input = input("Enter your height in meters: ")
    
    weight = float(weight_input)
    height = float(height_input)

    if weight <= 0 or height <= 0:
        print("Weight and height must be positive numbers.")
        return

    bmi = weight / (height ** 2.0)

    if bmi < 18.5:
        print(f"{name}, your BMI is {bmi:.2f}. You are underweight.")
    elif bmi < 24.9:
        print(f"{name}, your BMI is {bmi:.2f}. Congratulations, you are healthy.")
    elif bmi < 30:
        print(f"{name}, your BMI is {bmi:.2f}. You are overweight.")
    else:
        print(f"{name}, your BMI is {bmi:.2f}. You are in the obesity range.")

if __name__ == "__main__":
    bmi()
