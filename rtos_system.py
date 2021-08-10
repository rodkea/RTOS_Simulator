class Rate_Monotonic():

    def __init__(self, tasks : list , ticks : int) -> None:
        self._ticks = ticks
        self._tasks = tasks

    def utilization_factor(self) -> float:
        u = 0
        for task in self._tasks:
            u += task.ex_time / task.period
        return round(u, 15)

    def liu_layland(self) -> bool:
        n = len(self._tasks)
        test_condition = n * (2 ** (1/n) - 1)
        return self.utilization_factor() <= test_condition

    def bini(self) -> bool:
        u = 1
        for task in self._tasks:
            u *= (task.ex_time / task.period) + 1
        return u <= 2

    @property
    def ticks(self):
        return self._ticks    

    @ticks.setter
    def ticks(self, ticks):
        self._ticks = ticks


class Task():

    def __init__(self, ex_time : int, period : int, deadline : int, priority : int):
        self._ex_time = ex_time
        self._period = period
        self._deadline = deadline
        self._priority = priority

    @property
    def ex_time(self):
        return self._ex_time
    
    @ex_time.setter
    def ex_time(self, ex_time):
        self._ex_time = ex_time

    @property
    def period(self):
        return self._period
    
    @period.setter
    def period(self, period):
        self._period = period

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self, deadline):
        self._deadline = deadline

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, priority):
        self._priority = priority

    
    
if __name__ == '__main__':
    tasks = [Task(1,2,2,1), Task(1,3,3,2), Task(1,6,6,3)]    
    system = Rate_Monotonic(tasks, 10)
    tasks2 = [Task(1,3,3,1), Task(1,4,4,2), Task(1,6,6,3)]
    system2 = Rate_Monotonic(tasks2, 10)  
    print('FU: ',system.utilization_factor())
    print('Liu-Laylnad: ', system.liu_layland())
    print('Bini: ', system.bini())
    print('FU: ', system2.utilization_factor())
    print('Liu-Laylnad: ', system2.liu_layland())
    print('Bini: ', system2.bini())

