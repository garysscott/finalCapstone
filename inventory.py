from tabulate import tabulate


# ========The beginning of the class==========
class Shoe:
    """This is the Shoe class, and it takes in five separate variables - country, code, product
        cost and quantity.  There are seven methods in this class"""

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

    def change_quantity(self):
        new_quantity = int(input("Please enter the quantity to be purchased: "))
        self.quantity = new_quantity

    def get_country(self):
        return self.country

    def get_code(self):
        return self.code

    def get_product(self):
        return self.product

    def __str__(self):
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}\n"


# =============Shoe list===========
# The shoe_list will hold the data obtained from reading from the inventory.txt .
# The shoe_object_list will be used to store the shoe objects once created.
shoe_list = []
shoe_object_list = []


# ==========Functions outside the class==============

# This function pulls in the information from the text file.
# The information from the text file (inventory.txt) is read and appended into the shoe_list list.
# .strip is used to remove the new lines in the text file and .split separates with a ','.
# In the next stage a for loop is used to iterate through the shoe_list list.
# A temporary variable is used which is then combined to make the object which is appended to the shoe_object_list.
# The final value (quantity) is added as an integer to allow calculations to be performed on it later in the program.

def read_shoes_data():
    try:
        file = open("inventory.txt", "r")
        lines = file.readlines()
        file.close()

        for line in lines:
            strip_lines = line.strip("\n")
            split_lines = strip_lines.split(",")
            shoe_list.append(split_lines)

        for x in range(1, len(shoe_list)):
            temp = shoe_list[x]
            shoe1 = Shoe(temp[0], temp[1], temp[2], temp[3], int(temp[4]))
            shoe_object_list.append(shoe1)

    except FileNotFoundError as error:
        print("\n\t\tThe file does not exist")


# This function will allow the user to enter new stock information.
# User inputs are taken for the country, code, product, cost and quantity.
# Validation is added to ensure only an 8 character code can be added (to match all other entries).
# Code entered forced into upper case to match all other codes in the inventory.
# This is then written to the inventory for storage.
# It is also turned into a Shoe class object and appended to the shoe_object_list.
def capture_shoes():
    country = input("Please enter the country the shoe is from: ")
    while True:
        code = input(f"Please enter the eight character shoe code: ").upper()
        if len(code) == 8:
            break
        else:
            print("The code entered was incorrect - try again")
    product = input("Please enter the product name: ")
    cost = input("Please enter the cost of the shoe: ")
    quantity = input("Please enter the quantity in stock: ")

    file = open("inventory.txt", "a")
    file.write("\n" + country + "," + code + "," + product + "," + cost + "," + quantity)
    file.close()

    shoe_object = country, code, product, cost, quantity
    shoe_object_list.append(shoe_object)


# This function will display all the shoe objects that are in the system.
# Empty lists are populated as the program iterates through the shoe_object_list.
# Methods in the Shoe class are run to obtain the necessary data for the lists.
# Because they are tuples the zip feature is used to combine them into one record to be shown in the table.
# I have used the tabulate module to format the data to ensure it displays in a readable manner.
# I have used the 'double-grid' style in tabulate so the output looks similar to the main title screen.
# Center alignment has been added to the table to further improve readability.

def view_all():
    country = []
    code = []
    product = []
    cost = []
    quantity = []

    for lines in shoe_object_list:
        country.append(lines.get_country())
        code.append(lines.get_code())
        product.append(lines.get_product())
        cost.append(lines.get_cost())
        quantity.append(lines.get_quantity())

    record_titles = zip(country, code, product, cost, quantity)

    print('''
╔══════════════════════════════════════════════════════════════════════╗
║                        CURRENT STOCK LEVELS                          ║     
╚══════════════════════════════════════════════════════════════════════╝       
    ''')
    print(tabulate(record_titles, headers=("Country", "Code", "Product", "Cost", "Quantity"),
                   tablefmt="double_grid", numalign="center", stralign="center"))


# This function finds the shoe with the minimum amount in stock.
# A lambda function is used to find the class object with the lowest quantity.
# Adding min to the lambda function means that the shoe item with the manimum value in quantity will be output.
# I used this website to help with lamda / sorting / finding the maximum value (shorturl.at/DFM47).
# The user is then prompted to decide whether to re-stock or not via a menu.
# If they select yes then the change_quantity() method is run which allows the user to update quantity.
# The class object is then updated.
# The new information is wriiten to the inventory.txt file.
def re_stock():
    lowest_stock_shoe = min(shoe_object_list, key=lambda shoe_type: shoe_type.quantity)
    print(f'''
        ╔══════════════════════════════════════════════════╗
        ║      SHOE WITH THE LOWEST NUMBER OF STOCK        ║
        ╠══════════════════════════════════════════════════╣
             {lowest_stock_shoe}                                                       
        ╚══════════════════════════════════════════════════╝

    ''')

    while True:
        try:
            choice = int(input('''
        ╔══════════════════════════════════════════════════╗
        ║          WOULD YOU LIKE TO RE-STOCK?             ║
        ║   1 ► Yes                                        ║ 
        ║   2 ► No                                         ║    
        ╠══════════════════════════════════════════════════╣
        ║ Enter your choice below:                         ║     
        ╚══════════════════════════════════════════════════╝
        ►►►
        '''))
            if choice == 1:
                lowest_stock_shoe.change_quantity()
                print(f'''
        ╔══════════════════════════════════════════════════╗
        ║                NEW STOCK STATUS                  ║
        ╠══════════════════════════════════════════════════╣
             {lowest_stock_shoe}                                                       
        ╚══════════════════════════════════════════════════╝

    ''')
                print("Here is an updated stock list:\n")
                view_all()

                output = ""
                for x in shoe_object_list:
                    output += (
                        f"{x.get_country()},{x.get_code()},{x.get_product()},{x.get_cost()},{x.get_quantity()}\n")

                file = open("inventory.txt", "w")
                file.write("Country,Code,Product,Cost,Quantity\n")
                file.write(output)
                file.close()
                break

            elif choice == 2:
                break
            else:
                print("\t\tYou can only enter 1 or 2.\n\t\tPlease try again.")


        except ValueError:
            print("\n\t\tYou need to enter either 1 or 2.\n\t\tTry again!")


# This function allows the user to search for a shoe based on a code
# Once the code is entered (must be 8 characters) the program will iterate through the shoe_object_list
# A temporary list is created (new_display) which holds the column headers as the first item
# If it locates the code it will append it to the temporary list and display
# A header has been added to ensure it is as readable as possible (making allowances for the eight character code).
# Input taken for the search code is forced into upper case to match all entries in the inventory.
# A 'Not in Stock' message is displayed if the code is not found in the list.
def search_shoe():
    while True:
        search_code = input("\nPlease enter the code you are searching for: ").upper()
        if len(search_code) == 8:
            for x in shoe_object_list:
                marker = 0
                if x.get_code() == search_code:
                    print(f'''
        ╔══════════════════════════════════════════════════╗
        ║           ITEM {search_code} IN STOCK                 ║     
        ╚══════════════════════════════════════════════════╝       
                        ''')
                    print(f'\t\t\t\t{x}')
                    marker = 1

            if marker != 1:
                print(f'''
        ╔══════════════════════════════════════════════════╗
        ║           ITEM {search_code} IS NOT STOCK             ║     
        ╚══════════════════════════════════════════════════╝       

                            ''')

            break

        else:
            print("\t\tThe code must be 8 characters in length.\n\t\tPlease try again.")


# This function returns the value of each item in stock.
# I have tried to format it in a similar style to the menu and other functions
# As the function iterates through the shoe_object_list it runs the get_cost method from the Shoe class.
# Once the get_cost method is run it is then multiplied by the quantity.
# The quantity is obtained from the Shoe class using the get_quantity method.
def value_per_item():
    print('''
        ╔══════════════════════════════════════════════════╗
        ║                  Value per Item                  ║
        ╠══════════════════════════════════════════════════╣
        ''')
    for x in shoe_object_list:
        value = int(x.get_cost()) * int(x.get_quantity())
        print(f'\t\t  {x.get_code()}  {x.get_product()}  VALUE: R{value}')
        print("\t\t╠══════════════════════════════════════════════════╣")

    print('''
        ╔══════════════════════════════════════════════════╗
        ║                   END OF LIST                    ║   
        ╚══════════════════════════════════════════════════╝
        ''')


# This function iterates through the shoe_object list and locates the item with the highest quantity.
# A lambda function is used to sort the shoe items in the shoe_object_list based on quantity.
# Adding max to the lambda function means that the shoe item with the maximum value in quantity will be output.
# I used this website to help with lamda / sorting / finding the maximum value (shorturl.at/DFM47).
# I have tried to format the output to ensure it matches the main menu and other functions in the program.
def highest_qty():
    highest_stock_shoe = max(shoe_object_list, key=lambda shoe_type: shoe_type.quantity)

    print(f'''
        ╔══════════════════════════════════════════════════╗
        ║      SHOE WITH THE HIGHEST NUMBER OF STOCK       ║
        ╠══════════════════════════════════════════════════╣
              {highest_stock_shoe}                                 
        ╚══════════════════════════════════════════════════╝
            ''')


# ==========Main Menu=============

# The read_shoes_data function is called as soon as the program is run.
read_shoes_data()

# The menu has been formatted in a way that I believe makes it very readable
# The input needs to be an integer - Try/ Except is used to ensure an integer can only be input.
# The integer input determines the function to be run.
# Validation has been added to ensure that only the numbers 1 to 7 can be accepted.
# An option to exit the program has also been added.
while True:
    try:
        menu_choice = int(input('''
        ╔══════════════════════════════════════════════════╗
        ║               SHOE INVENTORY SYSTEM              ║
        ╠══════════════════════════════════════════════════╣
        ║ Select an option from the menu below:            ║     
        ╠══════════════════════════════════════════════════╣
        ║   1 ► View all shoes in stock                    ║ 
        ║   2 ► Search for a shoe using a code             ║ 
        ║   3 ► Add a new shoe                             ║ 
        ║   4 ► View the item with the highest quantity    ║ 
        ║   5 ► View shoes that need to be re-stocked      ║ 
        ║   6 ► View the total value per item              ║
        ║   7 ► Exit the system                            ║
        ╠══════════════════════════════════════════════════╣
        ║ Enter your choice below:                         ║     
        ╚══════════════════════════════════════════════════╝
        ►►► 
        '''))

        if menu_choice == 1:
            view_all()
        elif menu_choice == 2:
            search_shoe()
        elif menu_choice == 3:
            capture_shoes()
        elif menu_choice == 4:
            highest_qty()
        elif menu_choice == 5:
            re_stock()
        elif menu_choice == 6:
            value_per_item()
        elif menu_choice == 7:
            exit()
        else:
            print("\n\t\tYou need to enter a number between 1 and 7.\n\t\tTry again!")

    except ValueError:
        print("\n\t\tYou need to enter a number between 1 and 7.\n\t\tTry again!")
