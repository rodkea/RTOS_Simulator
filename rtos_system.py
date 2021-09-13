from math import ceil
from numpy import lcm
from nptyping import Int32

class Rate_Monotonic():

    def __init__(self, tasks : list = []) -> None: 
        '''
        Inicializa el sistema con el conjunto de tareas
        ingresadas como argumento
        '''       
        self._tasks = tasks

    def add_task(self, task):
        '''
        Agrega tareas al sistema
        '''
        self._tasks.append(task)

    def hyperperiod(self) -> Int32:
        '''
        Calcula el hiperperiodo del sistema buscando
        el mínimo común múltiplo entre todos los períodos
        de las tareas del sistema.
        '''
        return lcm.reduce([x.period for x in self.tasks])

    def utilization_factor(self) -> float:
        '''
        Calcula el factor de utilización del sistema.
        '''        
        u = 0 # Factor de utilización
        for task in self.tasks:
            u += task.ex_time / task.period # Ci / Ti
        return round(u, 15) # Redonde para mejorar visualización

    def liu_layland(self) -> list: 
        '''
        Cálculo de la cota de Liu-Layland para el sistema. Devuelve una lista de dos elementos
        el primer elemento True si cumple la cota, False de lo contrario. El segundo elemento devuelve
        el valor numerico resultante del calculo de la cota.
        '''               
        n = len(self.tasks) # Número de tareas
        test_condition = n * (2 ** (1/n) - 1) # Cálculo de la cota
        return [self.utilization_factor() <= test_condition, test_condition] # (Condición de la cota, cálculo)

    def bini(self) -> list:
        '''
        Cálculo de la cota de Bini para el sistema. Devuelve una lista de dos elementos
        el primer elemento True si cumple la cota, False de lo contrario. El segundo elemento devuelve
        el valor numerico resultante del calculo de la cota.               
        '''        
        u = 1 # Inicializo con 1 para la productoria
        for task in self.tasks:
            u *= (task.ex_time / task.period) + 1 
        return [u <= 2, u] 

    def joshep_pandya(self, verbose : bool=False) -> bool:
        '''
        Cálculo del Test de planificabilidad de M. Joseph y P. Pandya.
        Imprime en pantalla el peor tiempo de respuesta de cada tarea. 
        Devuelve True si es planificable, False de lo contrario.
        Si se especifica verbose = True imprime en pantalla el número de 
        iteraciones y funciones techo utilizadas.
        '''
        n_iteration = 0 # Contador de iteraciones
        ceil_count = 0  # Contador de funciones techo.       
        for n, task in enumerate(self.tasks):
            tq = 0 # Tiempo actual            
            print('Task:',n+1) 
            if n == 0:
                print('PF:',task.ex_time)
            else:
                while tq <= task.deadline: 
                    cumsum = 0 # Valor de las sumatorias con funciones techo
                    n_iteration += 1                 
                    for i in range(n):
                        ceil_count += 1
                        cumsum += ceil(tq / self.tasks[i].period) * self.tasks[i].ex_time                                    
                    if tq == task.ex_time + cumsum:
                        print('PF:',tq)                                                            
                        break
                    else:                    
                        tq = task.ex_time + cumsum
                if tq > task.deadline:
                    print('No es programable  Numero de iteraciones:')
                    return False
        if verbose:
            print('Número de iteraciones:', n_iteration)
            print('Numero de funciones techo:', ceil_count)
        return True

    def rta(self, verbose : bool=False) -> bool:
        '''
        Cálculo del Test de planificabilidad por RTA
        Imprime en pantalla el peor tiempo de respuesta de cada tarea. 
        Devuelve True si es planificable, False de lo contrario.
        Si se especifica verbose = True imprime en pantalla el número de 
        iteraciones y funciones techo utilizadas.
        '''
        n_iteration = 0 # Contador de iteraciones
        ceil_count = 0 #Contador de funciones techo
        tq = 0 # Tiempo actual
                 
        for n, task in enumerate(self.tasks):                        
            print('Task:',n+1)
            if n == 0:
                tq = task.ex_time
                print('PF:',task.ex_time)
            else:
                tq += task.ex_time
                while tq <= task.deadline:
                    cumsum = 0 # Valor de las sumatorias con funciones techo
                    n_iteration += 1                 
                    for i in range(n):
                        ceil_count += 1
                        cumsum += ceil(tq / self.tasks[i].period) * self.tasks[i].ex_time                                    
                    if tq == task.ex_time + cumsum:
                        print('PF:',tq)                                                            
                        break
                    else:                    
                        tq = task.ex_time + cumsum
                if tq > task.deadline:
                    print('No es programable')
                    return False
        if verbose:
            print('Número de iteraciones:', n_iteration)
            print('Numero de funciones techo:', ceil_count)
        return True

    def rta2(self, verbose : bool=False) -> bool:
        '''
        Cálculo del Test de planificabilidad por RTA 2
        Imprime en pantalla el peor tiempo de respuesta de cada tarea. 
        Devuelve True si es planificable, False de lo contrario.
        Si se especifica verbose = True imprime en pantalla el número de 
        iteraciones y funciones techo utilizadas.
        '''
        n_iteration = 0 # Contador de iteraciones
        ceil_count = 0 # Contador de funciones techo
        tq = 0 # Tiempo actual
        a_coeff = [task.ex_time for task in self.tasks] # Coeficientes Ai                               
        for n, task in enumerate(self.tasks):
                                    
            print('Task:',n+1)
            if n == 0:
                tq = task.ex_time
                print('PF:',task.ex_time)
            else:
                tq += task.ex_time
                while tq <= task.deadline:
                    cumsum = 0 # Valor de las sumatorias con funciones techo
                    n_iteration += 1                 
                    for i in range(n):
                        ceil_count += 1
                        a = ceil(tq / self.tasks[i].period) * self.tasks[i].ex_time
                        cumsum += a
                        if a_coeff[i] < a:                             
                            a_coeff[i] = a                            
                            tq += a - a_coeff[n]                                    
                    if tq == task.ex_time + cumsum:                        
                        print('PF:',tq)                                                            
                        break
                    else:                    
                        tq = task.ex_time + cumsum
                if tq > task.deadline:
                    print('No es programable')
                    return False
        if verbose:
            print('Número de iteraciones:', n_iteration)
            print('Numero de funciones techo:', ceil_count) 
        return True

    def rta3(self, verbose : bool=False) -> bool:
        '''
        Cálculo del Test de planificabilidad por RTA 3
        Imprime en pantalla el peor tiempo de respuesta de cada tarea. 
        Devuelve True si es planificable, False de lo contrario.
        Si se especifica verbose = True imprime en pantalla el número de 
        iteraciones y funciones techo utilizadas.
        '''
        n_iteration = 0 # Contador de iteraciones        
        ceil_count = 0 # Contador de funciones techo
        tq = 0 # Tiempo actaul
        a_coeff = [task.ex_time for task in self.tasks] # Coeficientes Ai                         
        for n, task in enumerate(self.tasks):            
            t_valid = [-1 for task in self.tasks] # Periodos de valides (inicialización -1)                        
            print('Task:',n+1)
            if n == 0:
                tq = task.ex_time
                print('PF:',task.ex_time)
            else:
                tq += task.ex_time
                while tq <= task.deadline:
                    cumsum = 0
                    n_iteration += 1                 
                    for i in range(n):
                        if tq > t_valid[i]:
                            ceil_count += 1
                            ceil_calc = ceil(tq / self.tasks[i].period)
                            a =  ceil_calc * self.tasks[i].ex_time
                            cumsum += a
                            t_valid[i] = ceil_calc * self.tasks[i].period
                            if a_coeff[i] < a:                            
                                a_coeff[i] = a                            
                                tq += a - a_coeff[n] 
                        else:
                            cumsum += a_coeff[i]
                                                           
                    if tq == task.ex_time + cumsum:                        
                        print('PF:',tq)                                                            
                        break
                    else:                    
                        tq = task.ex_time + cumsum
                if tq > task.deadline:
                    print('No es programable')
                    return False
        if verbose:
            print('Número de iteraciones:', n_iteration)
            print('Numero de funciones techo:', ceil_count)
        return True

    def empty_slot(self, slot_size : int, verbose : bool = False) -> int:
        '''
        Devuelve el instante de tiempo donde se encuentra
        una ranura vacia de tamaño 'slot_size'.
        ''' 
        tq = slot_size # Tiempo actual       
        if self.utilization_factor() < 1: # Chequeo que el sistema no este saturado.
            while True:
                    cumsum = 0 # Valor de las sumatorias con funciones techo                                  
                    for task in self.tasks:                        
                        cumsum += ceil(tq / task.period) * task.ex_time                                    
                    if tq == slot_size + cumsum:                                                                                    
                        break
                    else:                    
                        tq = slot_size + cumsum
        return tq - slot_size # Instante de primera ranura vacia 

    def slack(self) -> int:
        '''
        Devuelve el slack disponible del sistema.
        '''
        work_load = 0 # Carga de trabajo
        hyperperiod = self.hyperperiod() 
        for task in self.tasks:
            work_load += (hyperperiod / task.period) * task.ex_time
        slack = hyperperiod - work_load
        return slack

    @property
    def tasks(self):
        return self._tasks    

class Task():

    def __init__(self, ex_time : int, period : int, deadline : int):
        self._ex_time = ex_time # Tiempo de ejecución
        self._period = period # Periodo
        self._deadline = deadline # Vencimiento        

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
    # TP1    
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
        system.rta2(verbose=True)
    system = Rate_Monotonic([Task(2,4,4), Task(1,5,5), Task(1,8,8)])
    print(system.slack())
        
        

