import logging


# Constants
CREDIT_CARD_KEYWORDS = []

FIXED_EXPENSE_KEYWORDS = []

GAS_KEYWORDS = []

GROCERY_KEYWORDS = []

PRIMARY_INCOME_KEYWORDS = []

RENT_UTIL_KEYWORDS = []


# Functions
def confirm_proceeding_with_parameters(month: str, year: str):
    """Confirm the month and year parameters input by the user before proceeding with update

    Parameters
    ----------
    month : str
        The name of the month to be updated in the Income & Expense Tracker
    year : str
        The year to be updated in the Income & Expense Tracker

    Raises
    ------
    KeyboardInterrupt
        If the user's response to the prompt begins with "n", disregarding case
    """
    proceed = False
    user_response = ""

    while not proceed:
        user_response = input(f"Are you sure you want to update {month} {year} Income & Expenses? (y/n): ").lower()
        proceed = user_response.startswith("y") or user_response.startswith("n")

    if user_response.startswith("n"):
        raise KeyboardInterrupt("Income & Expenses Update Cancelled")
    else:
        logging.info(f"Updating {month} {year} Income & Expenses...")


def verify_user_inputs(argv: list) -> (str, str):
    """Verify inputs from the user match expectations

    Parameters
    ----------
    argv : list
        List of user inputs

    Returns
    -------
    tuple[str, str]
        The month (spelled out) and year of the Income & Expenses sheet to update

    Raises
    ------
    ValueError
        If user inputs do not meet expectations
    """
    months_num_to_name = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July",
                          8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
    expected_num_user_inputs = 3
    expected_month_input_length = 2
    expected_year_input_length = 4
    expense_tracker_start_year = 2022
    month_input_idx = 1
    year_input_idx = 2

    if len(argv) != expected_num_user_inputs:
        raise ValueError(f"Please provide month (MM) and year (YYYY) following script name: \"{str.join(' ', argv)}\"")
    if len(argv[month_input_idx]) != expected_month_input_length:
        raise ValueError(f"Month should be input immediately following the script name as a 2-digit code (01-12) "
                         f"\"{argv[month_input_idx]}\"")
    if len(argv[year_input_idx]) != expected_year_input_length:
        raise ValueError(f"Year should be input immediately following the month as a 4-digit code (YYYY): "
                         f"\"{argv[year_input_idx]}\"")

    try:
        month = int(argv[month_input_idx])
    except ValueError:
        raise ValueError(f"Invalid month parameter: {argv[month_input_idx]}")
    try:
        year = int(argv[year_input_idx])
    except ValueError:
        raise ValueError(f"Invalid year parameter: {argv[year_input_idx]}")

    if not 1 <= month <= 12:
        raise ValueError(f"Invalid month parameter: {argv[month_input_idx]}. Expected month between 01 and 12")
    if year < expense_tracker_start_year:
        raise ValueError(f"Invalid year parameter: {argv[year_input_idx]}. Expected year later than "
                         f"{expense_tracker_start_year - 1}")

    return months_num_to_name[month], argv[year_input_idx]
