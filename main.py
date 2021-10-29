import random
import sqlite3


def print_menu():
    print("""1. Create an account
2. Log into account
0. Exit""")


def print_menu2():
    print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")


def create_account():
    login_exist = False
    while login_exist == False:
        login = "400000" + str(random.randint(100000000, 999999999))
        login2 = login
        sum = 0
        sum2 = 0
        login2 = [int(x) for x in login2]
        for x in range(15):
            if x % 2 == 0:
                login2[x] *= 2
                if login2[x] > 9:
                    login2[x] -= 9
                else:
                    pass
            else:
                pass
            sum += login2[x]

        while sum % 10 != 0:
            sum += 1
            sum2 += 1

        login = login + str(sum2)

        sql_select_query = """select * from card where number = ?"""
        cur.execute(sql_select_query, (login,))
        records = cur.fetchall()
        if records != []:
            login_exist = False
        else:
            login_exist = True
    pin = str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9)) + str(random.randint(0, 9))
    # balance = 0
    sqlite_insert_with_param = """INSERT INTO card
                              (number, pin) 
                              VALUES (?, ?);"""
    data_tuple = (login, pin)
    cur.execute(sqlite_insert_with_param, data_tuple)
    conn.commit()

    print("Your card has been created")
    print("Your card number:")
    print(login)
    print("Your card PIN:")
    print(pin)


def log_in_to_account():
    print("Enter your card number:")
    login = str(input())
    print("Enter your PIN:")
    pin = str(input())

    sql_select_query = """select pin from card where number = ?"""
    cur.execute(sql_select_query, (login,))
    records = cur.fetchall()

    if records != []:
        if pin == records[0][0]:
            print("You have successfully logged in!")
            message = manage_account(login)
            if message == 1:
                print("You have successfully logged out!")
                return True
            elif message == 2:
                return True
            elif message == 0:
                return False
            else:
                pass
        else:
            print("Wrong card number or PIN!")
            return True
    else:
        print("Wrong card number or PIN!")
        return True


def manage_account(login):
    picked_option = None
    while picked_option != 5:
        print_menu2()
        picked_option = int(input())
        if picked_option == 1:

            sql_select_query = """select balance from card where number = ?"""
            cur.execute(sql_select_query, (login,))
            records = cur.fetchall()

            print("Balance: ", records[0][0])
        elif picked_option == 0:
            return 0
        elif picked_option == 2:
            print("Enter income:")
            income_added = int(input())
            cur.execute(f'SELECT balance FROM card WHERE number = {login};')
            actual_balance = cur.fetchone()[0]
            actual_balance += income_added
            cur.execute(f'UPDATE card set balance ={actual_balance} WHERE number = {login};')
            conn.commit()
            print("Income was added!")
        elif picked_option == 3:
            cur.execute(f'SELECT balance FROM card WHERE number = {login};')
            actual_balance = cur.fetchone()[0]
            print("Transfer\nEnter card number:")
            account_number = input()
            if account_number == login:
                print("You can't transfer money to the same account!")
                continue
            sum = 0
            sum2 = 0
            account_number_2 = str(int(int(account_number) / 10))
            account_number_2 = [int(x) for x in account_number_2]
            for x in range(15):
                if x % 2 == 0:
                    account_number_2[x] *= 2
                    if account_number_2[x] > 9:
                        account_number_2[x] -= 9
                    else:
                        pass
                else:
                    pass
                sum += account_number_2[x]

            while sum % 10 != 0:
                sum += 1
                sum2 += 1

            if int(int(account_number) % 10) != sum2:
                print("Probably you made a mistake in the card number. Please try again!")
                continue
            cur.execute(f'SELECT * FROM card WHERE number = {account_number};')
            returned_rows = cur.fetchone()
            if returned_rows == None:
                print("Such a card does not exist.")
                continue
            print("Enter how much money you want to transfer:")
            money_to_transfer = int(input())
            if money_to_transfer > actual_balance:
                print("Not enough money!")
                continue
            cur.execute(f'SELECT balance FROM card WHERE number = {login};')
            actual_balance = cur.fetchone()[0]
            actual_balance -= money_to_transfer
            cur.execute(f'SELECT balance FROM card WHERE number = {account_number};')
            actual_balance_2 = cur.fetchone()[0]
            actual_balance_2 += money_to_transfer
            cur.execute(f'UPDATE card set balance ={actual_balance} WHERE number = {login};')
            cur.execute(f'UPDATE card set balance ={actual_balance_2} WHERE number = {account_number};')
            conn.commit()
        elif picked_option == 4:
            cur.execute(f'DELETE FROM card WHERE number = {login}')
            conn.commit()
            print("The account has been closed!")
            return 2
        else:
            pass
    return 1


conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS card")
cur.execute("CREATE TABLE card (id INTEGER primary key, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)")

selected_option = None

while selected_option != 0:
    print_menu()
    selected_option = int(input())
    if selected_option == 1:
        create_account()
    elif selected_option == 2:
        message = log_in_to_account()
        if not message:
            break
        else:
            pass
    else:
        pass
print("Bye!")
