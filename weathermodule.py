import os
import glob
import csv
import json
import argparse
import datetime

from collections import defaultdict
from collections import OrderedDict

all_data_dict = OrderedDict()
filtered_dict = OrderedDict()


class Data:

    def __init__(self, file_path):
        self.file_path = file_path

        for file in os.listdir(file_path):
            for file in glob.glob('Murree_weather_*.txt'):
                with open(file, "rt") as f:
                    csvReader = csv.reader(f)
                    fields = next(csvReader)
                    for row in csvReader:
                        temp = OrderedDict(zip(fields, row))
                        key = temp.pop(list(temp.keys())[0])
                        all_data_dict[key] = temp


class Result:

    def yearly_data_calculation(self, year):
        """A function for filtering out the data of given year from the whole data and maximum temp, minimum temp and max humidity and their respective dates"""
        self.year = year
        Max_Temp = 0
        Min_Temp = 0
        Max_Humidity = 0
        Max_Temp_key = 0
        Min_Temp_key = 0
        Max_Humidity_key = 0

        for k, v in all_data_dict.items():
            if isinstance(v, OrderedDict):
                for key, value in list(v.items()):
                    try:
                        if not value:
                            v[key] = str(10000000)
                    except:
                        pass

        for k in all_data_dict.keys():
            if str(year) in k:
                filtered_dict[k] = all_data_dict.get(k)

        for k, v in filtered_dict.items():
            if isinstance(v, OrderedDict):
                for key, value in list(v.items()):
                    if key == 'Max TemperatureC':
                        if int(v[key]) > int(Max_Temp):
                            Max_Temp = v[key]
                            Max_Temp_key = k
                    if key == 'Min TemperatureC':
                        if int(v[key]) < int(Min_Temp):
                            Min_Temp = v[key]
                            Min_Temp_key = k
                    if key == 'Max Humidity':
                        if int(v[key]) > int(Max_Humidity):
                            Max_Humidity = v[key]
                            Max_Humidity_key = k

        print('Maximum temperature value ' + str(Max_Temp) + ' was recorded on ' + str(Max_Temp_key))
        print('Minimum temperature value ' + str(Min_Temp) + ' was recorded on ' + str(Min_Temp_key))
        print('Maximum humidity value ' + str(Max_Humidity) + ' was recorded on ' + str(Max_Humidity_key))

    def monthly_data_calculation(self, year, month):
        """ A function for filtering out the data for given year and month and calculating averages of temperatures"""
        self.year = year
        self.month = month

        sum_highest_temp = 0
        sum_lowest_temp = 0
        sum_mean_humidity = 0
        average_highest_temp = 0
        average_lowest_temp = 0
        average_mean_humidity = 0

        for k, v in all_data_dict.items():
            if isinstance(v, OrderedDict):
                for key, value in list(v.items()):
                    try:
                        if not value:
                            v[key] = str(0)
                    except:
                        pass

        for k in all_data_dict.keys():
            if str(year) + '-' + str(month) in k:
                filtered_dict[k] = all_data_dict.get(k)

        for k, v in filtered_dict.items():
            if isinstance(v, OrderedDict):
                for key, value in list(v.items()):
                    if key == 'Max TemperatureC':
                        sum_highest_temp = sum_highest_temp + int(v[key])
                    if key == 'Min TemperatureC':
                        sum_lowest_temp = sum_lowest_temp + int(v[key])
                    if key == ' Mean Humidity':
                        sum_mean_humidity = sum_mean_humidity + int(v[key])
        no_of_days = len(list(filtered_dict.keys()))
        average_highest_temp = sum_highest_temp / no_of_days
        average_lowest_temp = sum_lowest_temp / no_of_days
        average_mean_humidity = sum_mean_humidity / no_of_days
        print('Average Highest Temperature was:' + str(average_highest_temp) + ' C')
        print('Average Lowest Temperature was:' + str(average_lowest_temp) + ' C')
        print('Average Mean Humidity was:' + str(average_mean_humidity))

    def monthly_graph_plotting(self, year, month):
        """A function for printing out the graphs in required format"""
        self.year = year
        self.month = month
        list_max_temp = []
        list_min_temp = []
        i = 0
        j = 0

        for k, v in all_data_dict.items():
            if isinstance(v, OrderedDict):
                for key, value in list(v.items()):
                    try:
                        if not value:
                            v[key] = str(0)
                    except:
                        pass

        for k in all_data_dict.keys():
            if str(year) + '-' + str(month) in k:
                filtered_dict[k] = all_data_dict.get(k)

        for k, v in filtered_dict.items():
            if isinstance(v, OrderedDict):
                for key, value in v.items():
                    if key == 'Max TemperatureC':
                        list_max_temp.append(int(v[key]))
                    if key == 'Min TemperatureC':
                        list_min_temp.append(int(v[key]))

        red = '\033[91m'
        blue = '\033[94m'

        while i < len(list_max_temp):
            print(i, red, '+' * list_max_temp[i], list_max_temp[i], 'C')
            print(i, blue, '+' * list_min_temp[i], list_min_temp[i], 'C')
            i += 1

        while j < len(list_max_temp):
            print(
            j, blue, '+' * list_min_temp[j], red, '+' * list_max_temp[j], list_min_temp[j], 'C', '-', list_max_temp[j],
            'C')
            j += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Enter the path to directory containing your weather files')
    parser.add_argument('-e', '--date1', type=str)
    parser.add_argument('-a', '--date2', type=str)
    parser.add_argument('-c', '--date3', type=str)

    args = parser.parse_args()
    file_path = args.path
    load_data = Data(file_path)

    if args.date2:
        date2 = args.date2
        date2 = datetime.datetime.strptime(date2, "%Y/%m")
        calcobj = Result()
        calcobj.monthly_data_calculation(date2.year, date2.month)

    if args.date3:
        date3 = args.date3
        date3 = datetime.datetime.strptime(date3, "%Y/%m")
        calcobj = Result()
        calcobj.monthly_graph_plotting(date3.year, date3.month)

    if args.date1:
        date1 = args.date1
        calcobj = Result()
        calcobj.yearly_data_calculation(date1)


if __name__ == '__main__':
    main()
