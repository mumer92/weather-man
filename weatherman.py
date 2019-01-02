from argparse import ArgumentParser
from collections import namedtuple
from termcolor import colored


import glob
import calendar

Date = namedtuple('Date', ['year', 'month', 'day'])


class Temperature:
    def __init__(self, date, max_temp, mean_temp, min_temp, dew_point,
                 mean_dew_point, min_dew_point, max_humidity, mean_humidity,
                 min_humidity, max_sea_level_pressure, mean_sea_level_pressure,
                 min_sea_level_pressure, max_visibility, mean_visibility,
                 min_visibility, max_wind_speed, mean_wind_speed,
                 max_gust_speed, percipitation, cloud_cover, events, wind_dir):

        self.date = date
        self.max_temp = max_temp
        self.mean_temp = mean_temp
        self.min_temp = min_temp
        self.dew_point = dew_point
        self.mean_dew_point = mean_dew_point
        self.min_dew_point = min_dew_point
        self.max_humidity = max_humidity
        self.mean_humidity = mean_humidity
        self.min_humidity = min_humidity
        self.max_sea_level_pressure = max_sea_level_pressure
        self.mean_sea_level_pressure = mean_sea_level_pressure
        self.min_sea_level_pressure = min_sea_level_pressure
        self.max_visibility = max_visibility
        self.mean_visibility = mean_visibility
        self.min_visibility = min_visibility
        self.max_wind_speed = max_wind_speed
        self.mean_wind_speed = mean_wind_speed
        self.max_gust_speed = max_gust_speed
        self.percipitation = percipitation
        self.cloud_cover = cloud_cover
        self.events = events
        self.wind_dir = wind_dir


def handle_year(year, file_path):
    text_files = glob.glob1(file_path, '*.txt')
    matched_files = [file for file in text_files if year in file]

    temperature_objects = []
    for file in matched_files:
        path = file_path + "/" + file

        with open(path) as f:
            next(f)
            temperature_list = [Temperature(*(line.split(','))) for line in f]
            temperature_objects.append(temperature_list)

    highest_object = None
    lowest_object = None
    humidity_object = None

    max_temp = 0
    min_temp = 90
    max_humidity = 0

    for item in temperature_objects:
        for x in item:
            if x.max_humidity:
                humidity = int(x.max_humidity)
                if humidity > max_humidity:
                    max_humidity = humidity
                    humidity_object = x

            if x.max_temp:
                max = int(x.max_temp)
                if max > max_temp:
                    max_temp = max
                    highest_object = x

            if x.min_temp:
                min = int(x.min_temp)
                if min < min_temp:
                    min_temp = min
                    lowest_object = x

    print('Highest: {0}C on {1} {2}'.format(
        highest_object.max_temp, month_name(highest_object.date),
        day_id(highest_object.date)))
    print('Lowest: {0}C on {1} {2}'.format(
        lowest_object.max_temp, month_name(lowest_object.date),
        day_id(lowest_object.date)))
    print('Humidity: {0} % on {1} {2}'.format(
        humidity_object.max_humidity, month_name(humidity_object.date),
        day_id(humidity_object.date)))


def day_id(date):
    splitted = date.split('-')
    return splitted[2]


def month_id(date):
    splitted = date.split('-')
    return splitted[1]


def month_name(date):
    splitted = date.split('-')
    name = calendar.month_name[int(splitted[1])]
    return name


def handle_year_month(year, month, file_path):
    text_files = glob.glob1(file_path, '*.txt')
    matched_files = [s for s in text_files if year in s]

    temperature_objects = []
    for file in matched_files:
        path = file_path + "/" + file

        with open(path) as f:
            next(f)
            temperature_list = [Temperature(*(line.split(','))) for line in f]
            temperature_objects.append(temperature_list)

    max_temp = []
    min_temp = []
    humidity = []

    for item in temperature_objects:
        for x in item:
            if month == month_id(x.date):
                if x.max_humidity:
                    humid = int(x.max_humidity)
                    humidity.append(humid)

                if x.max_temp:
                    max = int(x.max_temp)
                    max_temp.append(max)

                if x.min_temp:
                    min = int(x.min_temp)
                    min_temp.append(min)

    if (max_temp, min_temp, humidity):
        mean_max_temp = sum(max_temp) / len(max_temp)
        mean_min_temp = sum(min_temp) / len(min_temp)
        mean_humidity = sum(humidity) / len(humidity)

        print('Highest Average: {0}C'.format(int(mean_max_temp)))
        print('Lowest Average: {0}C'.format(int(mean_min_temp)))
        print('Average Mean Humidity: {0}%'.format(int(mean_humidity)))
    else:
        print("Not data availabe for month {0}".format(month))


def handle_year_month_for_each_day(year, month, file_path):
    text_files = glob.glob1(file_path, '*.txt')
    matched_files = [s for s in text_files if year in s]

    temperature_objects = []
    for file in matched_files:
        path = file_path + "/" + file

        with open(path) as f:
            next(f)
            temperature_list = [Temperature(*(line.split(','))) for line in f]
            temperature_objects.append(temperature_list)

    for item in temperature_objects:
        for x in item:
            if month == month_id(x.date):
                if x.max_temp:
                    max = int(x.max_temp)
                    plus = '+' * max
                    print(colored('{0} {1}{2}C'.format(
                        day_id(x.date), plus, max), 'red'))

                if x.min_temp:
                    min = int(x.min_temp)
                    plus = '+' * min
                    print(colored('{0} {1}{2}C'.format(
                        day_id(x.date), plus, min), 'blue'),)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('file_path', metavar='string', type=str)
    parser.add_argument('-e', type=str)
    parser.add_argument('-a', type=str)
    parser.add_argument('-c', type=str)

    args = parser.parse_args()

    file_path = args.file_path

    if args.e:
        print('\n')
        arg = args.e
        handle_year(arg, file_path)

    if args.a:
        print('\n')
        arg = args.a
        year, month = arg.split('/')
        handle_year_month(year, month, file_path)

    if args.c:
        print('\n')
        arg = args.c
        year, month = arg.split('/')
        handle_year_month_for_each_day(year, month, file_path)
