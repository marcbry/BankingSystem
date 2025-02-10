import json

class OnlineBankingSystem:
    def __init__(self):
        self.customers = self.load_data("customers.json")
        self.transactions = self.load_data("transactions.json")
        self.admin_password = "admin123"

    def load_data(self, filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_data(self, filename, data):
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def create_account(self):
        customer_id = input("Enter Customer ID: ")
        if customer_id in self.customers:
            print("Customer ID already exists!")
            return
        name = input("Enter Name: ")
        email = input("Enter Email: ")
        number = input("Enter Phone Number: ")
        password = input("Set a Password: ")
        self.customers[customer_id] = {"name": name, "email": email, "number": number, "password": password, "balance": 0.0}
        self.save_data("customers.json", self.customers)
        print("Account created successfully!")

    def sign_in(self):
        customer_id = input("Enter Customer ID: ")
        password = input("Enter Password: ")
        if customer_id in self.customers and self.customers[customer_id]["password"] == password:
            print("Login successful!")
            self.customer_menu(customer_id)
        else:
            print("Invalid credentials!")

    def customer_menu(self, customer_id):
        while True:
            print("\n1. Deposit\n2. Withdraw\n3. View Transactions\n4. Logout")
            choice = input("Enter choice: ")
            if choice == "1":
                self.deposit(customer_id)
            elif choice == "2":
                self.withdraw(customer_id)
            elif choice == "3":
                self.view_transactions(customer_id)
            elif choice == "4":
                print("Logging out...")
                break
            else:
                print("Invalid choice!")

    def deposit(self, customer_id):
        amount = float(input("Enter amount to deposit: "))
        self.customers[customer_id]["balance"] += amount
        self.record_transaction(customer_id, "Deposit", amount)
        self.save_data("customers.json", self.customers)
        print("Deposit successful!")

    def withdraw(self, customer_id):
        amount = float(input("Enter amount to withdraw: "))
        if self.customers[customer_id]["balance"] >= amount:
            self.customers[customer_id]["balance"] -= amount
            self.record_transaction(customer_id, "Withdraw", amount)
            self.save_data("customers.json", self.customers)
            print("Withdrawal successful!")
        else:
            print("Insufficient balance!")

    def record_transaction(self, customer_id, transaction_type, amount):
        if customer_id not in self.transactions:
            self.transactions[customer_id] = []
        self.transactions[customer_id].append({"type": transaction_type, "amount": amount})
        self.save_data("transactions.json", self.transactions)

    def view_transactions(self, customer_id):
        if customer_id in self.transactions:
            for tx in self.transactions[customer_id]:
                print(f"{tx['type']}: {tx['amount']}")
        else:
            print("No transactions found.")

    def admin_login(self):
        password = input("Enter Admin Password: ")
        if password == self.admin_password:
            print("Admin login successful!")
            self.admin_menu()
        else:
            print("Incorrect password!")

    def admin_menu(self):
        while True:
            print("\n1. View All Customers\n2. View All Transactions\n3. Logout")
            choice = input("Enter choice: ")
            if choice == "1":
                self.view_all_customers()
            elif choice == "2":
                self.view_all_transactions()
            elif choice == "3":
                print("Logging out...")
                break
            else:
                print("Invalid choice!")

    def view_all_customers(self):
        for cid, info in self.customers.items():
            print(f"ID: {cid}, Name: {info['name']}, Email: {info['email']}, Phone: {info['number']}, Balance: {info['balance']}")

    def view_all_transactions(self):
        for cid, tx_list in self.transactions.items():
            print(f"Customer ID: {cid}")
            for tx in tx_list:
                print(f"  {tx['type']}: {tx['amount']}")

if __name__ == "__main__":
    bank = OnlineBankingSystem()
    while True:
        print("\n1. Create Account\n2. Sign In\n3. Admin Login\n4. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            bank.create_account()
        elif choice == "2":
            bank.sign_in()
        elif choice == "3":
            bank.admin_login()
        elif choice == "4":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice!")
