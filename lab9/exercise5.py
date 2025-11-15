class BankAccount:
    def __init__(self, owner: str):
        self.owner = owner
        self.balance = 0.0
        self.movements = []
    
    def deposit(self, amount, concept: str):
        if not isinstance(amount, (int, float)):
            raise TypeError("Deposit amount must be a number.")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.__movement("Income    ", concept, amount, self.balance)

    def withdraw(self, amount, concept: str):
        if not isinstance(amount, (int, float)):
            raise TypeError("Withdrawal amount must be a number.")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Not enough balance to execute the operation.")
        self.balance -= amount
        self.__movement("Withdrawal", concept, -amount, self.balance)

    def __movement(self, type, concept, amount, balance):
        if concept is None:
            concept = "No concept"
        
        movement = {"type": type, "concept": concept, "amount": amount, "balance": balance}
        self.movements.append(movement)

    def __print_movements(self):
        output = ""
        last_movements = self.movements[-10:]
        for each in range(len(last_movements) - 1, -1, -1):
            mov = last_movements[each]
            output += f"{mov['type']:<10} | {mov['concept']:<10} | {mov['amount']:>8.1f} | {mov['balance']:>8.1f}\n"
        return output

    def __str__(self):
        movements_output = self.__print_movements()
        return (
            "Account information:\n"
            f"Owner: {self.owner}\n"
            f"Balance: {self.balance}\n"
            "Latest movements:\n"
            "   Type    | Concept    | Amount   | Balance\n"
        ) + movements_output
    
bank = BankAccount("Federico Fernandez")
bank.deposit(1000.50, "Deposit")
bank.withdraw(50.00, "Cash")
bank.deposit(250.00, None) 
bank.withdraw(1200.00, "Transfer")

print(bank)