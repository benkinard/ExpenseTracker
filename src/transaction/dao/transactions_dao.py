from abc import ABC, abstractmethod
import pandas as pd


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

    def pull_checking_account_transactions(self, month: int, year: int) -> pd.DataFrame:
        mm = str(month) if month >= 10 else f"0{str(month)}"
        checking_acct_trx = pd.read_csv(f"{self.root_path}/Tracker/{year}/{mm}_Transaction_Data/checking_{mm}.csv",
                                        index_col=False)
        checking_acct_trx['Balance'] = pd.to_numeric(checking_acct_trx['Balance'], errors='coerce')
        checking_acct_trx['Posting Date'] = pd.to_datetime(checking_acct_trx['Posting Date'])
        return checking_acct_trx.sort_values(by=['Posting Date'], ignore_index=True)

    def pull_credit_card_transactions(self, month: int, year: int) -> pd.DataFrame:
        mm = str(month) if month >= 10 else f"0{str(month)}"
        credit_card_trx = pd.read_csv(f"{self.root_path}/Tracker/{year}/{mm}_Transaction_Data/credit_card_{mm}.csv",
                                      index_col=False)
        credit_card_trx.rename(columns={'Post Date': 'Posting Date'}, inplace=True)
        credit_card_trx['Transaction Date'] = pd.to_datetime(credit_card_trx['Transaction Date'])
        credit_card_trx['Posting Date'] = pd.to_datetime(credit_card_trx['Posting Date'])
        return credit_card_trx.sort_values(by=['Posting Date'], ignore_index=True)


class APITransactionDAO(TransactionDAO):
    # TODO: Implement when/if bank grants API access to individuals for personal use
    def __init__(self, account_id: int):
        super().__init__()
        self.account_id: int = account_id

    def pull_checking_account_transactions(self, month: int, year: int) -> pd.DataFrame:
        pass

    def pull_credit_card_transactions(self, month: int, year: int) -> pd.DataFrame:
        pass
