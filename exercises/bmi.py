#!/usr/bin/env python3

# BMI = (weight in kg / height in meters sqaured)
# BMI Imperial version = (weight in pounds / height in inches squared) * 703

def gather_info():
    height = float(input("What is your height? (inches or meters) "))
    weight = float(input("What is your weight? (pounds or kilos) "))
    system = input("Are your measurements in metric or imperial units? ").lower().strip()

    #returns multiple values using a tuple
    return (height, weight, system)

def calculate_bmi(weight, height, system='metric'): #assigned a default value for 'system' in the case that user leaves that blank
    """
    Return the Body Mass Index (BMI) for the 
    given weight, height, and measurement system.
    """
    if system == 'metric':
        bmi = (weight / (height ** 2))
    else:
        bmi = 703 * (weight / (height ** 2))
    return bmi

# Ensure that what the user gives us actually works. Input validation
while True:
    #tuple unpacking below to set multiple variables at once. Function is called, and then the return values are assigned to the variables on the left
    height, weight, system = gather_info()
    if system.startswith('i'):
        bmi = calculate_bmi(weight, system='imperial', height=height)
        print(f"Your BMI is {bmi}")
        break
    elif system.startswith('m'):
        bmi = calculate_bmi(weight, height)
        print(f"Your BMI is {bmi}")
        break
    else:
        print('Error: Unknown measurement system. Please use imperial or metric.')