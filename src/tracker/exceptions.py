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


class InvalidTrxType(TrackerSectionError):
    pass


class ReplaceTrackerSectionError(TrackerSectionError):
    pass
