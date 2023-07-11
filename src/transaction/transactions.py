from dao.transaction_dao import TransactionDAO
from resources import CREDIT_CARD_KEYWORDS
import pandas as pd


class Transactions:
    def __init__(self, month: int, year: int, transaction_dao: TransactionDAO):
        # Public instance variables
        self.month: int = month
        self.year: int = year
        self.transaction_dao: TransactionDAO = transaction_dao
        # Private instance variables
        self.__checking_acct_trx: pd.DataFrame = pd.DataFrame()
        self.__credit_card_trx: pd.DataFrame = pd.DataFrame()
        self.__income: pd.DataFrame = pd.DataFrame()
        self.__expenses: pd.DataFrame = pd.DataFrame()

    # Public methods
    def get_expenses(self) -> pd.DataFrame:
        return self.__expenses.copy()

    def get_income(self) -> pd.DataFrame:
        return self.__income.copy()

    def get_num_checking_account_transactions(self) -> int:
        return len(self.__checking_acct_trx)

    def get_num_credit_card_transactions(self) -> int:
        return len(self.__credit_card_trx)

    def get_transactions_for_the_period(self):
        self.__checking_acct_trx = self.transaction_dao.pull_checking_account_transactions(self.month, self.year)
        self.__credit_card_trx = self.transaction_dao.pull_credit_card_transactions(self.month, self.year)
        self.__filter_income_from_expenses()

    # Private methods
    def __filter_income_from_expenses(self):
        checking = self.__checking_acct_trx.copy()
        cc = self.__credit_card_trx.copy()

        checking_expenses = checking.loc[checking['Details'] == 'DEBIT', list(checking.columns[1:4])]
        checking_expenses = checking_expenses.loc[list(map(lambda trx_desc: all(kywd not in trx_desc for kywd in
                                                                                CREDIT_CARD_KEYWORDS),
                                                           checking_expenses['Description'])), :].reset_index(drop=True)
        cc_expenses = cc.loc[cc['Type'] == 'Sale', ['Posting Date', 'Description', 'Amount']].reset_index(drop=True)
        self.__expenses = pd.concat([checking_expenses, cc_expenses]).sort_values(by=['Posting Date'],
                                                                                  ignore_index=True)

        self.__income = checking.loc[checking['Details'] == 'CREDIT',
                                     list(checking.columns[1:4])].reset_index(drop=True)
