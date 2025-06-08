#Generate a random password of a given length1
import random
import string
# Prompt the user for the length of the password
long = int(input("Enter a long till 12 signs: "))
# Check if the number is positive      
if long < 0:
    print("The signs must be positive")
elif long > 12:
    print("The signs must be less than 12")
else:
    password = ""
    for i in range(long):
        # Generate a random character from the set of digits, uppercase and lowercase letters
        password += random.choice("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ./-_=+!@#$%^&*()")
    print("Your password is: " + password)
    with open("password.txt", "w") as file:
        file.write(password)
    print("Password saved to password.txt")
    print("You can copy it from there")

# Note: This code generates a random password and saves it to a file named "password.txt".
# The password consists of digits, uppercase and lowercase letters, and special characters.

    
