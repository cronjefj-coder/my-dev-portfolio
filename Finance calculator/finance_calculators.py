#********** Pseudocode **********

# ASSUMPTIONS: There is only an error message required for initial incorrect inputs. No allowance given for
# accidental incorrect inputs during interest calculations shch as a negative interest rate.

# ADDITIONAL COMMENTS:
# This program could be optimised with the use of iteration or while loops to continue asking for an input
# until correct, also not to exit the code unnecessarily and handle errors better but for the purpose of
# this project and because iteration was not yet learnt at this stage, the current structure of code will
# comply to required specifications.

# Import the math library.

# Provide a definition of Investment versus Bond and then request the user to choose an option
# between either "investment" or "bond". Note that the input should not be case sensitive.

# Use if-elif-else statements to handle options

# If the user types the choices incorrectly, print an error message and end the program.

# For the investment option, request the user to input amount to be invested, then the interest rate
# (only number) and then the number of years they want to invest. Lastly the user must choose between
# simple and compound interest.

# Print out the results based on the decision according to the relevant interest formulae.

# For the bond option request the user to input the present value of the property, the interest rate
# (number only) and the number of months they want to take to repay the bond.

# Print out the repayment value per month.

#********** End of Pseudocode **********


# Import the math library.
import math

# Definitions and user input for options
print("Investment - to calculate the amount of interest you'll earn on\nyour investment.")
print("Bond       - to calculate the amount you'll have to pay on a home\nloan.\n")

calc_option = input("Enter either 'investment' or 'bond' from the menu above to\nproceed: ")
calc_option = calc_option.lower()

# This will be a control loop to handle the calculations for the two options and an error if the
# option is inserted incorrectly.

if calc_option == "investment":
    P = float(input("Please insert the amount you want to invest: "))
    r = float(input("Please insert the interest rate (e.g. 8 for 8%): ")) / 100
    t = int(input("Please insert the number of years you want to invest: "))
    interest = input("Please choose between 'simple' or 'compound' interest: ")

    if interest.lower() == "simple":
        simple = round(P * (1 + r*t),2)  # Simple interest formula
        
        print("\nYour total amount with simple interest is: {}.".format(simple))
        
    elif interest.lower() == "compound":
        compound = round(P * math.pow((1+r),t),2) # compound interest formula
        
        print("Your total amount with compount interest is: {}.".format(compound))

    else:
        print("You made and incorrect choice. Please choose 'simple' or 'compound'.")    
  

elif calc_option == "bond":
    P = float(input("Please insert the current value of the property: "))
    i = float(input("Please insert the interest rate on the bond: ")) / 100 / 12
    n = int(input("Please insert the number of months you are taking the bond: "))

    repayment = round((i *P)/(1 - (1 + i)**(-n)),2) # Bond repayment formula

    print("Your monthly repayment amount is: {}.".format(repayment))
    

else:
    print("Your input was incorrect. Please re-run the program to try again.")

# End of script.




    



