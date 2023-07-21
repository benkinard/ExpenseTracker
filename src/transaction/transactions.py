"""Define class to represent transactions that occurred within a specific time period

Classes
-------
Transactions
    Class for storing transactions that occurred within a specific time period
"""
import logging
import pandas as pd
import sys
from datetime import datetime
from tracker.resources import CREDIT_CARD_KEYWORDS, EXPECTED_ERR_NO
from transaction.dao.transaction_dao import TransactionDAO, TransactionDataPullError


class Transactions:
    """Class for storing transactions that occurred within a specific time period

    Instance Variables
    ------------------
    month : int
        Month to pull transactions from
    year : int
        Year to pull from transactions from
    transaction_dao : TransactionDAO
        Object to pull transactions from bank account

    Public Methods
    --------------
    get_as_of_date(self) -> datetime
        Return the date of the most recent transaction
    get_expenses(self) -> pd.DataFrame
        Return the subset of transactions that are expenses
    get_income(self) -> pd.DataFrame
        Return the subset of transactions that are income
    get_num_checking_account_transactions(self) -> int
        Return the number of transactions that came from the checking account
    get_num_credit_card_transactions(self) -> int
        Return the number of transactions that came from the credit card account
    get_transactions_for_the_period(self)
        Pull transactions for the period from bank account
    """
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
        """Return the date of the most recent transaction"""
        return self.__as_of_date

    def get_expenses(self) -> pd.DataFrame:
        """Return the subset of transactions that are expenses"""
        return self.__expenses.copy()

    def get_income(self) -> pd.DataFrame:
        """Return the subset of transactions that are income"""
        return self.__income.copy()

    def get_num_checking_account_transactions(self) -> int:
        """Return the number of transactions that came from the checking account"""
        return len(self.__checking_acct_trx)

    def get_num_credit_card_transactions(self) -> int:
        """Return the number of transactions that came from the credit card account"""
        return len(self.__credit_card_trx)

    def get_transactions_for_the_period(self):
        """Pull transactions for the period from bank account

        Raises
        ------
        SystemExit
            If error is encountered while pulling data
        """
        try:
            self.__checking_acct_trx = self.transaction_dao.pull_checking_account_transactions(self.month, self.year)
            self.__credit_card_trx = self.transaction_dao.pull_credit_card_transactions(self.month, self.year)
            self.__separate_income_from_expenses()
        except TransactionDataPullError as tdpe:
            logging.error(f"<{tdpe.__class__.__name__}> {tdpe}\n")
            sys.exit(EXPECTED_ERR_NO)

    # Private methods
    def __separate_income_from_expenses(self):
        """Split the transaction data for the period up into income transactions and expense transactions

        Raises
        ------
        SystemExit
            If columns of the transaction table do not match expectations
        """
        checking = self.__checking_acct_trx.copy()
        cc = self.__credit_card_trx.copy()
        # Date, Description, and Amount columns are the 2nd, 3rd, and 4th columns respectively
        column_selection = list(checking.columns[1:4])

        try:
            # Withdrawals from checking account are flagged as DEBIT in the Details column (bank's liability to me is
            # being debited)
            checking_expenses = checking.loc[checking['Details'] == 'DEBIT', column_selection]
            # Remove any withdrawals made to pay off credit card, since those expenses are being captured directly from
            # the credit card account
            paying_off_cc_filter = list(map(lambda trx_desc: all(kywd not in trx_desc.upper() for kywd in
                                                                 CREDIT_CARD_KEYWORDS),
                                            checking_expenses['Description']))
            checking_expenses = checking_expenses.loc[paying_off_cc_filter, :]
            checking_expenses.reset_index(drop=True, inplace=True)
            # Expenses in the credit card account are flagged as 'Sale' in the Type column
            cc_expenses = cc.loc[cc['Type'] == 'Sale', ['Posting Date', 'Description', 'Amount']].reset_index(drop=True)
            self.__expenses = pd.concat([checking_expenses, cc_expenses]).sort_values(by=['Posting Date'],
                                                                                      ignore_index=True)

            # Deposits to checking account are flagged as CREDIT in the Details column
            self.__income = checking.loc[checking['Details'] == 'CREDIT', column_selection].reset_index(drop=True)

            # Identify date of latest transaction and save it as the 'As of' date to post in the tracker
            checking_latest_date = checking.iloc[-1, list(checking.columns).index('Posting Date')]
            cc_latest_date = cc.iloc[-1, list(cc.columns).index('Posting Date')]
            self.__as_of_date = checking_latest_date if checking_latest_date > cc_latest_date else cc_latest_date
        except KeyError as ke:
            logging.error(f"<{ke.__class__.__name__}> Column not found in checking or credit card transaction tables: "
                          f"{ke}")
            sys.exit(EXPECTED_ERR_NO)
