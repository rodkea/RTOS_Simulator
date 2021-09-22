from math import ceil
from numpy import lcm
from nptyping import Int32

class Rate_Monotonic():

    def __init__(self, tasks : list = []) -> None: 
        '''
        Inicializa el sistema con el conjunto de tareas
        ingresadas como argumento y las ordenas segun su periodo.
        '''       
        self._tasks = sorted(tasks, key = lambda task: task.period)  # Ordena las prioridades segun Periodo.        

    def order_tasks(self):
        pass

    def add_task(self, task):
        '''
        Agrega una tarea al sistema.
        '''
        self._tasks.append(task) # Agrega la tarea
        self._tasks.sort(key = lambda task: task.period) # Reordena teniendo en cuenta la nueva tarea

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
        Devuelve True y una lista con los peores tiempos de respuesta de cada tarea 
        si es planificable, False de lo contrario.
        Si se especifica verbose = True imprime en pantalla el número de 
        iteraciones y funciones techo utilizadas.
        '''
        n_iteration = 0 # Contador de iteraciones
        ceil_count = 0  # Contador de funciones techo.
        response_time = [] # Tiempos de respuesta de las tareas        
        for n, task in enumerate(self.tasks):
            tq = 0 # Tiempo actual
            if n == 0:
                response_time.append(task.ex_time) # Tiempos de respuesta de las tareas
            else:
                while tq <= task.deadline: 
                    cumsum = 0 # Valor de las sumatorias con funciones techo
                    n_iteration += 1                 
                    for i in range(n):
                        ceil_count += 1
                        cumsum += ceil(tq / self.tasks[i].period) * self.tasks[i].ex_time                                    
                    if tq == task.ex_time + cumsum:
                        response_time.append(task.ex_time)                                                            
                        break
                    else:                    
                        tq = task.ex_time + cumsum
                if tq > task.deadline:
                    response_time = None
                    print('No es programable  Numero de iteraciones:')
                    return False, response_time
        if verbose:
            print('Número de iteraciones:', n_iteration)
            print('Numero de funciones techo:', ceil_count)
        return True, response_time

    def rta(self, verbose : bool=False) -> bool:
        '''
        Cálculo del Test de planificabilidad por RTA
        Imprime en pantalla el peor tiempo de respuesta de cada tarea. 
        Devuelve True y una lista con los peores tiempos de respuesta de cada tarea 
        si es planificable, False de lo contrario.
        Si se especifica verbose = True imprime en pantalla el número de 
        iteraciones y funciones techo utilizadas.
        '''
        n_iteration = 0 # Contador de iteraciones
        ceil_count = 0 #Contador de funciones techo
        tq = 0 # Tiempo actual
        response_time = [] # Tiempos de respuesta de las tareas         
        for n, task in enumerate(self.tasks):
            if n == 0:
                tq = task.ex_time
                response_time.append(tq)
            else:
                tq += task.ex_time
                while tq <= task.deadline:
                    cumsum = 0 # Valor de las sumatorias con funciones techo
                    n_iteration += 1                 
                    for i in range(n):
                        ceil_count += 1
                        cumsum += ceil(tq / self.tasks[i].period) * self.tasks[i].ex_time                                    
                    if tq == task.ex_time + cumsum:
                        response_time.append(tq)                                                           
                        break
                    else:                    
                        tq = task.ex_time + cumsum
                if tq > task.deadline:
                    print('No es programable')
                    responste_time = None
                    return False, responste_time
        if verbose:
            print('Número de iteraciones:', n_iteration)
            print('Numero de funciones techo:', ceil_count)
        return True, response_time

    def rta2(self, verbose : bool=False) -> bool:
        '''
        Cálculo del Test de planificabilidad por RTA 2
        Imprime en pantalla el peor tiempo de respuesta de cada tarea. 
        Devuelve True y una lista con los peores tiempos de respuesta de cada tarea 
        si es planificable, False de lo contrario.
        Si se especifica verbose = True imprime en pantalla el número de 
        iteraciones y funciones techo utilizadas.
        '''
        n_iteration = 0 # Contador de iteraciones
        ceil_count = 0 # Contador de funciones techo
        tq = 0 # Tiempo actual
        response_time = [] # Tiempos de respuesta de las tareas
        a_coeff = [task.ex_time for task in self.tasks] # Coeficientes Ai                               
        for n, task in enumerate(self.tasks):
            if n == 0:
                tq = task.ex_time
                response_time.append(tq)                
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
                        response_time.append(tq)                                                           
                        break
                    else:                    
                        tq = task.ex_time + cumsum
                if tq > task.deadline:
                    print('No es programable')
                    response_time = None
                    return False, response_time
        if verbose:
            print('Número de iteraciones:', n_iteration)
            print('Numero de funciones techo:', ceil_count) 
        return True, response_time

    def rta3(self, verbose : bool=False) -> bool:
        '''
        Cálculo del Test de planificabilidad por RTA 3
        Imprime en pantalla el peor tiempo de respuesta de cada tarea. 
        Devuelve True y una lista con los peores tiempos de respuesta de cada tarea 
        si es planificable, False de lo contrario.
        Si se especifica verbose = True imprime en pantalla el número de 
        iteraciones y funciones techo utilizadas.
        '''
        n_iteration = 0 # Contador de iteraciones        
        ceil_count = 0 # Contador de funciones techo
        tq = 0 # Tiempo actaul
        response_time = []
        a_coeff = [task.ex_time for task in self.tasks] # Coeficientes Ai                         
        for n, task in enumerate(self.tasks):            
            t_valid = [-1 for task in self.tasks] # Periodos de valides (inicialización -1)                        
            if n == 0:
                tq = task.ex_time
                print('PF:',task.ex_time)
                response_time.append(tq)
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
                        response_time.append(tq)                                                            
                        break
                    else:                    
                        tq = task.ex_time + cumsum
                if tq > task.deadline:
                    print('No es programable')
                    response_time = None
                    return False, response_time
        if verbose:
            print('Número de iteraciones:', n_iteration)
            print('Numero de funciones techo:', ceil_count)
        return True, response_time

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

    def find_ki(self, verbose : str = False) -> int:
        '''
        Devuelve los ki (inversiones) de las tareas del sistema.
        Si Verbose = True imprime el k de cada tarea
        '''
        ki = [] # Lista de los Ki de cada tarea
        for n, task in enumerate(self.tasks):
            tq = 0 # Tiempo actual            
            k = 1 # Inicio con k = 1            
            while tq <= task.deadline: # Mientras sea menor o igual que el vencimiento de la tarea
                cumsum = 0 # Suma de cargas de trabajo                
                for i in range(n):
                    cumsum += ceil(tq / self.tasks[i].period) * self.tasks[i].ex_time
                if tq == k + task.ex_time + cumsum: # Si encuentro punto fijo
                    k += 1 # Incremento k
                    tq = 0 # Reinicio el contador temporal                    
                else: # Si no hay punto fijo 
                    tq = k + task.ex_time + cumsum # Incremento el tiempo
            ki.append(k - 1) # Agrego el k de la tarea
        if verbose:
            for n, k in enumerate(ki, start= 1):
                print(f'K de la Tarea {n} = {k}')
        return ki
            
    def server_capacity(self) -> list:
        '''
        Devuelve una lista con las capacidades y 
        los periodos para Polling Server y Deferrable Server.
        '''
        ki = self.find_ki()
        capacitys = []
        for n, task in enumerate(self.tasks):
            c = []
            for i in range(n, len(self.tasks)):
                c.append(ki[i] / ceil(self.tasks[i].period / task.period))
            capacitys.append((min(c), task.period))
        
        return capacitys   
    
    def deferrable_server_bound(self):
        '''
        Devuelve una lista con las capacidades y 
        los periodos para Deferrable Server por el metodo de la cota.
        '''
        u = self.utilization_factor()
        n = len(self.tasks)
        bound = (2 - (((u / n) + 1) ** n )) / (2 * (((u / n) + 1) ** n) - 1)
        if bound > 0:        
            server_capacity = [(bound * task.period, task.period) for task in self.tasks]
            return server_capacity
        else:
            return None

    def polling_server_bound(self):
        '''
        Devuelve una lista con las capacidades y 
        los periodos para Polling Server por el metodo de la cota.
        '''
        u = self.utilization_factor()
        n = len(self.tasks)
        bound = (n + 1) * ((2) ** (1 / (n + 1)) - 1) - u
        if bound > 0:
            server_capacity = [(bound * task.period, task.period) for task in self.tasks]
            return server_capacity
        else:
            return None

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
    
class Aperiodic_Task():
    def __init__(self, call_time , ex_time : int):
        self._call_time = call_time # Tiempo de llamada
        self._ex_time = ex_time # Tiempo de ejecución

if __name__ == '__main__':
    TP = 2
    # TP1
    if TP == 1:         
        ex_tasks = [[Task(1,3,3), Task(1,4,4), Task(1,6,6)],
                    [Task(2,4,4), Task(1,5,5), Task(1,8,8)],
                    [Task(1,4,4), Task(1,5,5), Task(2,7,7), Task(1,12,12)],
                    [Task(1,5,5), Task(1,7,7), Task(2,10,10), Task(2,17,17)],
                    [Task(2,5,5), Task(1,8,8), Task(2,10,10), Task(3,17,17), Task(5,25,25)],
                    [Task(1,5,5), Task(1,6,6), Task(1,7,7), Task(2,11,11), Task(2,30,30)]                
                    ]
        for n, tasks in enumerate(ex_tasks, start= 1):
            print(f'Ejercicio {n}'.center(30,'-'))  
            system = Rate_Monotonic(tasks)
            print()
            print('Hiperperíodo:', system.hyperperiod())            
            print('Factor de utilización:', system.utilization_factor())            
            print('Cota de Liu:', system.liu_layland()[1])            
            print('Cota de Bini:', system.bini()[1])    
            print()
            _, ri = system.rta2(verbose=True)
            if ri != None:
                for i, r in enumerate(ri, start=1):
                    print(f'Tarea {i} -> Ri = {r}')
    elif TP == 2:
        ex_tasks = [[Task(1,3,3), Task(1,4,4), Task(1,6,6)],
                    [Task(2,4,4), Task(1,5,5), Task(1,8,8)],
                    [Task(1,5,5), Task(1,8,8), Task(2,10,10), Task(2,15,15), Task(2,20,20)],
                    [Task(1,8,8), Task(2,10,10), Task(2,13,13), Task(2,16,16), Task(3,25,25)]
                   ]
        for n, tasks in enumerate(ex_tasks):
            print(f'Ejercicio {n+1}'.center(30,'-'))
            print() 
            system = Rate_Monotonic(tasks)            
            print()            
            capacidades = system.polling_server_bound()
            if capacidades != None:
                print(f'Capacidad / Periodo por metodo de la cota Polling Server = {capacidades}')                            
            else:
                print(f'No se puede aplicar la cota para Polling Server')
            capacidades = system.deferrable_server_bound()
            if capacidades != None:
                print(f'Capacidad / Periodo por metodo de la cota Deferrable Server = {capacidades}')
            else:
                print(f'No se puede aplicar la cota para Deferrable Server')
            capacidades = system.server_capacity()
            print(f'Capacidad / Periodo por metodo de los ki = {capacidades}')
            print()
            system.rta2()
            print()
    
        

                
        

