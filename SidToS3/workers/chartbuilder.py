from data.datafile import DataFile
import os
import cairosvg
import pygal


class ChartBuilder:

    def __init__(self, s3):
        self.S3 = s3

        return

    def generate_chart(self, data_filename):
        datafile = DataFile(data_filename)

        #x = []
        #y = []
        series = []

        for dp in datafile.DataPoints:
            #x.append(dp.ReadingTime)
            #y.append(dp.ReadingValue)
            series.append((dp.ReadingTime, dp.ReadingValue))

        chart = pygal.DateTimeLine()
        chart.add("readings", series)
        chart.render_to_png(filename='/Transfer/SuperSid/Temp/test.png')

        return

