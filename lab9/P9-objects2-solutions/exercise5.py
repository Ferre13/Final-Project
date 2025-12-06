from bank_account import BankAccount

account = BankAccount("Pepe")
account.deposit(500, "Pay")
account.deposit(350.30)
account.withdraw(200.40, "Insurance")
print(account)
