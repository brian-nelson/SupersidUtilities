import os
from datetime import datetime

from aws.s3 import S3
from objects.processedfile import ProcessedFile
from workers.chartrenderer import ChartRenderer
from helpers.s3helper import S3Helper


class FileProcessor:

    def __init__(self, config):
        self.Config = config

        return

    def process(self):
        s3 = S3(
            self.Config.AWS.Key,
            self.Config.AWS.Secret,
            self.Config.AWS.Bucket)

        s3_loader = S3Helper(s3)

        utc_now = datetime.utcnow()
        utc_string = utc_now.date().isoformat()

        processed_files = []

        # Loop through the stations
        for station in self.Config.Stations:
            # Get the files for the specified station
            files = self.list_files(self.Config.DataPath, self.Config.SiteName, station.CallSign)

            for file in files:
                # Get the filename
                basename = os.path.basename(file)

                # pull the date from the filename
                current_file_datepart = basename[11:21]

                # don't process current file
                if utc_string != current_file_datepart:
                    # Generate chart and load datafile
                    currentDate = datetime.strptime(current_file_datepart, "%Y-%m-%d")
                    remote_chart = self.generate_load_chart(s3_loader, station, file)

                    # upload and archive the datafile
                    remote_datafile = self.load_data_file(s3_loader, station, file)

                    # add the file to list of processed files for later indexing
                    processed_files.append(
                        ProcessedFile(
                            self.SiteName,
                            station.CallSign,
                            currentDate,
                            remote_chart,
                            remote_datafile))

        # Sort processed files by date and return
        return sorted(processed_files, key=lambda x: getattr(x, "Datetime"))

    # Generates, Loads and then deletes chart.
    def generate_load_chart(self, s3_loader, station, data_filename):
        chart_renderer = ChartRenderer()

        # Generate the chart from the data file
        temp_filename = chart_renderer.generate_chart(data_filename)

        # Load the chart to S3 in correct location
        remote_file = s3_loader.load_file(
            self.Config.AWS.ChartPath,
            self.Config.SiteName,
            station.CallSign,
            "charts",
            temp_filename)

        # remove the chart
        os.remove(temp_filename)

        # return the remote file name
        return remote_file

    # Loads data file to s3 then moves it to archive folder
    def load_data_file(self, s3_loader, station, data_filename):
        # Load the data file to S3
        remote_file = s3_loader.load_file(
            self.Config.AWS.DataPath,
            self.Config.SiteName,
            station.CallSign,
            "data",
            data_filename)

        # Archive the data file
        pathname = os.path.dirname(data_filename)
        basename = os.path.basename(data_filename)
        archive_file = "{0}/Archive/{1}".format(pathname, basename)
        os.rename(data_filename, archive_file)

        # return the remote file name
        return remote_file

    # list files that match site and callsign
    @staticmethod
    def list_files(folder, site_name, call_sign):
        files = []

        prefix = "{0}_{1}".format(site_name, call_sign)

        with os.scandir(folder) as it:
            for entry in it:
                if entry.name.startswith(prefix) and entry.is_file():
                    files.append(entry.path)

        return files
