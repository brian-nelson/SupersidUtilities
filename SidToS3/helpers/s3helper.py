import os


class S3Helper:

    def __init__(self, s3):
        self.S3 = s3

        return

    # Load file to S3 then delete the file
    def load_file(self, supersid_path, sitename, station_callsign, datatype, local_file):

        # Get the folder to store this data to on s3
        remote_path = "{0}/stations/{1}/{2}/{3}".format(
            supersid_path,
            sitename,
            station_callsign,
            datatype)

        # get the actual file name
        basename = os.path.basename(local_file)

        # get the remote filename
        remote_file = "{0}/{1}".format(remote_path, basename)

        # load the file to s3
        self.S3.upload_file(local_file, remote_file)

        # record that file was loaded
        print("Loaded {0} to s3".format(local_file))

        return remote_file


    def get_file(self, supersid_path, sitename, station_callsign, datatype, file_name, local_folder):
        # Get the folder to store this data to on s3
        remote_file = "{0}/stations/{1}/{2}/{3}/{4}".format(
            supersid_path,
            sitename,
            station_callsign,
            datatype,
            file_name)

        local_file = "{0}/{1}".format(local_folder, file_name);

        try:
            self.S3.download_file(remote_file, local_file)
        except:
            local_file = None

        return local_file
