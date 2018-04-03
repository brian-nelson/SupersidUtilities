from datetime import timedelta
from data.datafile import DataFile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from astral import Location

class ChartRenderer:

    def __init__(self):
        return

    def generate_chart(self, data_filename, temp_path):
        datafile = DataFile(data_filename)

        x = []
        y = []

        for dp in datafile.DataPoints:
            time = self.get_decimal_time(dp.ReadingTime)

            x.append(time)
            y.append(dp.ReadingValue)

        sun = self.get_sun_info(datafile)
        sunrise = self.get_decimal_time(sun[0])
        sunset = self.get_decimal_time(sun[1])

        plt.plot(x, y)
        plt.xlim(0, 24)
        plt.xlabel("UTC Time")
        plt.ylabel("Signal Strength")

        current_date = datafile.UtcStartTime.strftime("%Y-%m-%d")
        plt.title(datafile.Site, loc='left')
        plt.title(current_date)
        plt.title("{0} - {1}".format(datafile.StationId, datafile.Frequency), loc='right')

        if sunset < sunrise:
            # Block in center
            plt.axvspan(sunset, sunrise, facecolor='blue', alpha=0.2)
        else:
            # Block on edges
            plt.axvspan(0.0, sunrise, facecolor='blue', alpha=0.2)
            plt.axvspan(sunset, 24.0, facecolor='blue', alpha=0.2)

        temp_filename = "{0}/{1}_{1}_{2}.png".format(temp_path, datafile.Site, datafile.StationId, current_date)
        plt.savefig(temp_filename)

        return temp_filename

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
        sunset = sun['sunset']

        if sunset.date() > current_day:
            previous_day = current_day - timedelta(days=1)
            sun = site.sun(date=previous_day)
            sunset = sun['sunset']

        return sunrise, sunset

