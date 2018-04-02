from datetime import datetime


class DataIndex:

    def __init__(self):
        current = datetime.utcnow().date()

        self.Month = current.month
        self.Year = current.year
        self.Files = []

        return

    def __init__(self, month, year):
        self.Month = month
        self.Year = year
        self.Files = []

        return

