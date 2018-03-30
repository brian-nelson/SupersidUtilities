import os


class DataFileLoader:

    def __init__(self, s3):
        self.S3 = s3

        return

    def load_file(self, datapath, sitename, station, localfile):

        # Get the folder to store this data to on s3
        remote_path = "{0}/{1}/{2}".format(
            datapath,
            sitename,
            station)

        # get the actual file name
        basename = os.path.basename(localfile)

        # get the remote filename
        remote_file = "{0}/{1}".format(remote_path, basename)

        # load the file to s3
        self.S3.upload_file(localfile, remote_file)

        # record that file was loaded
        print("Loaded {0} to s3".format(localfile))

        pathname = os.path.dirname(localfile)

        archive_file = "{0}/Archive/{1}".format(pathname, basename)

        os.rename(localfile, archive_file)

        return
