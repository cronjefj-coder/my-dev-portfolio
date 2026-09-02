# ===== Importing external modules ===========
'''This is the section where you will import modules'''
from datetime import datetime
from datetime import date
from tabulate import tabulate

# ==== Functions definitions ====
'''
This section will define functions to run the menu items rather than the
code blocks as in previous versions of the program. This will improve
modularity of the program.
'''
def reg_user():
    '''
    The reg_user function reads the user.txt file to determine the users
    already created. It asks the user to create a new username and password.
    When the username is created it will check if the user already exists and
    then prompt the user to enter a different name to prevent duplication.

    returns
    The function does not return anything but rather updates user.txt to store
    newly created users.
    '''
    # Initiate an empty user list:
    u_list = []

    # Read the user.txt file and append the u_list:
    with open("user.txt", "r") as file:

        for lines in file:
            temp = lines.strip()
            temp = temp.split(", ")
            u_list.append(temp)

    # A message to the user to explain the process:
    print("You have chosen to register a user. The following steps are "
            "required:\n"
            "1. Insert a new username.\n"
            "2. Insert a password.\n"
            "3. Confirm the password.\n\n"
            "Once the steps has been completed, the program will return"
            " to the main menu.\n")
    
    # Request a new username and check for duplicates:
    while True:
        new_user = input("New username: ")

        for idx in range(len(u_list)):
            if u_list[idx][0] == new_user:
                i = idx
                print(f"\n{u_list[i][0]} already exists. Please try a"
                      " different username.\n")
                break
            else:
                i = -1
        if i == -1:
            break
        
    # Request a new password and confirmation of password. If the passwords
    # do not match, the process is repeated until the passwords match.
    while True:
        new_pw = input("New password: ")
        conf_pw = input("Confirm new password: ")

        if new_pw == conf_pw:
            break
        else:
            print("The passwords do not match. Please try again.")

    # Write the new user to the user.txt file:
    with open("user.txt", "a") as file:

        file.write(f"\n{new_user}, {new_pw}")

    print("A new user has been created.\n")

    # End of function

def add_task():
    '''
    This function allows the user to add a task to tasks.txt file. The user
    should add the assigned user, task title, task description and due date.
    The function will default the task completion status to 'No'. After all
    inputs have been successfully added, the task will be written to the
    tasks.txt file.

    returns
    Nothing will be returned, only the tasks.txt file will be updated.
    '''
    username = input("Please input the assigned user: ")
    title = input("Please input the task title: ")
    task_desc = input("Please input a task description: ")

    # For the due date, this loop will validate the input of the user to ensure
    # a valid date is entered.
    while True:
        user_date = input("Please input a due date in format 'DD Mmm YYYY': ")

        try:
            due_date = datetime.strptime(user_date, "%d %b %Y").date()
            break
        except ValueError:
            print("Incorrect date or format. Please try again.")

    curr_date = date.today().strftime("%d %b %Y")
    status = "No"

    # The task is written to the tasks.txt file
    with open("tasks.txt", "a") as file:

        file.write(f"\n{username}, {title}, {task_desc}, {curr_date}, "
                   f"{user_date}, {status}")

    # End of function

def view_all():
    '''
    This function reads the tasks.txt file and displays all the tasks that is
    tracked by the task manager application.

    Returns
    Nothing is returned, only the output display of all tasks to the screen.
    '''
    # Reading file:
    with open("tasks.txt", "r") as file:

        for lines in file:

            temp = lines.strip()
            temp = temp.split(", ")

            print("_" * 70)
            print(f"\nTask:\t\t\t\t{temp[1]}")
            print(f"Assigned to:\t\t\t{temp[0]}")
            print(f"Date assigned:\t\t\t{temp[3]}")
            print(f"Due date:\t\t\t{temp[4]}")
            print(f"Task complete?\t\t\t{temp[5]}")
            print(f"Task description:\n{temp[2]}")

        print("_" * 70, "\n")

    # End of function

def edit_task(index, task_list):
    '''
    This function will be used inside the view_mine() function and will allow
    the user to edit their own tasks with relevant actions. One action is to
    re-assign the task to a new user, second is to change the due date of the
    selected action or thirdly to do both.

    Parameters
    This function takes in two parameters, first an index and secondly the
    main task list generated in view_mine() function. The index is also
    obtained from view_mine() and refers to a specific index in the task list
    to be edited.

    Returns
    The function does not return anything but writes the updates made to the
    specific task to the tasks.txt file.    
    '''
    # This loop will continuously as the user to make a choice for the relevant
    # action:
    while True:
        e_choice = input('''Which action do you want to complete?
ru - re-assign user.
cd - change due date.
db - change both the user and due date.
: ''')
        # Choice for re-assignment of a user:
        if e_choice == 'ru':
            new_user = input("Please provide the user name for"
                             " re-assignment: ")
            task_list[index][0] = new_user
            print(f"\nYou have successfully re-assigned {task_list[index][1]}"
                  f" to {task_list[index][0]}.")
            break

        # Choice for changing the due date:
        elif e_choice == 'cd':

            # The loop will take the user input and test if it is either in the
            # right format or if it is in the past. It will handle errors
            # accordingly:
            while True:
                try:
                    new_date = input("Please input a date in format 'DD Mmm "
                                     "YYYY': ")
                    due_date = datetime.strptime(new_date, "%d %b %Y").date()
                    curr_date = date.today()

                    if due_date > curr_date:
                        break
                    else:
                        print("Provided date is in the past. Please provide a "
                              "new date.")
                except ValueError:
                    print("Incorrect date or format. Please try again.")

            task_list[index][4] = new_date
            print(f"\nYour new due date is {task_list[index][4]}")
            break

        # Choice to change both user and due date. This is a repeat of both the
        # actions above:

        elif e_choice == 'db':
            new_user = input("Please provide the user name for"
                             " re-assignment: ")
            task_list[index][0] = new_user
            print(f"\nYou have successfully re-assigned {task_list[index][1]}"
                  f" to {task_list[index][0]}.")

            while True:
                try:
                    new_date = input("Please input a date in format 'DD Mmm "
                                     "YYYY': ")
                    due_date = datetime.strptime(new_date, "%d %b %Y").date()
                    curr_date = date.today()

                    if due_date > curr_date:
                        break
                    else:
                        print("Provided date is in the past. Please provide a "
                              "new date.")
                except ValueError:
                    print("Incorrect date or format. Please try again.")

            task_list[index][4] = new_date
            print(f"\nYour new due date is {task_list[index][4]}")
            break

        else:
            print("\nIncorrect choice. Please try again.\n")

    #Write changes to the tasks.txt file:
    with open("tasks.txt", "w") as file:

        for i in range(0, len(task_list)):
            file.write(f"{task_list[i][0]}, {task_list[i][1]}, "
                       f"{task_list[i][2]}, {task_list[i][3]}, "
                       f"{task_list[i][4]}, {task_list[i][5]}\n")

    # End of Function

def view_mine():
    '''
    This function will read the tasks.txt file and displays the specific tasks
    that is assigned to the current user that is logged into the program. It
    will then allow the user to select a task to edit. It will then evaluate if
    the selected task is already completed or not. If completed, the user will
    be prompted that they cannot edit a completed task. If the task is not
    completed, the user will be given two options. Firstly to mark the task as
    complete or secondly to edit the task.

    When the user chooses to mark a task as complete, the function will change
    the task completion status to 'Yes' and then update the tasks.txt file.
    When the user chooses to edit the task, the edit_task() function will be
    called. Please refer to the edit_task() function definition for more infor-
    mation on the edit_task() function.

    Returns
    The function does not return anything but updates the tasks.txt file if any
    editing was done.
    '''
    
    #Read the tasks.txt file and append lists accordingly
    with open("tasks.txt", "r") as file:

        # Two lists and a counter is initialised
        all_tasks = []
        my_tasks = []
        task_num = 1

        for lines in file:

            temp = lines.strip()
            temp = temp.split(", ")

            # Check assigned users in the file is the current_user logged in
            # and store the tasks if any is assigned:
            if temp[0] == curr_user:

                temp.append(task_num)
                my_tasks.append(temp)
                task_num += 1
            else:
                temp.append("N/A")

            all_tasks.append(temp)

        # If any tasks is assigned to the user it will be displayed else a
        # message will inform the user that they have no assigned tasks.
        if my_tasks != []:

            for i in range(len(my_tasks)):

                print("_" * 70)
                print(f"Task no:\t\t\t{my_tasks[i][6]}")
                print(f"Task:\t\t\t\t{my_tasks[i][1]}")
                print(f"Assigned to:\t\t\t{my_tasks[i][0]}")
                print(f"Date assigned:\t\t\t{my_tasks[i][3]}")
                print(f"Due date:\t\t\t{my_tasks[i][4]}")
                print(f"Task complete?\t\t\t{my_tasks[i][5]}")
                print(f"Task description:\n{my_tasks[i][2]}")

            print("_" * 70)

        else:
            print("\nYou have no tasks assigned to you.\n")

    # This next code block and while loops will cover user's choice to choose
    # a task to edit and will cover the different editing options.
    while True:
        try:
            u_choice = int(input("\nIf you want to edit a task please input"
                                 " the task number or -1 to go back to the"
                                 " main menu: "))   
                                         
            if u_choice == -1:
                break
            else:
                for i in range(len(all_tasks)):
                    if all_tasks[i][6] == u_choice:
                        idx = i

                try:
                    print(f"\nYou have chosen {all_tasks[idx][1]} for editing."
                          "\n")

                    # This if statement checks if the selected task is complete
                    # as completed tasks cannot be edited.
                    if all_tasks[idx][5] == 'Yes':
                        print("Your task is already completed.\n")
                        break

                    # The next while loop provides editing options
                    while True:
                        choice = input('''Please select an option:
mc - mark task complete
et - edit details
: ''')

                        # Change completion status of task and updates
                        # tasks.txt
                        if choice == 'mc':
                            all_tasks[idx][5] = 'Yes'
                            with open("tasks.txt", "w") as file:

                                for i in range(len(all_tasks)):
                                    file.write(f"{all_tasks[i][0]}, "
                                               f"{all_tasks[i][1]}, "
                                               f"{all_tasks[i][2]}, "
                                               f"{all_tasks[i][3]}, "
                                               f"{all_tasks[i][4]}, "
                                               f"{all_tasks[i][5]}\n")
                            break

                        # Edit details of the task using the edit_task()
                        # function.
                        elif choice == 'et':
                            edit_task(idx, all_tasks)
                            break

                        else:
                            print("\nIncorrect choice. Please try again.\n")
    
                    break

                except (NameError, ValueError):
                    print("\nIncorrect choice. Please try again.\n")

        except ValueError:
            print("\nPlease provide a task number.\n")
            



    # End of Function.

def view_completed():
    '''
    This function will display all the tasks if the status (completion)
    is 'Yes'. NOTE this function is only available for the admin user.
    If there are no completed tasks, a message will be displayed to confirm
    that there are no completed tasks.
    '''

    # Read the file tasks.txt and append the defined list:
    with open("tasks.txt", "r") as file:

        comp_tasks = []

        for lines in file:

            temp = lines.strip()
            temp = temp.split(", ")

            # Check if the status in the tasklist is 'Yes' and appends
            # comp_tasks if true:
            if temp[5] == 'Yes':
                comp_tasks.append(temp)

        # If there are completed tasks it will be displayed else the user
        # will be informed that there are no completed tasks:
        if comp_tasks != []:
            for i in range(len(comp_tasks)):
                print("_" * 70)
                print(f"\nTask:\t\t\t\t{comp_tasks[i][1]}")
                print(f"Assigned to:\t\t\t{comp_tasks[i][0]}")
                print(f"Date assigned:\t\t\t{comp_tasks[i][3]}")
                print(f"Due Date:\t\t\t{comp_tasks[i][4]}")
                print(f"Task description:\n{comp_tasks[i][2]}")

            print("_" * 70)

        else:
            print("\nThere are no completed tasks.\n")

    # End of Function.

def delete_task():
    '''
    This function allows the admin user to delete tasks from the task
    list. It reads and displays all the current tasks and numbers the
    tasks as well. It then provides an option to the user to delete a task.
    Once the task has been deleted, the tasks.txt file gets updated with
    the remaining tasks.
    '''

    # Read the tasks.txt file:
    with open("tasks.txt", "r") as file:

        # Initiate empty list and counter for task numbers:
        tasks = []
        task_num = 1

        for lines in flie:

            temp = lines.strip()
            temp = temp.split(", ")
            temp.append(task_num)
            tasks.append(temp)
            task_num += 1

            print("_" * 70)
            print(f"Task no:\t\t\t{temp[6]}")
            print(f"Task:\t\t\t\t{temp[1]}")
            print(f"Assigned to:\t\t\t{temp[0]}")
            print(f"Date assigned:\t\t\t{temp[3]}")
            print(f"Due date:\t\t\t{temp[4]}")
            print(f"Task complete?\t\t\t{temp[5]}")
            print(f"Task description:\n{temp[2]}")

        print("_" * 70)

    # This loop asks the user which task to delete and deletes it from the
    # tasks list:
    while True:
        try:
            del_task = int(input("\nEnter the task number you want to delete: "
                                 ))

            for idx in range(len(tasks)):
                if tasks[idx][6] == del_task:
                    i = idx

            tasks.pop(i)
            print(f"Task number {del_task} has been deleted.")
            break

        except (ValueError, NameError):
            print("Incorrect task number selected. Please try again.")

    # The tasks.txt file is updated:
    with open("tasks.txt", "w") as file:
        for i in range(len(tasks)):
            file.write(f"{all_tasks[i][0]}, {all_tasks[i][1]}, "
                       f"{all_tasks[i][2]}, {all_tasks[i][3]}, "
                       f"{all_tasks[i][4]}, {all_tasks[i][5]}\n")

    # End of Function.

def user_statistics(user, tasklist):
    '''
    This function calculates statistics about each registered user for use to
    generate a report in the gen_report() function. The calculated statistics
    include:
    - Number of tasks per user
    - % of the total number of tasks assigned per user
    - % tasks completed per user
    - % tasks still to complete per user
    - % tasks overdue per user

    Parameters
    The function has two parameters. The user parameter is used to identify the
    specific user to calculate statistics for.
    The second parameter is the task list that contains all the tasks tracked
    by the task manager program.

    Returns
    A list of the calculated statistics is returned from the function.
    '''
    # Variables defined to be used in function:
    task_tot = 0
    comp = 0
    od = 0
    curr_date = date.today()
    per_tasks = 0
    per_comp = 0
    per_inc = 0
    per_od = 0

    #For loop to calculate statistics per user:
    for i in range(len(tasklist)):

        # Calculate the due date to compare to current date:
        due_date = datetime.strptime(tasklist[i][4], '%d %b %Y').date()

        # Finds the user provided as paremeter and calculates the stats:
        if user == tasklist[i][0]:
            task_tot += 1   # Total tasks per user

            if tasklist[i][5] == 'Yes':
                comp += 1   # Total completed tasks

            if due_date < curr_date and tasklist[i][5] == 'No':
                od += 1     # Total overdue tasks

            # Calculating required percentages:
            per_tasks = round((task_tot / len(tasklist)) * 100, 2)
            per_comp = round((comp / task_tot) * 100, 2)
            per_inc = round(100 - per_comp, 2)
            per_od = round((od / task_tot) * 100, 2)

    # Returns the calculated statistics in a list
    return [user, task_tot, per_tasks, per_comp, per_inc, per_od]

    # End of Function

def task_statistics(tasklist):
    '''
    This function calculates statistics about the created tasks for use to
    generate a report in the gen_report() function. The calculated statistics
    include:
    - Total number of tasks
    - Total number of completed tasks
    - Total number of incompleted tasks
    - Total number of overdue tasks
    - % of incompleted tasks
    - % of overdue tasks

    Parameters
    The function takes a the task list generated from tasks.txt file as input
    to calculate the statistics.

    Returns
    A list of the calculated statistics is returned from the function.
    '''
    # Variables defined to use in calculations
    comp_tasks = 0
    od_tasks = 0
    curr_date = date.today()

    tot_tasks = len(tasklist)   # The total number of tasks created

    # This for loop runs through the list to calculate the required statistics:
    for i in range(tot_tasks):

        if tasklist[i][5] == 'Yes':
            comp_tasks += 1     # Number of completed tasks

        # Calculating the due date to compare with curr date:
        due_date = datetime.strptime(tasklist[i][4], '%d %b %Y').date()

        if tasklist[i][5] == 'No' and due_date < curr_date:
            od_tasks += 1   # Number of overdue tasks

    # Calculations of rest of the statistics:
    incomp_tasks = tot_tasks - comp_tasks
    pt_inc = round((incomp_tasks / tot_tasks) * 100, 2)
    pt_od = round((od_tasks / tot_tasks) * 100, 2)

    # Return the list of calculated statistics
    return [tot_tasks, comp_tasks, incomp_tasks, od_tasks, pt_inc, pt_od]

    # End of Function

def gen_report():
    '''
    This function will generate two text files. The first is task_overview.txt
    that contains the information generated in the task_statistics() function.
    The seconf file is user_overview.txt that will contain information from the
    user_statistics() function.
    The function reads information from both user.txt and tasks.txt to generate
    the required lists used in the applicable functions.

    This function does not have parameters and does not return anything other
    than generating the mentioned txt files.
    '''
    # Variables defined for use in function:
    tasks = []
    users = []
    user_stat = []

    # Reading the user.txt and tasks.txt files to generate lists:
    with open('user.txt', 'r') as file:

        for lines in file:
            temp = lines.strip().split(', ')
            users.append(temp[0])

    with open('tasks.txt', 'r') as file:

        for lines in file:
            temp = lines.strip().split(', ')
            tasks.append(temp)

    # Create task_overview.txt using task_statistics():
    task_stats = task_statistics(tasks)

    with open('task_overview.txt', 'w') as file:

        file.write("Total tasks, Completed, Incomplete, Overdue, "
                   "% Incomplete, % Overdue\n")
        file.write(f"{task_stats[0]}, {task_stats[1]}, {task_stats[2]}, "
                   f"{task_stats[3]}, {task_stats[4]}, {task_stats[5]}")

    # Create user_overview.txt using user_statistics():
    for i in range(len(users)):
        user_stat.append(user_statistics(users[i], tasks))

    with open('user_overview.txt', 'w') as file:

        file.write(f"Total users, {len(users)}\n")
        file.write(f"Total tasks, {task_stats[0]}\n")
        file.write("User, Tasks per user, % User tasks, % Completed, "
                   "% Incomplete, % Overdue\n")

        for i in range(len(user_stat)):
            file.write(f"{user_stat[i][0]}, {user_stat[i][1]}, "
                       f"{user_stat[i][2]}, {user_stat[i][3]}, "
                       f"{user_stat[i][4]}, {user_stat[i][5]}\n")

    # End of Function

def display_stats():
    '''
    This function allows the user to display the statistics generated in gen_
    report() function to the screen. In case the files have not been generated
    by the user, it will call gen_report() to first generate the txt files,
    then read the files and displays it to the screen in an easy to read
    format.

    The function does not return anyting but prints a report to the screen.
    '''
    gen_report()

    task_info = []
    user_info = []

    with open('task_overview.txt', 'r') as file:

        for lines in file:

            temp = lines.strip().split(', ')
            task_info.append(temp)

    with open('user_overview.txt', 'r') as file:

        for lines in file:

            temp = lines.strip().split(', ')
            user_info.append(temp)

    print("_" * 75)
    print("General task statistics:\n")
    print(f"Total tasks tracked:\t\t{task_info[1][0]}\n"
          f"Comleted tasks:\t\t\t{task_info[1][1]}\n"
          f"Incomplete tasks:\t\t{task_info[1][2]}\n"
          f"Overdue tasks:\t\t\t{task_info[1][3]}\n"
          f"Percentage incomplete tasks:\t{task_info[1][4]}%\n"
          f"Percentage overdue tasks:\t{task_info[1][5]}%\n")
    print("_" * 75)

    print("User statistics:\n")
    print(f"Total users registered:\t\t{user_info[0][1]}\n")

    headers = user_info[2]
    data = []

    for i in range(3, len(user_info)):
        data.append(user_info[i])

    print(tabulate(data, headers = headers, tablefmt = 'fancy_grid'))

    # End of Function
    
# ==== Login Section ====
# TODO: Implement the following functionality
'''Here you will write code that will allow a user to login.
    - Your code must read usernames and passwords from the user.txt file
    - You can use a list or dictionary to store a list of usernames and
       passwords from the file.
    - Use a while loop to validate your user name and password.
'''
# Welcome message:
print("Welcome to Task Manager. Please login.\n")

# Initiate an empty list to store users from text file:
user_list = []

# Reading and storing data from user.txt
with open("user.txt", "r") as file:

    for lines in file:

        temp = lines.strip()
        temp = temp.split(", ")
        user_list.append(temp)

# The following loop requests the user for username and checks if it is valid.
# It will continually request a username until a valid username is entered.
while True:
    try:
        user_input = input("Username: ")

        for idx in range(len(user_list)):
            if user_list[idx][0] == user_input:
                i = idx

        curr_user = user_list[i][0]
        break

    except NameError:
        print("The user does not exist. Please re-enter your username.")

# The following loop requests the user's password. If the password is not
# correct, the user will be continually asked to input until the password
# is correct.
while True:
    pword = input("Password: ")

    if user_list[i][1] == pword:
        break
    else:
        print("Your password is incorrect. Please try again.")

while True:
    '''
    Additional functionality will be added here to allow admin only function.
    For this, an if statement will be used to check the current user if it is
    admin. additional conditions will be added to the if statements below to
    restrict users to admin only. Two new admin processes will be added namely
    to view completed tasks and to delete tasks.
    '''

    # Admin check and menu.
    if curr_user == 'admin':
        menu = input(
            '''\nSelect the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
vc - view completed tasks
del - delete tasks
ds - display stiatistics
gr - generate report
e - exit
: '''
            ).lower()
    
    # Present the menu to the user and
    # make sure that the user input is converted to lower case.
    else:
        menu = input(
        '''\nSelect one of the following options:
a - add task
va - view all tasks
vm - view my tasks
e - exit
: '''
    ).lower()

    if menu == 'r' and curr_user == 'admin':
        # Call the reg_user() function
        reg_user()

    elif menu == 'a':
        # Call the add_task() function
        add_task()
        
    elif menu == 'va':
        # Call the view_all() function
        view_all()       
        
    elif menu == 'vm':
        # Call the view_mine() function
        view_mine()

    elif menu == 'vc' and curr_user == 'admin':
        view_completed()

    elif menu == 'del' and curr_user == 'admin':
        delete_task()

    elif menu == 'ds' and curr_user == 'admin':
        display_stats()

    elif menu == 'gr' and curr_user == 'admin':
        gen_report()
        print("Your report files have been generated. To view the statistics\n"
              "please select the ds option from the menu.")
               
    elif menu == 'e':
        print('Goodbye!!!')
        raise SystemExit()

    else:
        print("You have entered an invalid input. Please try again")
