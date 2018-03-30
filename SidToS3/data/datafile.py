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
                    self.Site = line[9:-1]
                elif line.startswith("# StationID = "):
                    self.StationId = line[14:-1]
                elif line.startswith("# Contact = "):
                    self.Contact = line[12:-1]
                elif line.startswith("# Longitude = "):
                    self.Longitude = float(line[13:-1])
                elif line.startswith("# Latitude = "):
                    self.Latitude = float(line[12:-1])
                elif line.startswith("# Country = "):
                    self.Country = line[12:-1]
                elif line.startswith("# SampleRate = "):
                    self.SampleRate = line[16:-1]
                elif line.startswith("# Frequency = "):
                    self.Frequency = line[14:-1]
                elif line.startswith("# MonitorId = "):
                    self.MonitorId = line[13:-1]
                elif line.startswith("# UTC_StartTime = "):
                    self.UtcStartTime = datetime.strptime(line[18:-1], "%Y-%m-%d %H:%M:%S")
                elif line.startswith("# UTC_Offset = "):
                    self.UtcOffset = line[15:-1]
            else:
                date_string = line[0:19]
                value_string = line[21:-1]

                date_value = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
                value = float(value_string)

                data_point = DataPoint(date_value, value)
                self.DataPoints.append(data_point)

        return
