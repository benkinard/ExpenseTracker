"""Define classes for accessing bank account transaction data

Classes
-------
TransactionDataPullError
    Class for exceptions that occur while attempting to pull transaction data from bank accounts
TransactionDAO
    Abstract Base Class for pulling transaction data from bank accounts
FlatFileTransactionDAO
    Concrete Class for pulling bank account transaction data from flat files
APITransactionDAO
    Concrete Class for pulling bank account transaction data using bank's API
"""
import pandas as pd
from abc import ABC, abstractmethod


class TransactionDataPullError(Exception):
    pass


class TransactionDAO(ABC):
    """Abstract Base Class for pulling transaction data from bank accounts

    Methods
    -------
    pull_checking_account_transactions(month: int, year: int) -> pd.DataFrame
        Pull transaction data from checking account
    pull_credit_card_transactions(month: int, year: int) -> pd.DataFrame
        Pull transaction data from credit card account
    """
    @abstractmethod
    def pull_checking_account_transactions(self, month: int, year: int) -> pd.DataFrame:
        """Pull transaction data from checking account

        Parameters
        ----------
        month : int
            Month to pull checking account transaction data from
        year : int
            Year to pull checking account transaction data from

        Returns
        -------
        pd.DataFrame
            Checking account transaction data
        """
        pass

    @abstractmethod
    def pull_credit_card_transactions(self, month: int, year: int) -> pd.DataFrame:
        """Pull transaction data from credit card account

        Parameters
        ----------
        month : int
            Month to pull credit card account transaction data from
        year : int
            Year to pull credit card account transaction data from

        Returns
        -------
        pd.DataFrame
            Credit card account transaction data
        """
        pass


class FlatFileTransactionDAO(TransactionDAO):
    """Concrete Implementation of TransactionDAO class for pulling bank account transaction data from flat files

    Instance Variables
    ------------------
    tracker_root_path : str
        File path to root directory containing transaction data flat files
    """
    def __init__(self, tracker_root_path: str):
        """Constructor for FlatFileTransactionDAO class

        Parameters
        ----------
        tracker_root_path : str
            File path to root directory containing transaction data flat files
        """
        super().__init__()
        self.tracker_root_path: str = tracker_root_path

    # Public methods
    def pull_checking_account_transactions(self, month: int, year: int) -> pd.DataFrame:
        """Pull transaction data from checking account

        Parameters
        ----------
        month : int
            Month to pull checking account transaction data from
        year : int
            Year to pull checking account transaction data from

        Returns
        -------
        pd.DataFrame
            Checking account transaction data

        Raises
        ------
        FileNotFoundError
            If path to checking account transaction data flat files does not exist
        KeyError
            If expected column of checking account transaction data is not present
        DateParseError
            If Posting Date column contains an unexpected value
        ValueError
            If Balance column contains an unexpected value
        """
        mm = self.__format_month(month)
        try:
            checking_acct_trx = pd.read_csv(f"{self.tracker_root_path}/{year}/{mm}_Transaction_Data/checking_{mm}.csv",
                                            index_col=False)
            checking_acct_trx['Balance'] = pd.to_numeric(checking_acct_trx['Balance'], errors='coerce')
            checking_acct_trx['Posting Date'] = pd.to_datetime(checking_acct_trx['Posting Date'])
        except FileNotFoundError as fnfe:
            raise TransactionDataPullError(f"Unable to pull checking account transactions. {fnfe}")
        except KeyError as ke:
            raise TransactionDataPullError(f"Column not found in pulled checking account transaction data: {ke}")
        except pd._libs.tslibs.parsing.DateParseError as dpe:
            raise TransactionDataPullError(f"Unexpected value in checking account transaction \"Posting Date\" field. "
                                           f"{dpe}")
        except ValueError as ve:
            raise TransactionDataPullError(f"Unexpected value in checking account transaction \"Balance\" field. {ve}")

        return checking_acct_trx.sort_values(by=['Posting Date'], ignore_index=True)

    def pull_credit_card_transactions(self, month: int, year: int) -> pd.DataFrame:
        """Pull transaction data from credit card account

        Parameters
        ----------
        month : int
            Month to pull credit card account transaction data from
        year : int
            Year to pull credit card account transaction data from

        Returns
        -------
        pd.DataFrame
            Credit card account transaction data

        Raises
        ------
        FileNotFoundError
            If path to credit card transaction data flat files does not exist
        KeyError
            If expected column of credit card transaction data is not present
        ValueError
            If Transaction or Posting Date columns contain an unexpected value
        """
        mm = self.__format_month(month)
        try:
            credit_card_trx = pd.read_csv(f"{self.tracker_root_path}/{year}/{mm}_Transaction_Data/credit_card_{mm}.csv",
                                          index_col=False)
            credit_card_trx.rename(columns={'Post Date': 'Posting Date'}, inplace=True)
            credit_card_trx['Transaction Date'] = pd.to_datetime(credit_card_trx['Transaction Date'])
            credit_card_trx['Posting Date'] = pd.to_datetime(credit_card_trx['Posting Date'])
        except FileNotFoundError as fnfe:
            raise TransactionDataPullError(f"Unable to pull credit card transactions. {fnfe}")
        except KeyError as ke:
            raise TransactionDataPullError(f"Column not found in pulled credit card transaction data: {ke}")
        except ValueError as ve:
            raise TransactionDataPullError(f"Unexpected value in \"Transaction/Posting Date\" field. {ve}")

        return credit_card_trx.sort_values(by=['Posting Date'], ignore_index=True)

    # Private methods
    @staticmethod
    def __format_month(month: int) -> str:
        """Convert integer representation of month to two-digit code (mm)

        Parameters
        ----------
        month : int
            Number representing a month of the year

        Returns
        -------
        str
            Two digit code for the month passed in (01-12)
        """
        return str(month) if month >= 10 else f"0{str(month)}"


class APITransactionDAO(TransactionDAO):
    """
    Concrete Implementation of TransactionDAO class for pulling bank account transaction data using bank's provided
    API

    Instance Variables
    ------------------
    account_ids : list[int]
        IDs of bank accounts to pull transaction data from
    """
    # TODO: Implement when/if bank grants API access to individuals for personal use
    def __init__(self, account_ids: list[int]):
        """Constructor for APITransactionDAO class

        Parameters
        ----------
        account_ids : list[int]
            IDs of bank accounts to pull transaction data from
        """
        super().__init__()
        self.account_ids: list[int] = account_ids

    def pull_checking_account_transactions(self, month: int, year: int) -> pd.DataFrame:
        pass

    def pull_credit_card_transactions(self, month: int, year: int) -> pd.DataFrame:
        pass
