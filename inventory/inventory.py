from tabulate import tabulate
import os

# constants
FILE_PATH = "./inventory.txt"

# global variables
shoe_list = []
file_header = []
is_file_Loaded = False

# this class is used to represent a shoe
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"


# this function read data from the file
# and add parse each line to a shoe object and add it to the shoe_list
# it also extracts the first line as header and store it in a global variable to use in other functions
def read_shoes_data():
    with open(FILE_PATH, "r") as inventory_file:
        items = inventory_file.readlines()

    for index, item in enumerate(items):
        if index == 0:
            # allows change file_header value outside of its current scope
            global file_header
            file_header = item.strip("\n").split(",")
            continue

        try:
            country, code, product, cost_str, quantity_str = item.strip("\n").split(",")
        except ValueError:
            print(f"Not enough values to unpack in the line {(index + 1)}, it's ignored")
            continue

        try:
            cost = float(cost_str)
        except ValueError:
            print(f"The cost value is not a number in the line {(index + 1)}, it's ignored")
            continue

        try:
            quantity = int(quantity_str)
        except ValueError:
            print(f"The quantity value is not a number in the line {(index + 1)}, it's ignored")
            continue            

        shoe = Shoe(country, code, product, cost, quantity)
        shoe_list.append(shoe)

    # allows change is_file_Loaded value outside of its current scope
    global is_file_Loaded
    is_file_Loaded = True

    print("File has been load successfully!")

# this function allows the user to add a new shoe
# and append the new object inside the shoe list
# finally, data is stored in the file
def capture_shoes():
    country = input("Enter the country: ")
    code = input("Enter shoe code: ")
    product = input("Enter shoe product: ")

    while True:
        try:
            cost = float(input("Enter shoe cost: "))
            break
        except ValueError:
            print("You should enter a number for cost!")

    while True:
        try:
            quantity = int(input("Enter shoe quantity: "))
            break
        except ValueError:
            print("You should enter an integer number for quantity!")

    shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(shoe)

    store_shoe_list()

    print("The new shoe has been added successfully!")

# this function shows the details of the shoes
def view_all():
    print_list(shoe_list)

# this function print the list in a friendly manner
def print_list(list):
    if len(shoe_list) == 0:
        print("No shoe in the list")
        return

    print()
    print(tabulate([x.__str__().split(",") for x in list], headers=file_header))
    print()

# this function finds the shoe that have the lowest quantity 
# and asks the user if they want to add quantity or not
# finally, if the quantity is added, the new data is stored in the file
def re_stock():
    if len(shoe_list) == 0:
        print("No shoe in the list")
        return

    lowest_quantity = shoe_list[0].quantity
    lowest_index = 0

    for index, shoe in enumerate(shoe_list):
        if shoe.quantity < lowest_quantity:
            lowest_quantity = shoe.quantity 
            lowest_index = index

    print(f"The lowest quantity shoes is {shoe_list[lowest_index].code} with {lowest_quantity} quantity.")

    while True:
        result = input("Do you want to change quantity of this shoe?[Yes/No] ").lower()

        if result != "yes" and result != "no":
            print("Please select between \'Yes\' and \'No\'")
            continue
        else:
            break

    if result == "yes":
        while True:
            try:
                add_quantity = int(input("How many shoes do you want to add? "))
            except ValueError:
                print("Please enter an integer number")
                continue

            if add_quantity <= 0:
                print("Please enter a positive number!")
                continue
            else:
                break

        quantity = lowest_quantity + add_quantity
        shoe_list[lowest_index].quantity = quantity
        
        store_shoe_list()
        print("The quantity has been updated successfully!")

# this function stores the shoe_list in the file br rewriting it with new data
# at first, it writes the header to first line and after that writes data to the file 
def store_shoe_list():
    with open(FILE_PATH, "w") as inventory_file:
        header = ",".join(file_header)
        inventory_file.write(f"{header}\n")

        for shoe in shoe_list:
            inventory_file.write(f"{shoe}\n")

# this function searches for all shoe from the list by part of code
# it searches for any shoes that its code contains the keyword that user entered
# finally, show all the shoes in a table that have keyword in their code
def search_shoes():
    search_item = input("Enter the item code to search: ").lower()
    found_items = []

    for shoe in shoe_list:
        if shoe.code.lower().find(search_item) > -1:
            found_items.append(shoe)

    if len(found_items) == 0:
        print("Item not found")
    else:
        print_list(found_items)

# this function searches a shoe from the list by whole code
# it searches for a shoe that its code equals to the keyword that user entered
# finally, if find a shoe with this condition returns it otherwise returns None
def search_shoe():
    search_item = input("Enter the item code to search: ").lower()

    for shoe in shoe_list:
        if shoe.code.lower() == search_item:
            return shoe

    return None

# this function calculates the total value for each item
# and then print all the shoes in a table
def value_per_item():
    value_list = []
    for shoe in shoe_list:
        value = shoe.cost * shoe.quantity
        value_list.append([shoe.code, shoe.cost, shoe.quantity, value])

    if len(value_list) == 0:
        print("No shoe in the list")
        return

    print()
    print(tabulate(value_list, headers=["Code", "Cost", "Quantity", "Value"]))
    print()

# this function finds the shoe with the highest quantity and suggests it for sale
def highest_qty():
    if len(shoe_list) == 0:
        print("No shoe in the list")
        return

    highest_quantity = shoe_list[0].quantity
    highest_index = 0

    for index, shoe in enumerate(shoe_list):
        if shoe.quantity > highest_quantity:
            highest_quantity = shoe.quantity
            highest_index = index

    print(f"The highest quantity shoes is {shoe_list[highest_index].code} with {highest_quantity} quantity.")
    print("These shoes are ready for sale.")

#==========Main Menu=============
while True:

    # clear screen before show the menu
    os.system("cls")

    selected_option = input('''Select one of the following Options below:
r  - Read shoes data from file
a  - Add new shoe 
va - View all shoes
re - Re-stock
f  - Find specific shoe
s  - Search shoe
vi - Display Value per item
h  - Highest quantity
e  - Exit
: ''').lower()

    print()

    # check if file is loaded or not
    if (not is_file_Loaded and selected_option != 'e' and selected_option != 'r'):
        print("Please read shoes data from file first!")

    # handel the read shoes data from file option
    elif selected_option == 'r':
        read_shoes_data()

    # handel the add new shoe option
    elif selected_option == 'a':
        capture_shoes()

    # handel the view all shoes option
    elif selected_option == 'va':
        view_all()

    # handel the re-stock option
    elif selected_option == 're':
        re_stock()

    # handel the Find specific shoe option 
    elif selected_option == 'f' :
        found_shoe = search_shoe()

        if found_shoe == None:
            print("No shoe found for this code!")
        else:
            print(f"Country : {found_shoe.country}")
            print(f"Code    : {found_shoe.code}")
            print(f"Product : {found_shoe.product}")
            print(f"Cost    : {found_shoe.cost}")
            print(f"Quantity: {found_shoe.quantity}")
            print()
    
    # handel the search shoes option 
    elif selected_option == 's' :
        search_shoes()

    # handel the display Value per item option 
    elif selected_option == 'vi' :
        value_per_item()

    # handel the highest quantity option
    elif selected_option == 'h' :
        highest_qty()

    # exit the program
    elif selected_option == 'e':
        print('Goodbye!!!')
        exit()

    # otherwise show an error message
    else:
        print("You have made a wrong choice, Please Try again")

    input("Press Enter to back to Main Menu...")
