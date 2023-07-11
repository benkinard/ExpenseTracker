import pandas as pd
import sys


class Transactions:
    def __init__(self, month: int, year: int):
        self.month: int = month
        self.year: int = year
        self.checking_acct_trx: pd.DataFrame = pd.DataFrame()
        self.credit_card_trx: pd.DataFrame = pd.DataFrame()
        self.income: pd.DataFrame = pd.DataFrame()
        self.expenses: pd.DataFrame = pd.DataFrame()

    # Public methods
    def get_transactions_for_the_period(self):
        pass

    # Private methods
    def __get_checking_account_transactions(self):
        root_path = sys.path[1]
        mm = str(self.month) if self.month >= 10 else f"0{str(self.month)}"
        self.checking_acct_trx = pd.read_csv(f"{root_path}/Tracker/{self.year}/{mm}_Transaction_Data/checking_{mm}.csv",
                                             index_col=False)
