from pathlib import Path
import logging
import sys

logging.basicConfig(format="%(asctime)s | %(levelname)s\t| %(module)s.%(funcName)s:%(lineno)d - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)
main_parent_path = Path(__file__).parent
sys.path.insert(1, str(main_parent_path.parent))

from tracker.resources import MONTHS_NUM_TO_NAME, confirm_proceeding_with_parameters, verify_user_inputs
from transaction.transactions import Transactions
from transaction.dao.transaction_dao import FlatFileTransactionDAO


def main(argv: list):
    try:
        month, year = verify_user_inputs(argv)
        confirm_proceeding_with_parameters(MONTHS_NUM_TO_NAME[month], year)
        transactions = Transactions(month, year, FlatFileTransactionDAO(sys.path[1]))
        transactions.get_transactions_for_the_period()
        print(f"# Checking Account Transactions: {transactions.get_num_checking_account_transactions()}",
              f"# Credit Card Transactions: {transactions.get_num_credit_card_transactions()}",
              f"# Income Transactions: {len(transactions.get_income())}",
              f"# Expense Transactions: {len(transactions.get_expenses())}", sep="\n*****\n")
    except ValueError as ve:
        logging.error(f"<{ve.__class__.__name__}> {ve}\n")
        sys.exit(1)
    except KeyboardInterrupt as ki:
        logging.info(f"<{ki.__class__.__name__}> {ki}\n")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main(sys.argv)
    except SystemExit as exit_code:
        sys.exit(exit_code)
    except BaseException as e:
        logging.error(f"<{e.__class__.__name__}> {e}\n")
        sys.exit(2)
