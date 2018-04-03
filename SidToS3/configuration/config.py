import configparser
from configuration.awsconfig import AwsConfig
from configuration.station import Station


class Config:

    def __init__(self, filename):
        self.filename = filename
        self._load()

        return

    def _load(self):
        cp = configparser.ConfigParser()
        cp.read(self.filename)

        self.SiteName = cp.get('PARAMETERS', 'site_name')
        self.Country = cp.get('PARAMETERS', 'country')
        self.Latitude = cp.get('PARAMETERS', 'latitude')
        self.Longitude = cp.get('PARAMETERS', 'longitude')
        self.AudioSamplingRate = cp.get('PARAMETERS', 'audio_sampling_rate')
        self.LogInterval = cp.get('PARAMETERS', 'log_interval')
        self.LogType = cp.get('PARAMETERS', 'log_type')
        self.ScalingFactor = cp.get('PARAMETERS', 'scaling_factor')
        self.UtcOffset = cp.get('PARAMETERS', 'utc_offset')
        self.Timezone = cp.get('PARAMETERS', 'time_zone')
        self.MonitorId = cp.get('PARAMETERS', 'monitor_id')
        self.HourlySave = cp.get('PARAMETERS', 'hourly_save')
        self.DataPath = cp.get('PARAMETERS', 'data_path')
        self.TempPath = cp.get('PARAMETERS', 'temp_path')
        self.NumberOfStations = int(cp.get('PARAMETERS', 'number_of_stations'))
        self.Stations = []

        for x in range(0, self.NumberOfStations):
            station_name = 'STATION_{0}'.format(x + 1)
            call_sign = cp.get(station_name, 'call_sign')
            color = cp.get(station_name, 'color')
            frequency = cp.get(station_name, 'frequency')

            station = Station(call_sign, color, frequency)
            self.Stations.append(station)

        aws_key = cp.get('AWS', 'key')
        aws_secret = cp.get('AWS', 'secret')
        aws_bucket = cp.get('AWS', 'bucket')
        data_path = cp.get('AWS', 'datapath')
        chart_path = cp.get('AWS', 'chartpath')

        aws_config = AwsConfig(aws_key, aws_secret, aws_bucket, data_path, chart_path)
        self.AWS = aws_config

        return
