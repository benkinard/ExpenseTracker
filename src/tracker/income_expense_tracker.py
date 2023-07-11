import openpyxl


class TrackerError(Exception):
    pass


class TrackerWorkbookDoesNotExist(TrackerError):
    pass


class TrackerWorksheetDoesNotExist(TrackerError):
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
        pass

    def replace_section(self, key: str, section: TrackerSection):
        pass

    def update_tracker(self):
        self.__clear_tracker_contents()
        self.__write_transaction_data_to_tracker()

    # Private methods
    def __clear_tracker_contents(self):
        pass

    def __write_transaction_data_to_tracker(self):
        pass


class TrackerSection:
    pass
