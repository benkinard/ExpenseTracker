from transaction.dao.transaction_dao import TransactionDAO, TransactionDataPullError
from tracker.resources import CREDIT_CARD_KEYWORDS
from datetime import datetime
import logging
import pandas as pd
import sys


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
        self.__as_of_date: datetime = datetime.now()

    # Public methods
    def get_as_of_date(self) -> datetime:
        return self.__as_of_date

    def get_expenses(self) -> pd.DataFrame:
        return self.__expenses.copy()

    def get_income(self) -> pd.DataFrame:
        return self.__income.copy()

    def get_num_checking_account_transactions(self) -> int:
        return len(self.__checking_acct_trx)

    def get_num_credit_card_transactions(self) -> int:
        return len(self.__credit_card_trx)

    def get_transactions_for_the_period(self):
        try:
            self.__checking_acct_trx = self.transaction_dao.pull_checking_account_transactions(self.month, self.year)
            self.__credit_card_trx = self.transaction_dao.pull_credit_card_transactions(self.month, self.year)
            self.__filter_income_from_expenses()
        except TransactionDataPullError as tdpe:
            logging.error(f"<{tdpe.__class__.__name__}> {tdpe}\n")
            sys.exit(1)

    # Private methods
    def __filter_income_from_expenses(self):
        checking = self.__checking_acct_trx.copy()
        cc = self.__credit_card_trx.copy()
        column_selection = list(checking.columns[1:4])

        try:
            checking_expenses = checking.loc[checking['Details'] == 'DEBIT', column_selection]
            paying_off_cc_filter = list(map(lambda trx_desc: all(kywd not in trx_desc.upper() for kywd in
                                                                 CREDIT_CARD_KEYWORDS),
                                            checking_expenses['Description']))
            checking_expenses = checking_expenses.loc[paying_off_cc_filter, :]
            checking_expenses.reset_index(drop=True, inplace=True)
            cc_expenses = cc.loc[cc['Type'] == 'Sale', ['Posting Date', 'Description', 'Amount']].reset_index(drop=True)
            self.__expenses = pd.concat([checking_expenses, cc_expenses]).sort_values(by=['Posting Date'],
                                                                                      ignore_index=True)

            self.__income = checking.loc[checking['Details'] == 'CREDIT', column_selection].reset_index(drop=True)

            checking_latest_date = checking.iloc[-1, list(checking.columns).index('Posting Date')]
            cc_latest_date = cc.iloc[-1, list(cc.columns).index('Posting Date')]
            self.__as_of_date = checking_latest_date if checking_latest_date > cc_latest_date else cc_latest_date
        except KeyError as ke:
            logging.error(f"<{ke.__class__.__name__}> Column not found in checking or credit card transaction tables: "
                          f"{ke}")
            sys.exit(1)
