"""Define custom Exceptions encountered by the IncomeExpenseTracker"""


# TrackerErrors
class TrackerError(Exception):
    pass


class TrackerWorkbookDoesNotExist(TrackerError):
    pass


class TrackerWorksheetDoesNotExist(TrackerError):
    pass


class EmptyTrackerError(TrackerError):
    pass


# TrackerSectionErrors
class TrackerSectionError(TrackerError):
    pass


class InsufficientTrackerSectionSize(TrackerSectionError):
    pass


class InvalidTrxType(TrackerSectionError):
    pass


class ReplaceTrackerSectionError(TrackerSectionError):
    pass


class TrackerSectionAlreadyExists(TrackerSectionError):
    pass


class TrackerSectionDoesNotExist(TrackerSectionError):
    pass
