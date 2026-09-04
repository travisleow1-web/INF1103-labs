#Activity 1
print("================")
print("Welcome Here")
print("My first post!")
print("================")

#3A) The program does display the way it was written
#3B) It follows a top to bottom approach, executing each line of code in the order it appears. The print statements are executed first, followed by the variable assignments and subsequent print statements that display the values of those variables. This sequential execution ensures that the output is generated in a logical and organized manner, reflecting the structure of the code as written.
#3C) The output of the program is displayed in the console or terminal where the code is executed. The print statements generate text output that is visible to the user, allowing them to see the welcome message, user information, and any other relevant details as specified in the code.

#Activity 2:
print("================")
print("Welcome Here")
print("My first post!")
print("================")

username = "cool_creator"
bio = "fun blogger"
followers = 100

print("Username: " ,username)
print("Bio: " ,bio)
print("Followers: " ,followers)
#2A) The use of having variables in this code is to store information about the user, such as their username, bio, and number of followers. This allows for easy access and modification of these values throughout the program.
#2B) If we are talking about the code stored inside the variables, when we change the value of the variables, the output when using said variables would change.

#Activity 3:
#1 
followers += 50
print("day 1:" ,followers)

followers += 20
print("day 2:" ,followers)

followers -= 10
print("day 3:" ,followers)

#2A) We do not need to manually reassign the value of followers each time we want to change it. Instead, we can use the += and -= operators to modify the value of followers based on the current value. This makes the code more efficient and easier to read.
#2B) It will affect the existing value of followers by adding or subtracting the specified amount, rather than replacing the entire value with a new one. This allows for more dynamic updates to the variable based on user interactions or other events in the program.

#Activity 4:
#1
username = input("Enter your username: ")
age = input("Enter your Age: ")
category = input("Enter Content category: ")

print("\nInstagram Profile")
print ("================")
print("Username: " ,username)
print("Age: " ,age)
print("Category: " ,category)

#2A) The input() function is used to take user input in the form of a string. It allows the program to prompt the user for information and store it in a variable for later use.
#2B) The program is now dynamic, allowing users to input their own information instead of using hardcoded values. This makes the program more interactive and personalized for each user.
#2C) Having ran the program with different inputs, we can see that the output changes based on the user's input. For example, if the user enters a different username, age, or category, the output will reflect those changes accordingly.
