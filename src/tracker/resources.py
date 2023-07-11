import configparser
import logging
import os
import sys


# Set up ConfigParser
config = configparser.ConfigParser()
config_file = None
# Define which paths in sys.path to search for the config file
PROJECT_PATHS_STOP_IDX = int(os.getenv('ROOT_PATH_INDEX')) + 1
for path in sys.path[:PROJECT_PATHS_STOP_IDX]:
    if os.path.isfile(f"{path}/config.ini"):
        config_file = f"{path}/config.ini"
        break
try:
    if not config_file:
        raise FileNotFoundError("Please create a \"config.ini\" file in the project root directory")
except FileNotFoundError as fnfe:
    logging.error(f"<{fnfe.__class__.__name__}> {fnfe}\n")
    sys.exit(1)
config.read(config_file)

# Constants
MONTHS_NUM_TO_NAME = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July",
                      8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
try:
    CREDIT_CARD_KEYWORDS = config.get("Transaction Keywords", "CREDIT_CARD").split(",")

    FIXED_EXPENSE_KEYWORDS = config.get("Transaction Keywords", "FIXED_EXPENSES").split(",")

    GAS_KEYWORDS = config.get("Transaction Keywords", "GASOLINE").split(",")

    GROCERY_KEYWORDS = config.get("Transaction Keywords", "GROCERIES").split(",")

    PRIMARY_INCOME_KEYWORDS = config.get("Transaction Keywords", "PRIMARY_INCOME").split(",")

    RENT_UTIL_KEYWORDS = config.get("Transaction Keywords", "RENT_UTIL").split(",")
except configparser.NoSectionError as nse:
    logging.error(f"<{nse.__class__.__name__}> {nse}\n")
    sys.exit(1)
except configparser.NoOptionError as noe:
    logging.error(f"<{noe.__class__.__name__}> {noe}\n")
    sys.exit(1)


# Functions
def confirm_proceeding_with_parameters(month: str, year: int):
    """Confirm the month and year parameters input by the user before proceeding with update

    Parameters
    ----------
    month : str
        The name of the month to be updated in the Income & Expense Tracker
    year : int
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


def verify_user_inputs(argv: list) -> (int, int):
    """Verify inputs from the user match expectations

    Parameters
    ----------
    argv : list
        List of user inputs

    Returns
    -------
    tuple[int, int]
        The month and year of the Income & Expenses sheet to update

    Raises
    ------
    ValueError
        If user inputs do not meet expectations
    """
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

    return month, year
