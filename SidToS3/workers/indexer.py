from aws.s3 import S3
from helpers.s3helper import S3Helper
import json
import os
from objects.index import DataIndex
from objects.indexentry import DataFile
from datetime import datetime

class Indexer:

    def __init__(self, config):
        self.Config = config

        return

    # creates a monthly index file for all processed files
    # the fill will have day entries for each day that has
    # been loaded.  The intent is that these json indexes
    # can be used with a mustache template (or other) to build a
    # web page automatically
    # 2018-03
    # - Station - abcde
    # - Callsign - NML
    # - Files
    #   - File
    #     - Date - 2018-03-01
    #     - Chart - downloads.abc.com/abcde/nml/charts/2018-03-01.png
    #     - Datafile - downloads.abc.com/abcde/nml/data/2018-03-01.csv
    def index_new_files(self, processed_files):
        s3 = S3(
            self.Config.AWS.Key,
            self.Config.AWS.Secret,
            self.Config.AWS.Bucket)

        s3helper = S3Helper(s3)

        # create dictionary of local index files
        month_indexes = dict()

        # loop through all files that were processed
        for processed_file in processed_files:
            #store local variables
            sitename = processed_file.Sitename
            call_sign = processed_file.StationCallsign;
            file_date = processed_file.Datetime.date;

            # build the key for the dictionary for this processed file
            key = self.build_index_key(
                sitename,
                call_sign,
                file_date)

            # do we already have the index file
            if key not in month_indexes:
                # We do not.
                # get the file from s3
                index = self.get_index_file_from_S3(
                    s3,
                    sitename,
                    call_sign,
                    key,
                    self.Config.TempPath)

                # if we didn't find it build a new one
                # and add it to the dictionary
                if index is None:
                    month_indexes[key] = DataIndex(
                        sitename,
                        call_sign,
                        file_date.year,
                        file_date.month)

            # pull the index file from the dictionary
            month_index = month_indexes[key]

            # find the entry for the date
            data_file = month_index.findDataFile(file_date)

            if data_file is None:
                data_file = DataFile(file_date)
                month_index.Files.append(data_file)
            
            data_file.Chart = processed_file.RemoteChartFilename
            data_file.Datafile = processed_file.RemoteDateFilename

        # todo
        # for each index file
        #    serialize to json
        #    save to s3

        return

    def write_index_file_to_s3(self, index, s3helper, supersid_path, site, station, key, temp_folder):
        local_file = "{0}/{1}.json".format(temp_folder, key)
        self.write_index_file(index, local_file)

        remote_file = s3helper.load_file(
            supersid_path,
            site,
            station,
            "index",
            local_file)

        os.remove(local_file)

        return

    def write_index_file(self, index, local_file):
        json.dump(index, open(local_file))

    def read_index_file(self, local_file):
        index = json.load(open(local_file))

        return index


    def get_index_file_from_S3(self, s3helper, supersid_path, site, station, key, temp_folder):
        local_file = s3helper.get_file(
            supersid_path,
            site,
            station,
            "index",
            key + ".json",
            temp_folder)

        if local_file is None:
            return None

        return self.read_index_file(local_file)

    @staticmethod
    def build_index_key(site, station, datetime):
        return "{0}_{1}_{2}".format(
            site,
            station,
            datetime.strftime("%Y-%m"))