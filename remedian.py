import numpy as np

class Remedian:
    def __init__(self, buffer_size: int = 3):
        self.buffer_size = buffer_size
        self.buffers = []

    def _create_buffer(self):
        if self.i > len(self.buffers) - 1:
            new_buffer = [None] * self.buffer_size
            self.buffers.append(new_buffer)
    
    def _is_current_buffer_full(self):
        buffer = self.buffers[self.i]
        return buffer[-1] != None
    
    def _is_buffer_empty(self, position: int):
        buffer = self.buffers[position]
        return buffer[0] == None
    
    def _insert_number_into_buffer(self, number: int):
        buffer = self.buffers[self.i]

        for i in range(len(buffer)):
            if not buffer[i]:
                buffer[i] = number
                break
        
        return self._is_current_buffer_full()
    
    def _calculate_current_buffer_median(self):
        buffer = self.buffers[self.i]
        return np.median(buffer)
    
    def _calculate_weighted_median(self, data, weights):
        # https://gist.github.com/tinybike/d9ff1dad515b66cc0d87
        data, weights = np.array(data).squeeze(), np.array(weights).squeeze()
        s_data, s_weights = map(np.array, zip(*sorted(zip(data, weights))))
        midpoint = 0.5 * sum(s_weights)
        if any(weights > midpoint):
            w_median = (data[weights == np.max(weights)])[0]
        else:
            cs_weights = np.cumsum(s_weights)
            idx = np.where(cs_weights <= midpoint)[0][-1]
            if cs_weights[idx] == midpoint:
                w_median = np.mean(s_data[idx:idx+2])
            else:
                w_median = s_data[idx+1]
        return w_median

    def _clear_current_buffer(self):
        self.buffers[self.i] = [None] * self.buffer_size
    
    def _should_calculate_weighted_median(self):
        for i in range(len(self.buffers) - 1):
            if not self._is_buffer_empty(i):
                return True
        return self.buffers[self.i][1] is not None
    
    def _get_values_from_buffer(self, position: int):
        buffer = self.buffers[position]
        return [n for n in buffer if n is not None]
    
    def push(self, number: int):
        self.i = 0
        if len(self.buffers) == 0:
            self._create_buffer()
        
        while self._insert_number_into_buffer(number):
            number = self._calculate_current_buffer_median()
            self._clear_current_buffer()
            self.i += 1
            self._create_buffer()
    
    def median(self):
        if len(self.buffers) == 0:
            return None
        
        if self._should_calculate_weighted_median():
            values = []
            weights = []
            for i in range(len(self.buffers)):
                buffer_values = self._get_values_from_buffer(i)
                buffer_weights = [self.buffer_size**i] * len(buffer_values)
                values.extend(buffer_values)
                weights.extend(buffer_weights)
            return self._calculate_weighted_median(values, weights)
        else:
            return self.buffers[self.i][0]

# A = Remedian()
# A.push(1)
# A.push(2)
# A.push(3)
# A.push(4)
# A.push(5)
# print(A.approximate())