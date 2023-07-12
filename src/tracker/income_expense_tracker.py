from openpyxl.cell.cell import Cell
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from transaction.transactions import Transactions
from transaction.dao.transaction_dao import FlatFileTransactionDAO
from typing import Optional
import logging
import openpyxl
import pandas as pd
import tracker.exceptions


class TrackerSection:
    def __init__(self, name: str, xl_worksheet: Worksheet, trx_type: str, keywords: list[str], min_row: int,
                 max_row: int, min_col: int, max_col: int, keyword_exceptions: list[str] = None,
                 is_inverse_section: bool = False):
        if trx_type not in ["expense", "income"]:
            raise tracker.exceptions.InvalidTrxType(f"TrackerSection requires \"expense\" or \"income\" for trx_type, "
                                                    f"got \"{trx_type}\"")
        # Public instance variables
        self.name: str = name
        self.xl_worksheet: Worksheet = xl_worksheet
        self.trx_type: str = trx_type
        self.min_row: int = min_row
        self.max_row: int = max_row
        self.min_col: int = min_col
        self.max_col: int = max_col
        # Private instance variables
        self.__keywords: list[str] = keywords
        self.__keyword_exceptions = [] if keyword_exceptions is None else keyword_exceptions
        self.__is_inverse_section: bool = is_inverse_section

    # Public methods
    def clear_contents(self):
        for row in self.xl_worksheet.iter_rows(min_row=self.min_row, min_col=self.min_col, max_row=self.max_row,
                                               max_col=self.max_col):
            for cell in row:
                if isinstance(cell, Cell):
                    cell.value = None

    def write_data(self, transactions: pd.DataFrame):
        section_trx: pd.DataFrame = transactions.loc[list(map(self.__trx_filter(), transactions['Description'])), :]
        section_trx.reset_index(drop=True, inplace=True)
        if len(section_trx) > (self.max_row - self.min_row + 1):
            raise tracker.exceptions.InsufficientTrackerSectionSize(f"TrackerSection \"{self.name}\" transactions "
                                                                    f"({len(section_trx)}) exceeds row allowance "
                                                                    f"({self.max_row - self.min_row + 1})")

    # Private methods
    def __eq__(self, other):
        return self.name == other.name and self.trx_type == other.trx_type \
               and self.min_row == other.min_row and self.max_row == other.max_row \
               and self.min_col == other.min_col and self.max_col == other.max_col \
               and self.__keywords == other._TrackerSection__keywords \
               and self.__is_inverse_section == other._TrackerSection__is_inverse_section

    def __trx_filter(self):
        if self.__is_inverse_section:
            if len(self.__keyword_exceptions) == 0:
                return lambda text: all(key_word not in text for key_word in self.__keywords)
            else:
                return lambda text: all(key_word not in text for key_word in self.__keywords) or \
                                    any(kw_ex in text for kw_ex in self.__keyword_exceptions)
        else:
            if len(self.__keyword_exceptions) == 0:
                return lambda text: any(key_word in text for key_word in self.__keywords)
            else:
                return lambda text: (any(key_word in text for key_word in self.__keywords)) and \
                                    all(kw_ex not in text for kw_ex in self.__keyword_exceptions)


class IncomeExpenseTracker:
    def __init__(self, month_name: str, month_num: int, year: int, tracker_root_path: str):
        # Public instance variables
        self.month_name: str = month_name
        self.month_num: int = month_num
        self.year: int = year
        # Private instance variables
        # TODO: Move tracker_root_path to class variable
        self.__tracker_root_path: str = tracker_root_path
        self.__transactions: Optional[Transactions] = None
        self.__xl_workbook_path: str = f"{tracker_root_path}/{year}/Income&Expenses{year}.xlsx"
        try:
            self.__xl_workbook: Workbook = openpyxl.load_workbook(self.__xl_workbook_path)
            self.__xl_worksheet: Worksheet = self.__xl_workbook[f"{month_name} {year}"]
        except FileNotFoundError as fnfe:
            raise tracker.exceptions.TrackerWorkbookDoesNotExist(fnfe)
        except KeyError as ke:
            raise tracker.exceptions.TrackerWorksheetDoesNotExist(ke)
        self.__sections: dict[str, TrackerSection] = {}

    # Public methods
    def add_section(self, name: str, keywords: list[str], min_row: int, max_row: int, min_col: int, max_col: int,
                    trx_type: str = "expense", keyword_exceptions: list[str] = None, is_inverse_section: bool = False):
        if name in self.__sections.keys():
            raise tracker.exceptions.TrackerSectionAlreadyExists(f"Section \"{name}\" already exists. If you'd like to "
                                                                 f"replace the existing section, make a call to the "
                                                                 f"\"replace_section()\" method instead.")

        section = TrackerSection(name, self.__xl_worksheet, trx_type, keywords, min_row, max_row, min_col, max_col,
                                 keyword_exceptions, is_inverse_section)
        self.__sections[section.name] = section

    def close_tracker(self):
        if self.__xl_workbook:
            self.__xl_workbook.close()

    def delete_section(self, name: str):
        if name not in self.__sections.keys():
            raise tracker.exceptions.TrackerSectionDoesNotExist(f"Cannot delete section \"{name}\" because it does "
                                                                f"not exist")
        del self.__sections[name]

    def replace_section(self, name: str, keywords: list[str], min_row: int, max_row: int, min_col: int, max_col: int,
                        trx_type: str = "expense", keyword_exceptions: list[str] = None,
                        is_inverse_section: bool = False):
        if name not in self.__sections.keys():
            raise tracker.exceptions.TrackerSectionDoesNotExist(f"Cannot replace section \"{name}\" because it does "
                                                                f"not exist")

        section = TrackerSection(name, self.__xl_worksheet, trx_type, keywords, min_row, max_row, min_col,
                                 max_col, keyword_exceptions, is_inverse_section)
        if section == self.__sections[name]:
            raise tracker.exceptions.ReplaceTrackerSectionError(f"Replacement TrackerSection is identical to current "
                                                                f"one")
        self.__sections[name] = section

    def update_tracker(self):
        logging.info(f"Clearing {self.month_name} {self.year} Income & Expense Tracker Contents")
        self.__clear_tracker_contents()
        logging.info(f"Pulling Updated Transactions Data for {self.month_name} {self.year}")
        self.__get_transactions()
        logging.info(f"Writing Updated {self.month_name} {self.year} Transactions Data to Tracker")
        self.__write_transaction_data_to_tracker()
        logging.info(f"Saving Updates to {self.month_name} {self.year} Income & Expense Tracker")
        self.__xl_workbook.save(self.__xl_workbook_path)
        self.__xl_workbook.close()

    # Private methods
    def __clear_tracker_contents(self):
        for section in self.__sections.values():
            section.clear_contents()

    def __get_transactions(self):
        if not self.__transactions:
            self.__transactions = Transactions(self.month_num, self.year,
                                               FlatFileTransactionDAO(self.__tracker_root_path))

        self.__transactions.get_transactions_for_the_period()

    def __write_transaction_data_to_tracker(self):
        for section in self.__sections.values():
            if section.trx_type == "expense":
                trx = self.__transactions.get_expenses()
            else:
                trx = self.__transactions.get_income()
            section.write_data(trx)
