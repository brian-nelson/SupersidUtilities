class ProcessedFile:

    def __init__(self,
                 sitename,
                 station_callsign,
                 datetime,
                 remote_chart_filename,
                 remote_data_filename):

        self.Sitename = sitename
        self.StationCallsign = station_callsign
        self.Datetime = datetime
        self.RemoteChartFilename = remote_chart_filename
        self.RemoteDateFilename = remote_data_filename

        return