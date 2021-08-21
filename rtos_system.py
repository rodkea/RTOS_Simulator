from math import ceil
from numpy import lcm

class Rate_Monotonic():

    def __init__(self, tasks : list = []) -> None:        
        self._tasks = tasks

    def add_task(self, task):
        self._tasks.append(task)

    def utilization_factor(self) -> float:
        u = 0
        for task in self._tasks:
            u += task.ex_time / task.period
        return round(u, 15)

    def liu_layland(self) -> list:        
        n = len(self._tasks)
        test_condition = n * (2 ** (1/n) - 1)
        return [self.utilization_factor() <= test_condition, test_condition]

    def bini(self) -> list:
        u = 1
        for task in self._tasks:
            u *= (task.ex_time / task.period) + 1
        return [u <= 2, u]

    def joshep_pandya(self, verbose : bool=False) -> bool:
        n_iteration = 0        
        for n, task in enumerate(self._tasks):
            tq = 0
            ceil_count = 0            
            print('Task:',n+1)
            if n == 0:
                print('PF:',task._ex_time)
            else:
                while tq <= task._deadline:
                    cumsum = 0
                    n_iteration += 1                 
                    for i in range(n):
                        ceil_count += 1
                        cumsum += ceil(tq / self._tasks[i].period) * self._tasks[i].ex_time                                    
                    if tq == task.ex_time + cumsum:
                        print('PF:',tq)                                                            
                        break
                    else:                    
                        tq = task.ex_time + cumsum
                if tq > task._deadline:
                    print('No es programable  Numero de iteraciones:')
        if verbose:
            print('Número de iteraciones:', n_iteration)
            print('Numero de funciones techo:', ceil_count)

    def rta(self, verbose : bool=False) -> bool:
        n_iteration = 0
        tq = 0
        ceil_count = 0        
        for n, task in enumerate(self._tasks):                        
            print('Task:',n+1)
            if n == 0:
                tq = task._ex_time
                print('PF:',task.ex_time)
            else:
                tq += task._ex_time
                while tq <= task.deadline:
                    cumsum = 0
                    n_iteration += 1                 
                    for i in range(n):
                        ceil_count += 1
                        cumsum += ceil(tq / self._tasks[i].period) * self._tasks[i].ex_time                                    
                    if tq == task.ex_time + cumsum:
                        print('PF:',tq)                                                            
                        break
                    else:                    
                        tq = task.ex_time + cumsum
                if tq > task.deadline:
                    print('No es programable')
        if verbose:
            print('Número de iteraciones:', n_iteration)
            print('Numero de funciones techo:', ceil_count)

    def hyperperiod(self):
        return lcm.reduce([x.period for x in self._tasks])


    @property
    def ticks(self):
        return self._ticks    

    @ticks.setter
    def ticks(self, ticks):
        self._ticks = ticks


class Task():

    def __init__(self, ex_time : int, period : int, deadline : int):
        self._ex_time = ex_time
        self._period = period
        self._deadline = deadline        

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
    
    
if __name__ == '__main__':    
    ex_tasks = [[Task(1,3,3), Task(1,4,4), Task(1,6,6)],
                [Task(2,4,4), Task(1,5,5), Task(1,8,8)],
                [Task(1,4,4), Task(1,5,5), Task(2,7,7), Task(1,12,12)],
                [Task(1,5,5), Task(1,7,7), Task(2,10,10), Task(2,17,17)],
                [Task(2,5,5), Task(1,8,8), Task(2,10,10), Task(3,17,17), Task(5,25,25)],
                [Task(1,5,5), Task(1,6,6), Task(1,7,7), Task(2,11,11), Task(2,30,30)]                
                ]
    for n, tasks in enumerate(ex_tasks):
        print(f'Ejercicio {n+1}'.center(30,'-'))  
        system = Rate_Monotonic(tasks)
        print('Hiperperíodo:', system.hyperperiod())
        print('Factor de utilización:', system.utilization_factor())
        print('Cota de Liu:', system.liu_layland()[1])
        print('Cota de Bini:', system.bini()[1])    
        system.rta(verbose=True)
        

