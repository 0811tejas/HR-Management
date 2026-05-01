def banking():

    print("Hello""\n""What's on your mind?")
    print("Choose from the following menu:""\n""1.Create Account""\n""2.View Account""\n""3.Deposit Money""\n""4.Withdraw Money""\n""5.Delete Account")

    while True:
        try:
            choice=int(input("Enter your choice 1,2,3,4 or 5: "))
            if choice not in [1,2,3,4,5]:
                print("Enter valid choice 1,2,3,4 or 5")
            else:
                break
        except ValueError:
            print("Please enter a number 1,2,3,4 or 5")

    if choice==1:    #create account
        name=input("Enter your name ")
        phn=input("Enter your phone number ")
        deposit_amount=int(input("Enter the deposit amount "))
        acc_no=input("Enter the account number(B__) ")

        import mysql.connector

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bank"
        )

        mycursor = mydb.cursor()
        sql="INSERT INTO bms (name,deposit_amount,phn,acc_no) VALUES (%s,%s,%s,%s)"
        val=(name,deposit_amount,phn,acc_no)

        mycursor.execute(sql,val)
        mydb.commit()
        print("Account created successfully")


    elif choice==2:   #view account
        account_no=input("Enter your account number ")

        import mysql.connector

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bank"
        )

        mycursor = mydb.cursor()
        sql="SELECT * FROM bms WHERE acc_no=%s"
        val=(account_no,)
        mycursor.execute(sql,val)
        myresult=mycursor.fetchone()

        if not myresult:
            print("Account not found")
        else:
            print(myresult)  #since we are using fetchone we can directly print myresult which is a tuple

    elif choice==3:    #deposit money
        acc=input("Enter your account number ")
        amt=int(input("Enter the amount you want to deposit "))

        import mysql.connector
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bank"
        )

        mycursor = mydb.cursor()
        sql="SELECT deposit_amount FROM bms WHERE acc_no= %s"   #fetching current bal of user
        val=(acc,)
        mycursor.execute(sql,val)
        myresult=mycursor.fetchone()   #here we should use fetchone so that we will get only one tuple as output which we can unpack
                                       #if we use fetchall we will get multiple tuples so we cant fetch individual value
        if myresult:   #if we found the users account
            a=myresult[0]
            dep=a+amt    #adding deposit amt to current balance of user

            sql = "UPDATE bms SET deposit_amount=%s WHERE acc_no=%s"
            val = (dep,acc)
            mycursor.execute(sql, val)
            mydb.commit()
            print("Money deposited successfully")

        else:
            print("Account not found")

    elif choice==4:  #Withdraw money
        acc=input("Enter your account number ")
        amt=int(input("Enter the amount you want to withdraw "))

        import mysql.connector
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bank"
        )

        mycursor = mydb.cursor()
        sql = "SELECT deposit_amount FROM bms WHERE acc_no= %s"   #fetching current balance of user
        val = (acc,)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchone()

        if myresult:   #if we found the users account
            a=myresult[0]   #current balance of acc holder
            if a<amt or (a-amt)<1000:  #if amt is less than balance or amount-balance is less than min bal required
                print("Insufficient funds. Minimum balance of 1000rs must be kept")

            else:
                wd=a-amt   #current bal-amt to be withdrawn
                sql="UPDATE bms SET deposit_amount=%s WHERE acc_no=%s"
                val=(wd,acc)
                mycursor.execute(sql,val)
                mydb.commit()
                print("Amount withdrawn successfully")

        else:
            print("Account not found")

    elif choice==5:   #delete account

        acc=input("Enter your account number")
        import mysql.connector
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bank"
        )

        mycursor = mydb.cursor()
        sql="SELECT * FROM bms WHERE acc_no=%s "  #checking if account exits and fetching it
        val=(acc,)
        mycursor.execute(sql,val)
        myresult=mycursor.fetchone()

        if myresult:
            sql="DELETE FROM bms where acc_no=%s"
            val=(acc,)
            mycursor.execute(sql,val)
            mydb.commit()
            print("Account deleted successfully")

        else:
            print("Account not found")


banking()
