class BankAccount:
    def __init__(self, owner: str):
        self.owner = owner
        self.__balance = 0.0
        self.__movements: list[str] = []

    @property
    def balance(self) -> float:
        return self.__balance

    # -----------------------------
    # Internal helpers
    # -----------------------------
    def __format_movement(self, mtype: str, concept: str, amount: float, bal: float) -> str:
        row = "{:^10}|{:^20}|{:>10}|{:>10}"
        return row.format(mtype, concept[:20], f"{amount:.2f}", f"{bal:.2f}")

    def __last_movements(self) -> str:
        header_row = "{:^10}|{:^20}|{:^10}|{:^10}"
        text = (
            "Latest movements:\n"
            + header_row.format("Type", "Concept", "Amount", "Balance")
            + "\n"
        )
        max_mov = min(10, len(self.__movements))
        for i in range(max_mov):
            text += self.__movements[i] + "\n"
        return text

    # -----------------------------
    # Public API
    # -----------------------------
    def deposit(self, amount, concept: str = "No Concept"):
        if not isinstance(amount, (int, float)):
            raise TypeError("Deposit amount must be numeric")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.__balance += float(amount)
        self.__movements.insert(
            0,
            self.__format_movement("Income", concept, float(amount), self.balance),
        )

    def withdraw(self, amount, concept: str = "No Concept"):
        if not isinstance(amount, (int, float)):
            raise TypeError("Withdrawal amount must be numeric")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.balance < float(amount):
            raise ValueError("Insufficient balance")
        self.__balance -= float(amount)
        self.__movements.insert(
            0,
            self.__format_movement("Withdrawal", concept, -float(amount), self.balance),
        )

    # -----------------------------
    # String representation
    # -----------------------------
    def __str__(self) -> str:
        return (
            "Account Information:\n"
            f"Owner: {self.owner}\n"
            f"Balance: €{self.balance:.2f}\n"
            + self.__last_movements()
        )
