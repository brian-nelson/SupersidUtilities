from aws.s3 import S3
from datetime import datetime
from workers.datafileloader import DataFileLoader
from workers.chartbuilder import ChartBuilder
import os


class FileProcessor:

    def __init__(self, config):
        self.Config = config

        return

    def process(self):
        s3 = S3(
            self.Config.AWS.Key,
            self.Config.AWS.Secret,
            self.Config.AWS.Bucket)

        data_file_loader = DataFileLoader(s3)
        chart_builder = ChartBuilder(s3)

        utc_now = datetime.utcnow()
        utc_string = utc_now.date().isoformat()

        # Loop through the stations
        for station in self.Config.Stations:
            # Get the files for the specified station
            files = self.list_files(self.Config.DataPath, self.Config.SiteName, station.CallSign)

            for file in files:
                # Get the filename
                basename = os.path.basename(file)

                # pull the date from the filename
                datepart = basename[11:21]

                # don't process current file
                if utc_string != datepart:
                    chart_builder.generate_chart(file)

                    #data_file_loader.load_file(
                    #    self.Config.DataPath,
                    #    self.Config.SiteName,
                    #    station.CallSign,
                    #    file)

        return

    @staticmethod
    def list_files(folder, site_name, call_sign):
        files = []

        prefix = "{0}_{1}".format(site_name, call_sign)

        with os.scandir(folder) as it:
            for entry in it:
                if entry.name.startswith(prefix) and entry.is_file():
                    files.append(entry.path)

        return files
