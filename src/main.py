"""Update the Income & Expense Tracker for the month & year input by the User"""
import logging
import sys
import tracker.resources as tr
from tracker.exceptions import TrackerError
from tracker.income_expense_tracker import IncomeExpenseTracker


def main(argv: list[str]):
    # Receive, verify, and confirm User input specifying month & year of Income&Expense Tracker to update
    try:
        month, year = tr.verify_user_inputs(argv)
        tr.confirm_proceeding_with_parameters(tr.MONTHS_NUM_TO_NAME[month], year)
    except ValueError as input_error:
        logging.error(f"<{input_error.__class__.__name__}> {input_error}\n")
        sys.exit(tr.EXPECTED_ERR_NO)
    except KeyboardInterrupt as abort_msg:
        logging.info(f"<{abort_msg.__class__.__name__}> {abort_msg}\n")
        sys.exit(tr.EXPECTED_ERR_NO)

    # Connect to Income&Expense Tracker Sheet corresponding to the month & year input by the User
    logging.info(f"Connecting to {tr.MONTHS_NUM_TO_NAME[month]} {year} Income & Expense Tracker...")
    try:
        income_expense_tracker = IncomeExpenseTracker(tr.MONTHS_NUM_TO_NAME[month], month, year)
    except TrackerError as conn_error:
        logging.error(f"<{conn_error.__class__.__name__}> {conn_error}\n")
        sys.exit(tr.EXPECTED_ERR_NO)
    logging.info("Connection Successful")

    # Define/Add sections to the Income&Expense Tracker Sheet, then update the Tracker Sheet
    try:
        income_expense_tracker.add_section("Primary Income", tr.PRIMARY_INCOME_KEYWORDS, min_row=7, max_row=8,
                                           min_col=2, max_col=8, trx_type="income")
        logging.info("Added Primary Income Section")

        income_expense_tracker.add_section("Other Income", tr.PRIMARY_INCOME_KEYWORDS, min_row=12, max_row=166,
                                           min_col=2, max_col=8, trx_type="income", is_inverse_section=True)
        logging.info("Added Other Income Section")

        income_expense_tracker.add_section("Rent & Utilities", tr.RENT_UTIL_KEYWORDS, min_row=7, max_row=14, min_col=10,
                                           max_col=16)
        logging.info("Added Rent & Utilities Section")

        income_expense_tracker.add_section("Groceries", tr.GROCERY_KEYWORDS, min_row=18, max_row=37, min_col=10,
                                           max_col=16, keyword_exceptions=tr.GAS_KEYWORDS)
        logging.info("Added Groceries Section")

        income_expense_tracker.add_section("Gas", tr.GAS_KEYWORDS, min_row=41, max_row=50, min_col=10, max_col=16)
        logging.info("Added Gas Section")

        income_expense_tracker.add_section("Miscellaneous Fixed Expenses", tr.FIXED_EXPENSE_KEYWORDS, min_row=54,
                                           max_row=63, min_col=10, max_col=16)
        logging.info("Added Miscellaneous Fixed Expenses Section")

        income_expense_tracker.add_section("Other Expenses", tr.RENT_UTIL_KEYWORDS + tr.GROCERY_KEYWORDS +
                                           tr.GAS_KEYWORDS + tr.FIXED_EXPENSE_KEYWORDS, min_row=67, max_row=166,
                                           min_col=10, max_col=16, is_inverse_section=True)
        logging.info("Added Other Expenses Section")

        income_expense_tracker.update_tracker()
    except TrackerError as te:
        logging.error(f"<{te.__class__.__name__}> {te}\n")
        sys.exit(tr.EXPECTED_ERR_NO)
    finally:
        logging.info(f"Closing connection to {tr.MONTHS_NUM_TO_NAME[month]} {year} Income & Expense Tracker")
        income_expense_tracker.close_tracker()

    logging.info(f"Successfully Updated {tr.MONTHS_NUM_TO_NAME[month]} {year} Income & Expense Tracker")


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s | %(levelname)s\t| %(module)s.%(funcName)s:%(lineno)d - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)
    try:
        main(sys.argv)
    except SystemExit as exit_code:
        sys.exit(exit_code)
    except BaseException as e:
        logging.error(f"<{e.__class__.__name__}> {e}\n")
        sys.exit(tr.UNEXPECTED_ERR_NO)
