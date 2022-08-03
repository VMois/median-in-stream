import pandas as pd

from running_median import RunningMedian

sensor_data = pd.read_csv('sensor_data_reducted.csv')

A = RunningMedian()
sensor_data['temp'][:48803].apply(A.push)

B = RunningMedian()
sensor_data['temp'][48803:].apply(B.push)

total_n = A.n + B.n
median_A_B = A.median() + (B.n / total_n) * (B.median() - A.median())
