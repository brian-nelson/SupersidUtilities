from aws.s3 import S3
from helpers.s3helper import S3Helper
import json
import os
from objects.index import DataIndex

class Indexer:

    def __init__(self, config):
        self.Config = config

        return

    def index_new_files(self, processed_files):
        s3 = S3(
            self.Config.AWS.Key,
            self.Config.AWS.Secret,
            self.Config.AWS.Bucket)

        s3helper = S3Helper(s3)

        # todo
        # for each processed file
        #   Is the index file already in memory
        #   No - pull file from server
        #        deserialize into dataindex and datafile
        #        add to local collection
        #   Is file and chart already in the index
        #   No - add file to index
        # for each index file
        #    serialize to json
        #    save to s3

        month_indexes = dict()

        for processed_file in processed_files:
            key = self.build_index_key(
                processed_file.Sitename,
                processed_file.StationCallsign,
                processed_file.Datetime)

            if key not in month_indexes:
                index = self.get_index_file_from_S3(
                    s3,
                    processed_file.Sitename,
                    processed_file.StationCallsign,
                    key,
                    self.Config.TempPath)

                if index is None:
                    month_indexes[key] = DataIndex()

            month_index = month_indexes[key]
            


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
            datetime.strftime("%Y-%m-%d"))