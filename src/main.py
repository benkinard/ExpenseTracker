import logging
from pathlib import Path
import os
import sys

logging.basicConfig(format="%(asctime)s | %(levelname)s\t| %(module)s.%(funcName)s:%(lineno)d - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)

PROJECT_ROOT_PATH = Path(__file__).parent.parent
try:
    ROOT_PATH_IDX = int(os.getenv('ROOT_PATH_INDEX'))
except ValueError as root_idx_e:
    logging.error(f"<{root_idx_e.__class__.__name__}> {root_idx_e}\n")
    sys.exit(1)
# Insert the path to the project's root directory at the specified index of sys.path
sys.path.insert(ROOT_PATH_IDX, str(PROJECT_ROOT_PATH))

from tracker.resources import MONTHS_NUM_TO_NAME, confirm_proceeding_with_parameters, verify_user_inputs
from tracker.income_expense_tracker import IncomeExpenseTracker, TrackerError
from transaction.transactions import Transactions
from transaction.dao.transaction_dao import FlatFileTransactionDAO


def main(argv: list):
    try:
        month, year = verify_user_inputs(argv)
        confirm_proceeding_with_parameters(MONTHS_NUM_TO_NAME[month], year)
    except ValueError as ve:
        logging.error(f"<{ve.__class__.__name__}> {ve}\n")
        sys.exit(1)
    except KeyboardInterrupt as ki:
        logging.info(f"<{ki.__class__.__name__}> {ki}\n")
        sys.exit(1)

    transactions = Transactions(month, year, FlatFileTransactionDAO(sys.path[ROOT_PATH_IDX]))
    transactions.get_transactions_for_the_period()

    try:
        income_expense_tracker = IncomeExpenseTracker(MONTHS_NUM_TO_NAME[month], year,
                                                      f"{sys.path[ROOT_PATH_IDX]}/Tracker")
        logging.info("Connected to Income & Expense Tracker")
        income_expense_tracker.update_tracker()
    except TrackerError as te:
        logging.error(f"<{te.__class__.__name__}> {te}\n")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main(sys.argv)
    except SystemExit as exit_code:
        sys.exit(exit_code)
    except BaseException as e:
        logging.error(f"<{e.__class__.__name__}> {e}\n")
        sys.exit(2)
