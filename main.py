import json

def add_expenses(expenses):
    name = input("Enter Expense name : ")
    try:
        amt = int(input("Enter amount for expense : "))
    except:
        print("Invalid! Please enter amount in numbers")
        return

    category = input("Enter category of Expense : ")
    expenses.append({"name": name, "amt": amt, "category": category})
    save_exp(expenses)


def display(expenses):
    if not expenses:
        print("No Expenses added yet")
    else:
        print(f"{'Name':<15}\t{'Amount':<10}\t{'Category':<10}")
        for i in expenses:
            print(f"{i['name']:<15}\t{i['amt']:<10}\t{i['category']:<10}")


def total_exp(expenses):
    if not expenses:
        print("No Expenses added yet")
        print("Your Total expenses : 0")
    else:
        total = sum(i['amt'] for i in expenses)
        print("Your Total expenses : ", total)


def filter_category(expenses):
    val = input("Enter category name : ")
    found = False

    print(f"{'Name':<15}\t{'Amount':<10}\t{'Category':<10}")
    for i in expenses:
        if i["category"].lower() == val.lower():
            print(f"{i['name']:<15}\t{i['amt']:<10}\t{i['category']:<10}")
            found = True

    if not found:
        print("No such category found")


def del_exp(expenses):
    val = input("Enter expense name to delete : ")

    orig_len = len(expenses)

    found = False
    expenses[:] = [i for i in expenses if i["name"].lower() != val.lower()]

    if len(expenses)<orig_len:
        print(val, "deleted")
    else:
        print(val, "doesn't exist")
    
    save_exp(expenses)


def edit_exp(expenses):
    val = input("Enter Expense name : ")
    try:
        amt = int(input("Enter amount to edit : "))
    except:
        print("Invalid! Enter amount in number")
        return

    found = False

    for i in expenses:
        if i["name"].lower() == val.lower():
            i["amt"] = amt
            found = True
            break

    if found:
        print(val, "amount updated successfully")
    else:
        print(val, "not found")

    save_exp(expenses)

def save_exp(expenses):
    with open("expenses.json","w") as f:
        json.dump(expenses,f,indent=4)

def load_exp():
    try:
        with open("expenses.json","r") as f:
            return json.load(f)
    except:
        return []


expenses = load_exp()

while True:

    print("\n\n1. Add Expense")
    print("2. Show Expense")
    print("3. Show sum of expenses")
    print("4. Filter expenses by category")
    print("5. Delete expense by Name")
    print("6. Edit expense by Name")
    print("7. Exit")
    try:
        choice = int(input("Enter serial no. of your choice : "))
    except:
        print("Invalid! Please enter number")
        continue

    match choice:
        case 1:
            add_expenses(expenses)

        case 2:
            display(expenses)

        case 3:
            total_exp(expenses)

        case 4:
            filter_category(expenses)

        case 5:
            del_exp(expenses)

        case 6:
            edit_exp(expenses)

        case 7:
            print("Bye")
            break

        case _:
            print("Invalid serial no choice")
