from abc import ABC, abstractmethod
import pandas as pd


class TransactionDataPullError(Exception):
    pass


class TransactionDAO(ABC):
    @abstractmethod
    def pull_checking_account_transactions(self, month: int, year: int) -> pd.DataFrame:
        pass

    @abstractmethod
    def pull_credit_card_transactions(self, month: int, year: int) -> pd.DataFrame:
        pass


class FlatFileTransactionDAO(TransactionDAO):
    def __init__(self, root_path: str):
        super().__init__()
        self.root_path: str = root_path

    # Public methods
    def pull_checking_account_transactions(self, month: int, year: int) -> pd.DataFrame:
        mm = self.__format_month(month)
        try:
            checking_acct_trx = pd.read_csv(f"{self.root_path}/Tracker/{year}/{mm}_Transaction_Data/checking_{mm}.csv",
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
        mm = self.__format_month(month)
        try:
            credit_card_trx = pd.read_csv(f"{self.root_path}/Tracker/{year}/{mm}_Transaction_Data/credit_card_{mm}.csv",
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
        return str(month) if month >= 10 else f"0{str(month)}"


class APITransactionDAO(TransactionDAO):
    # TODO: Implement when/if bank grants API access to individuals for personal use
    def __init__(self, account_id: int):
        super().__init__()
        self.account_id: int = account_id

    def pull_checking_account_transactions(self, month: int, year: int) -> pd.DataFrame:
        pass

    def pull_credit_card_transactions(self, month: int, year: int) -> pd.DataFrame:
        pass
