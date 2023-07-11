import logging
import openpyxl


# Exceptions
class TrackerError(Exception):
    pass


class TrackerWorkbookDoesNotExist(TrackerError):
    pass


class TrackerWorksheetDoesNotExist(TrackerError):
    pass


class TrackerSectionError(TrackerError):
    pass


class TrackerSectionAlreadyExists(TrackerSectionError):
    pass


class TrackerSectionDoesNotExist(TrackerSectionError):
    pass


# IncomeExpenseTracker is composed of TrackerSections
class TrackerSection:
    def __init__(self):
        pass

    def clear_contents(self):
        pass

    def write_data(self):
        pass


class IncomeExpenseTracker:
    def __init__(self, month: str, year: int, tracker_root_path: str):
        # Public instance variables
        self.month: str = month
        self.year: int = year
        # Private instance variables
        self.__xl_workbook_path: str = f"{tracker_root_path}/{year}/Income&Expenses{year}.xlsx"
        try:
            self.__xl_workbook: openpyxl.Workbook = openpyxl.load_workbook(self.__xl_workbook_path)
            self.__target_xl_worksheet: openpyxl.workbook.workbook.Worksheet = self.__xl_workbook[f"{month} {year}"]
        except FileNotFoundError as fnfe:
            raise TrackerWorkbookDoesNotExist(fnfe)
        except KeyError as ke:
            raise TrackerWorksheetDoesNotExist(ke)
        self.__sections: dict[str, TrackerSection] = {}

    # Public methods
    def add_section(self, key: str, section: TrackerSection):
        if key in self.__sections.keys():
            raise TrackerSectionAlreadyExists(f"Section \"{key}\" already exists. If you'd like to replace the "
                                              f"existing section, make a call to the \"replace_section()\" "
                                              f"method instead.")
        else:
            self.__sections[key] = section

    def replace_section(self, key: str, section: TrackerSection):
        if key not in self.__sections.keys():
            raise TrackerSectionDoesNotExist(f"Cannot replace section \"{key}\" because it does not exist")
        else:
            self.__sections[key] = section

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
