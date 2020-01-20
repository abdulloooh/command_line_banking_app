from time import sleep
id_pwd = {}
id_acc_bal = {}
# user_input = {1:}
def treat_input(inp):
    if inp == "1": create_account()
    elif inp =="2": login()
    elif inp =="3": terminate()
    else:
        print("Request not clear, terminating...") #put delay here later
        sleep(3)
        terminate()

def start():
    # default screen
    start_option = input("""Welcome Dear Customer,
                                            Press 1: create account
                                            Press 2: log in 
                                            press 3: terminate\n>>""")
    treat_input(start_option)

def create_account():
    # regsiter id and pwd
    user_id = input("Enter Your email or any unique identity: \n>>")
    pwd = input("Enter a password: \n>>")
    # if id already exists
    if user_id in id_pwd:
        print("This email/id has been selected or you already create an account")
        # bad_id = "" #get input ot proceed
        # while (bad_id != 1 or bad_id !=2 or bad_id !=3):
        bad_id = input("""Press 1: try another email/Id
                                            2 to: login or
                                            3: terminate\n>>""")
        treat_input(bad_id)
        # bad_id = ""  #re-assign bad_id for next session
    #if id is new
    print("Account creating....")
    sleep(3)
    id_pwd[user_id] = pwd #initialise user
    id_acc_bal[user_id] = 0.0 #initialise acct bal to zero for new user
    print("Account created succesfully")
    print("""
                    Welcome to our platform we hope to serve you best
                    press 1: Create another account
                    press 2: go ahead and login 
                     press 3: terminate""")
    # good_id = "" #get input to proceed
    # while(good_id!=1 or good_id!= 2):
    good_id = input(">>")
    treat_input(good_id)

def login():
    print("Please enter your login details")
    user_id = input("Enter email or Id\n>>")
    pwd= input("Enter password:\n>>")
    if(user_id in id_pwd):
        # print("user dey oo")
        if(id_pwd[user_id] == pwd):
            print("signing in... Please wait")
            sleep(3)
            transaction(user_id)
        else: 
            print("""
                            Wrong password for user
                            Press 1: Create account if you have not
                            Press 2: Re-try login
                            Press 3: Terminate
                            """)
            wrong_pwd = input(">>")
            treat_input(wrong_pwd)
    else:
        print("""
                    User does not exist
                    press 1: create account
                    press 2: Re-try login
                    press 3: Cancel
                    """)
        no_user = input(">>")
        treat_input(no_user)

def transaction(user):
    print("""  
                  press 1: Check Balance
                   Press 2: Deposit
                   Press 3: Withdraw
                   Press 4 Transfer
                   Press 5: Terminate""")
    transact ="" #initalise transact option
    transact = input(">>")
    while(transact !="1" and transact!="2" and transact!= "3" and transact!= "4" and transact!="5"):
        transact = input("Enter correct input>>")
    if(transact == "1"): check_bal(user)
    elif  transact == "2": deposit_or_withdraw(user, 'dep')
    elif transact == "3": deposit_or_withdraw(user, 'withd')
    elif transact == "4": transfer(user)
    elif transact == "5": terminate()
    # else:  it cannot be somethin else,a lraedy handled from the while loop

def check_bal(user):
    print("fetching balance...")
    sleep(3)
    print("Your balance is ", str(id_acc_bal[user]))
    if(input("Press any key to go back: >>") == '0' ) : transaction(user)
    transaction(user)

def deposit_or_withdraw(user,option):  #use one function for deposit and withdrawal, second argument dep/withd determines which of the actions
    if option == 'dep':    print("Enter Amount to deposit")
    elif option == 'withd': print("Enter Amount to withdraw") 
    try:   #ensure only integer comes in
        if option == 'dep': depos = int(input(">>"))  #var depos for deposit amount
        elif option == 'withd': withdraw = int(input(">>"))     #var withdraw for withdrawal amount
    except ValueError:
        print("Integer values only are allowed")
        if option == "dep": deposit_or_withdraw(user, 'dep')
        elif option == "withd": deposit_or_withdraw(user, 'withd')
    except:
        print("Unexpected Input, try again")
        if option == "dep": deposit_or_withdraw(user, 'dep')
        elif option == "withd": deposit_or_withdraw(user, 'withd')
    #top up acct
    if option == 'dep': 
        print("Processing your deposit...")
        sleep(3)
        id_acc_bal[user] = id_acc_bal[user] + depos
    elif option == 'withd': 
        if id_acc_bal[user] - withdraw < 0:  #check if user has enough money to withdraw
            print("You do not have enough balance, kindly make deposit")
            if(input("Press any key to go back: >>") == '0') : transaction(user)   #handle any key later simply
            transaction(user)
        print("Processing your withdrawal...")
        sleep(3)
        id_acc_bal[user] = id_acc_bal[user] - withdraw
    #feedback
    if option =='dep': print(f"{depos} has been deposited into your account and your new balance is {id_acc_bal[user]}")
    elif option == 'withd': print(f"{withdraw} has been withdrawn from your account and your new balance is {id_acc_bal[user]}")
    #return
    if(input("Press any key to go back: >>") == '0') : transaction(user)   #handle any key later simply
    transaction(user)

def transfer(user):    
    try:
        amount = int(input("How much to be transferred?  >>"))
        if id_acc_bal[user] - amount < 0:  #check if user has enough money to transfer
            print("You do not have enough balance to make this amount of transfer")
            print("""
                            press 1:     try small amount of transfer
                            press any other key:      Cancel Transfer
                            """)
            what_next = input(">>")
            if(what_next == 1): transfer(user)
            transaction(user)
    except ValueError:
        print("Integer only expected, try again")
        transfer(user)
    except:
        print("Unexpected input")
        transfer(user)
    #amount resolved, get destination addr
    print("Enter email or Id of the receiver")
    receiver = input(">>")
    #look up user
    while (receiver not in id_pwd or receiver == user):
        if receiver == user: print("There is no point in transferring to your same account, try another")
        else:print("Receiver account not registered")
        print("Enter correct email / Id of the receiver or 4 to cancel transfer")
        receiver = input(">>") 
        if receiver == "4" : transaction(user)
    #top up and deduct
    print("Processing your transfer...")
    sleep(3)
    id_acc_bal[user] -= amount
    id_acc_bal[receiver] += amount
    #feedback
    print(f"{amount} has been transferred from {user} to {receiver}'s account'")
    #return
    if(input("Press any key to go back: >>") == '0' ) : transaction(user)
    transaction(user)
    
def terminate():
    print("terminating...")
    sleep(3)
    print("Thanks for banking with us, Good Bye")
    # Introduce delay later here
    start()
    
start()