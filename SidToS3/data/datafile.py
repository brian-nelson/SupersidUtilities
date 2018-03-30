from datetime import datetime
from data.datapoint import DataPoint


class DataFile:

    def __init__(self, filename):
        self.Filename = filename
        self.DataPoints = []

        self._load_file()

        return

    def _load_file(self):
        file = open(self.Filename, 'r')
        lines = file.readlines()

        for line in lines:
            if line.startswith("#"):
                if line.startswith("# Site = "):
                    self.Site = line[7:13]
                elif line.startswith("# StationID = "):
                    self.StationId = line[12:15]
                elif line.startswith("# Contact = "):
                    self.Contact = line[10]
            else:
                date_string = line[0:19]
                value_string = line[21:]

                date_value = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
                value = float(value_string)

                data_point = DataPoint(date_value, value)
                self.DataPoints.append(data_point)

        return
