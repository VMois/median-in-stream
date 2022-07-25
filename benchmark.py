import time
import sys

import pandas as pd

from running_median import RunningMedian
from remedian import Remedian

sensor_data = pd.read_csv('sensor_data_reducted.csv')
print(sensor_data.describe())

running_median = RunningMedian()
remedian = Remedian(11)  # buffer size can be adjusted here

running_median_time = time.time()
sensor_data['temp'].apply(running_median.push)
print("\nRunningMedian, "
      f"median: {running_median.median()}, "
      f"time: {time.time() - running_median_time}, "
      f"memory (in bytes): {sys.getsizeof(running_median)}")


remedian_time = time.time()
sensor_data['temp'].apply(remedian.push)
print(f"\nRemedian, median: {remedian.median()}, "
      f"time: {time.time() - remedian_time}, memory (in bytes): {sys.getsizeof(remedian)}")


def basic_median(data):
    n = len(data)
    s = sorted(data)
    if n % 2:
        return s[n // 2 - 1] / 2.0 + s[n // 2] / 2.0
    else:
        return s[n // 2]

temperatures = sensor_data['temp'].tolist()
default_time = time.time()
median = basic_median(temperatures)
print(f"\nBasic median, median: {median}, "
      f"time: {time.time() - default_time}, memory (in bytes): {sys.getsizeof(temperatures)}")