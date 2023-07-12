from transaction.transactions import Transactions
import logging
import openpyxl
import pandas as pd
import tracker.exceptions


class TrackerSection:
    def __init__(self, name: str, xl_worksheet: openpyxl.workbook.workbook.Worksheet, transactions: pd.DataFrame,
                 keywords: list[str], min_row: int, max_row: int, min_col: int, max_col: int,
                 is_inverse_section: bool = False):
        # Public instance variables
        self.name: str = name
        self.xl_worksheet: openpyxl.workbook.workbook.Worksheet = xl_worksheet
        self.min_row: int = min_row
        self.max_row: int = max_row
        self.min_col: int = min_col
        self.max_col: int = max_col
        # Private instance variables
        self.__keywords: list[str] = keywords
        self.__section_trx: pd.DataFrame = transactions # TODO: Filter based on keywords/is_inverse_section

    def clear_contents(self):
        pass

    def write_data(self):
        pass

    def __eq__(self, other):
        return self.name == other.name and self.min_row == other.min_row and self.max_row == other.max_row \
               and self.min_col == other.min_col and self.max_col == other.max_col \
               and self.__keywords == other._TrackerSection__keywords \
               and self.__section_trx.equals(other._TrackerSection__section_trx)


class IncomeExpenseTracker:
    def __init__(self, month: str, year: int, tracker_root_path: str):
        # Public instance variables
        self.month: str = month
        self.year: int = year
        # Private instance variables
        self.__transactions: Transactions = None
        self.__xl_workbook_path: str = f"{tracker_root_path}/{year}/Income&Expenses{year}.xlsx"
        try:
            self.__xl_workbook: openpyxl.Workbook = openpyxl.load_workbook(self.__xl_workbook_path)
            self.__target_xl_worksheet: openpyxl.workbook.workbook.Worksheet = self.__xl_workbook[f"{month} {year}"]
        except FileNotFoundError as fnfe:
            raise tracker.exceptions.TrackerWorkbookDoesNotExist(fnfe)
        except KeyError as ke:
            raise tracker.exceptions.TrackerWorksheetDoesNotExist(ke)
        self.__sections: dict[str, TrackerSection] = {}

    # Public methods
    def add_section(self, name: str, keywords: list[str], min_row: int, max_row: int, min_col: int, max_col: int,
                    trx_type: str = "expense", is_inverse_section: bool = False):
        if trx_type not in ["expense", "income"]:
            raise tracker.exceptions.InvalidTrxType(f"Expected \"expense\" or \"income\" for trx_type, got "
                                                    f"\"{trx_type}\"")
        if name in self.__sections.keys():
            raise tracker.exceptions.TrackerSectionAlreadyExists(f"Section \"{name}\" already exists. If you'd like to "
                                                                 f"replace the existing section, make a call to the "
                                                                 f"\"replace_section()\" method instead.")

        trx = self.__transactions.get_expenses() if trx_type == "expense" else self.__transactions.get_income()
        section = TrackerSection(name, self.__target_xl_worksheet, trx, keywords, min_row, max_row, min_col, max_col,
                                 is_inverse_section)
        self.__sections[section.name] = section

    def replace_section(self, name: str, keywords: list[str], min_row: int, max_row: int, min_col: int, max_col: int,
                        trx_type: str = "expense", is_inverse_section: bool = False):
        if trx_type not in ["expense", "income"]:
            raise tracker.exceptions.InvalidTrxType(f"Expected \"expense\" or \"income\" for trx_type, got "
                                                    f"\"{trx_type}\"")
        if name not in self.__sections.keys():
            raise tracker.exceptions.TrackerSectionDoesNotExist(f"Cannot replace section \"{name}\" because it does "
                                                                f"not exist")

        trx = self.__transactions.get_expenses() if trx_type == "expense" else self.__transactions.get_income()
        section = TrackerSection(name, self.__target_xl_worksheet, trx, keywords, min_row, max_row, min_col,
                                 max_col, is_inverse_section)
        if section == self.__sections[name]:
            raise tracker.exceptions.ReplaceTrackerSectionError(f"Replacement TrackerSection is identical to current "
                                                                f"one")
        self.__sections[name] = section

    def update_tracker(self):
        logging.info("Clearing Income & Expense Tracker Contents")
        self.__clear_tracker_contents()
        logging.info("Writing Updated Transactions Data to Income & Expense Tracker")
        self.__write_transaction_data_to_tracker()

    # Private methods
    def __clear_tracker_contents(self):
        for section in self.__sections.values():
            section.clear_contents()

    def __write_transaction_data_to_tracker(self):
        for section in self.__sections.values():
            section.write_data()
