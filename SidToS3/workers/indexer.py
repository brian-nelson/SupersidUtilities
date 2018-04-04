from aws.s3 import S3
from helpers.s3helper import S3Helper

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
                month_indexes[key] = self.get_index_file(
                    s3,
                    processed_file.Sitename,
                    processed_file.StationCallsign,
                    key)

            month_index = month_indexes[key]

        return

    @staticmethod
    def get_index_file(s3helper, supersid_path, site, station, key, temp_folder):
        local_file = s3helper.get_file(
            supersid_path,
            site,
            station,
            "indexes",
            key + ".json",
            temp_folder)

        return local_file

    @staticmethod
    def build_index_key(site, station, datetime):
        return "{0}_{1}_{2}".format(
            site,
            station,
            datetime.strftime("%Y-%m-%d"))