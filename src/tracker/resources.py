"""Define constants and functions to be used by the program

Constants
---------
EXPECTED_ERR_NO : int
    Exit code to use when program exits due to handled exception
UNEXPECTED_ERR_NO : int
    Exit code to use when program exits due to unhandled exception
MONTHS_NUM_TO_NAME : dict[int, str]
    Mapping from number representation of each month to the name of each month
PROJECT_ROOT_PATH : str
    File path to project root directory
CREDIT_CARD_KEYWORDS : list[str]
    List of keywords to search for in transaction descriptions that qualify the transaction as part of the Credit Card
    category
FIXED_EXPENSE_KEYWORDS : list[str]
    List of keywords to search for in transaction descriptions that qualify the transaction as part of the Fixed
    Expenses category
GAS_KEYWORDS : list[str]
    List of keywords to search for in transaction descriptions that qualify the transaction as part of the Gas category
GROCERY_KEYWORDS : list[str]
    List of keywords to search for in transaction descriptions that qualify the transaction as part of the groceries
    category
PRIMARY_INCOME_KEYWORDS : list[str]
    List of keywords to search for in transaction descriptions that qualify the transaction as part of the Primary
    Income category
RENT_UTIL_KEYWORDS : list[str]
    List of keywords to search for in transaction descriptions that qualify the transaction as part of the Rent &
    Utilities category

Functions
---------
confirm_proceeding_with_parameters(month: str, year: int)
    Confirm the month and year parameters input by the user before proceeding with update
verify_user_inputs(argv: list[str]) -> tuple[int, int]
    Verify inputs from the user match expectations
"""
import configparser
import logging
import os
import sys
from pathlib import Path


# Constants
EXPECTED_ERR_NO = 1
UNEXPECTED_ERR_NO = 2

MONTHS_NUM_TO_NAME = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July",
                      8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

# main.py is executed from src/ whose parent directory is the project root directory: ExpenseTracker/
PROJECT_ROOT_PATH = str(Path(sys.path[0]).parent)

# Set up ConfigParser
expected_config_filepath = f"{PROJECT_ROOT_PATH}/config.ini"
config_file = expected_config_filepath if os.path.isfile(expected_config_filepath) else None
try:
    if not config_file:
        raise FileNotFoundError(f"Missing \"config.ini\" file in the project root directory: {PROJECT_ROOT_PATH}")
except FileNotFoundError as config_error:
    logging.error(f"<{config_error.__class__.__name__}> {config_error}\n")
    sys.exit(EXPECTED_ERR_NO)
config = configparser.ConfigParser()
config.read(config_file)

# Define keywords to search for in transaction descriptions when grouping transactions into categories
try:
    CREDIT_CARD_KEYWORDS = config.get("Transaction Keywords", "CREDIT_CARD").split(",")
    FIXED_EXPENSE_KEYWORDS = config.get("Transaction Keywords", "FIXED_EXPENSES").split(",")
    GAS_KEYWORDS = config.get("Transaction Keywords", "GASOLINE").split(",")
    GROCERY_KEYWORDS = config.get("Transaction Keywords", "GROCERIES").split(",")
    PRIMARY_INCOME_KEYWORDS = config.get("Transaction Keywords", "PRIMARY_INCOME").split(",")
    RENT_UTIL_KEYWORDS = config.get("Transaction Keywords", "RENT_UTIL").split(",")
except configparser.NoSectionError as nse:
    logging.error(f"<{nse.__class__.__name__}> {nse}\n")
    sys.exit(EXPECTED_ERR_NO)
except configparser.NoOptionError as noe:
    logging.error(f"<{noe.__class__.__name__}> {noe}\n")
    sys.exit(EXPECTED_ERR_NO)


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


def verify_user_inputs(argv: list[str]) -> tuple[int, int]:
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
