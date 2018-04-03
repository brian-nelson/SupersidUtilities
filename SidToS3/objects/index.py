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

