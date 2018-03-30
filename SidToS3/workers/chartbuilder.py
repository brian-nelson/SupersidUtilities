from datetime import timedelta
from datetime import datetime
from datetime import date
from data.datafile import DataFile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from astral import Astral
from astral import Location

class ChartBuilder:

    def __init__(self, s3):
        self.S3 = s3

        return

    def generate_chart(self, data_filename):
        datafile = DataFile(data_filename)

        x = []
        y = []

        for dp in datafile.DataPoints:
            time = self.get_decimal_time(dp.ReadingTime)

            x.append(time)
            y.append(dp.ReadingValue)

        sun = self.get_sun_info(datafile)

        sunset = self.get_decimal_time(sun[0])
        sunrise = self.get_decimal_time(sun[1])

        plt.plot(x, y)
        plt.xlim(0, 24)
        plt.xlabel("UTC Time")
        plt.ylabel("Signal Strength")

        current_date = datafile.UtcStartTime.strftime("%Y-%m-%d")
        plt.title("{0}\n{1}".format(datafile.Site, current_date))
        plt.axvspan(sunset, sunrise, facecolor='blue', alpha=0.2)
        plt.savefig('/Transfer/SuperSid/Temp/test.png')

        return

    @staticmethod
    def get_decimal_time(datetime_value):
        return datetime_value.hour \
               + datetime_value.minute / 60 \
               + datetime_value.second / 3600

    @staticmethod
    def get_sun_info(datafile):

        site = Location()
        site.name = datafile.Site
        site.region = datafile.Country
        site.latitude = datafile.Latitude
        site.longitude = datafile.Longitude
        site.elevation = 0

        current_day = datafile.UtcStartTime.date()
        sun = site.sun(date=current_day)
        sunrise = sun['sunrise']

        previous_day = current_day - timedelta(days=1)
        sun = site.sun(date=previous_day)
        sunset = sun['sunset']

        return sunset, sunrise

