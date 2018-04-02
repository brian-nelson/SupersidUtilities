class ProcessedFile:

    def __init__(self,
                 datetime,
                 remote_chart_filename,
                 remote_data_filename):
        self.Datetime = datetime
        self.RemoteChartFilename = remote_chart_filename
        self.RemoteDateFilename = remote_data_filename

        return