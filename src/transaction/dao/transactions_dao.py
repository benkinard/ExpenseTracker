from abc import ABC, abstractmethod


class TransactionDAO(ABC):
    @staticmethod
    @abstractmethod
    def pull_checking_account_transactions():
        pass

    @staticmethod
    @abstractmethod
    def pull_credit_card_transactions():
        pass
