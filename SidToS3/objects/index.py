from datetime import datetime


class DataIndex:

    def __init__(self):
        current = datetime.utcnow().date()
        self.Site = ""
        self.StationCallsign = ""
        self.Month = current.month
        self.Year = current.year
        self.Files = []

        return

    def __init__(self, site, station_callsign, month, year):
        self.Site = site
        self.StationCallsign = station_callsign
        self.Month = month
        self.Year = year
        self.Files = []

        return

    def findDataFile(self, file_date):
        # Todo - this could be made to be more efficient
        # with a dictionary, but may not be worth effort
        for df in self.Files:
            if df.Date == file_date:
                return df

        return None