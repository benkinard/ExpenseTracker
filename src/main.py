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

from tracker.resources import MONTHS_NUM_TO_NAME, PRIMARY_INCOME_KEYWORDS, RENT_UTIL_KEYWORDS, GROCERY_KEYWORDS, \
    GAS_KEYWORDS, FIXED_EXPENSE_KEYWORDS, confirm_proceeding_with_parameters, verify_user_inputs
from tracker.income_expense_tracker import IncomeExpenseTracker
from tracker.exceptions import TrackerError


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

    logging.info(f"Connecting to {MONTHS_NUM_TO_NAME[month]} {year} Income & Expense Tracker...")
    try:
        income_expense_tracker = IncomeExpenseTracker(MONTHS_NUM_TO_NAME[month], month, year,
                                                      f"{sys.path[ROOT_PATH_IDX]}/Tracker")
    except TrackerError as conn_error:
        logging.error(f"<{conn_error.__class__.__name__}> {conn_error}\n")
        sys.exit(1)
    logging.info("Connection Successful")

    try:
        income_expense_tracker.add_section("Primary Income", PRIMARY_INCOME_KEYWORDS, min_row=7, max_row=8, min_col=2,
                                           max_col=8, trx_type="income")
        logging.info("Added Primary Income Section")

        income_expense_tracker.add_section("Other Income", PRIMARY_INCOME_KEYWORDS, min_row=12, max_row=166, min_col=2,
                                           max_col=8, trx_type="income", is_inverse_section=True)
        logging.info("Added Other Income Section")

        income_expense_tracker.add_section("Rent & Utilities", RENT_UTIL_KEYWORDS, min_row=7, max_row=14, min_col=10,
                                           max_col=16)
        logging.info("Added Rent & Utilities Section")

        income_expense_tracker.add_section("Groceries", GROCERY_KEYWORDS, min_row=18, max_row=37, min_col=10,
                                           max_col=16, keyword_exceptions=GAS_KEYWORDS)
        logging.info("Added Groceries Section")

        income_expense_tracker.add_section("Gas", GAS_KEYWORDS, min_row=41, max_row=50, min_col=10, max_col=16)
        logging.info("Added Gas Section")

        income_expense_tracker.add_section("Miscellaneous Fixed Expenses", FIXED_EXPENSE_KEYWORDS, min_row=54,
                                           max_row=63, min_col=10, max_col=16)
        logging.info("Added Miscellaneous Fixed Expenses Section")

        income_expense_tracker.add_section("Other Expenses", RENT_UTIL_KEYWORDS + GROCERY_KEYWORDS + GAS_KEYWORDS +
                                           FIXED_EXPENSE_KEYWORDS, min_row=67, max_row=166, min_col=10, max_col=16,
                                           is_inverse_section=True)
        logging.info("Added Other Expenses Section")

        income_expense_tracker.update_tracker()
    except TrackerError as te:
        logging.error(f"<{te.__class__.__name__}> {te}\n")
        sys.exit(1)
    finally:
        logging.info(f"Closing connection to {MONTHS_NUM_TO_NAME[month]} {year} Income & Expense Tracker")
        income_expense_tracker.close_tracker()

    logging.info(f"Successfully Updated {MONTHS_NUM_TO_NAME[month]} {year} Income & Expense Tracker")


if __name__ == "__main__":
    try:
        main(sys.argv)
    except SystemExit as exit_code:
        sys.exit(exit_code)
    except BaseException as e:
        logging.error(f"<{e.__class__.__name__}> {e}\n")
        sys.exit(2)
