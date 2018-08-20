import os
import glob
import csv
import json
from collections import defaultdict
from collections import OrderedDict
import argparse
import datetime
aDict = OrderedDict()
filtered_dict = OrderedDict()

i = 0
j = 0
x = []
y = []


class LoadingData:

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
                        aDict[key] = temp


class ResultCalculation:

    #def __init__(self, year, month):
    #    self.year = year
    #    self.month = month

    def yearly_data_calculation(self, year):
        self.year=year
        self.Max_Temp_Dict = ()
        self.Min_Temp_Dict = ()
        self.Max_Humidity_Dict = ()
        self.Max_Temp_keys = ()
        self.Min_Temp_keys = ()
        self.Max_Humidity_keys = ()

        for k, v in aDict.items():
            if isinstance(v, OrderedDict):
                for key, value in list(v.items()):
                    try:
                        if not value:
                            v[key] = str(10000000)
                    except:
                        pass

        for k in aDict.keys():
            if str(year) in k:
                filtered_dict[k] = aDict.get(k)

        Max_Temp_Dict = OrderedDict(sorted(filtered_dict.items(), key=lambda x: x[1]['Max TemperatureC'], reverse=True))
        Min_Temp_Dict = OrderedDict(sorted(filtered_dict.items(), key=lambda x: x[1]['Min TemperatureC'], reverse=False))
        Max_Humidity_Dict = OrderedDict(sorted(filtered_dict.items(), key=lambda x: x[1]['Max Humidity'], reverse=True))
        Max_Temp_keys = list(Max_Temp_Dict.keys())
        Min_Temp_keys = list(Min_Temp_Dict.keys())
        Max_Humidity_keys = list(Max_Humidity_Dict.keys())
        print('Maximum temperature value ' + str((Max_Temp_Dict.get(Max_Temp_keys[0])).get('Max TemperatureC')) + ' was recorded on ' + str(Max_Temp_keys[0]))
        print('Minimum temperature value ' + str((Min_Temp_Dict.get(Min_Temp_keys[0])).get('Min TemperatureC')) + ' was recorded on ' + str(Min_Temp_keys[0]))
        print('Maximum humidity value '  + str((Max_Humidity_Dict.get(Max_Humidity_keys[0])).get('Max Humidity')) + ' was recorded on ' + str(Max_Humidity_keys[0]))



    def monthly_data_calculation(self, year, month):
        self.year=year
        self.month=month

        sum_highest_temp = 0
        sum_lowest_temp = 0
        sum_mean_humidity = 0
        average_highest_temp = 0
        average_lowest_temp = 0
        average_mean_humidity = 0

        for k, v in aDict.items():
            if isinstance(v, OrderedDict):
                for key, value in list(v.items()):
                    try:
                        if not value:
                            v[key] = str(0)
                    except:
                        pass

        for k in aDict.keys():
            if str(year) + '-' + str(month) in k:
                filtered_dict[k] = aDict.get(k)

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
        self.year=year
        self.month=month

        for k, v in aDict.items():
            if isinstance(v, OrderedDict):
                for key, value in list(v.items()):
                    try:
                        if not value:
                            v[key] = str(0)
                    except:
                        pass

        for k in aDict.keys():
            if str(year) + '-' + str(month) in k:
                filtered_dict[k] = aDict.get(k)

        for k, v in filtered_dict.items():
            if isinstance(v, OrderedDict):
                for key, value in v.items():
                    if key == 'Max TemperatureC':
                        x.append(int(v[key]))
                    if key == 'Min TemperatureC':
                        y.append(int(v[key]))

        red = '\033[91m'
        blue = '\033[94m'
        grey = '\033[37m'
        global i
        global j
        while i < len(x):
            print(i, red, '+' * x[i], x[i], 'C')
            print(i, blue, '+' * y[i], y[i], 'C')
            i += 1

        while j < len(x):
            print(j, blue, '+' * y[j], red, '+' * x[j], y[j], 'C', '-', x[j], 'C')
            j += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Enter the path to directory containing your weather files')
    parser.add_argument('-e','--date1',type=str)
    parser.add_argument('-a', '--date2', type=str)
    parser.add_argument('-c', '--date3',type=str)

    args = parser.parse_args()
    file_path = args.path
    load_data = LoadingData(file_path)

    if args.date2:
        date2=args.date2
        date2 = datetime.datetime.strptime(date2, "%Y/%m")
        calcobj = ResultCalculation()
        calcobj.monthly_data_calculation(date2.year, date2.month)

    if args.date3:
        date3 = args.date3
        date3 = datetime.datetime.strptime(date3, "%Y/%m")
        print(date3.year)
        print(date3.month)
        calcobj = ResultCalculation()
        calcobj.monthly_graph_plotting(date3.year, date3.month)

    if args.date1:
        date1=args.date1
        calcobj = ResultCalculation()
        calcobj.yearly_data_calculation(date1)




if __name__ == '__main__':
    main()