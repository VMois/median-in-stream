class RunningMedian:
    n = 0
    _median = 0

    def push(self, new_number: int):
        self.n += 1
        weighted_average = (new_number - self._median) / self.n
        self._median += weighted_average
    
    def median(self):
        return self._median

# A = RunningMedian()
# A.push(1)
# A.push(2)
# A.push(3)
# A.push(4)

# print(A.median)  # 2.5