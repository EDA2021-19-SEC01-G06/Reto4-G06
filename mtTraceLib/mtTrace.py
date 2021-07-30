from time import process_time
import tracemalloc

class mtTrace:
    """
    Permite hacer seguimiento de tiempo y memoria consumida
    Si self.trace_memory = False, no se hace seguimiento a la
    memoria (para mejorar los tiempos de ejecución)
    
    ...

    Attributes
    ----------
    __start_time : float, private
        time stamp en milisegundos del tiempo en
        el que inición el seguimiento
    __start_memory : Snapshot, private
        Snapshot de la memoria del momento en el
        que se inició el seguimiento o None si está descativado
        el seguimiento de memoria
    __stop_time : float, private
        time stamo en milisegundos del teimpo
        en el que se llamó al método stop()
    __stop_memory : Snapshot, private
        (private) Snapshot de la memoria en el momento en el
        que se llamó al método stop() o None si está desactivado
        el seguimiento de memoria
    trace_momory : bool
        True si está activado el seguimiento de memoria y False
        si está desactivado (True por defecto)
    last_trace : dict[str, float]
        Diccionario con tiempo y memoria del último seguimiento
        realizado o None si no se ha realizado ningún seguimiento
    """
    __start_time = None
    __start_memory = None
    __stop_time = None
    __stop_memory = None
    trace_memory = False
    last_trace = None

    def start(self):
        """
        Inicializa tracemalloc y las variables __start_time y __start_memory
        """
        self.__start_time = process_time()
        if self.trace_memory:
            self.__memory_init()
        else:
            self.__deltaMem = lambda: None
            self.__memory_init = lambda: None
            self.__memory_end = lambda: None
    

    def stop(self):
        """
        Devuelve el tiempo transcurrido desde que se inicializó
        la variable __start_time, y la memoria consumida desde
        que se inicializó la variable __start_memory

        Returns: dict -- Diccionario con llave time en donde se
        encuentra el tiempo transcurrido en segundos y con llave
        memory en donde se encuentra la memoria utilizada en Mb
        """
        self.__stop_time = process_time()
        self.__memory_end()
        delta_time = self.__stop_time - self.__start_time
        delta_memory = self.__deltaMem()
        self.last_trace = {
            "time": delta_time,
            "memory": delta_memory
        }

        return self.last_trace


    def __memory_init(self):
        tracemalloc.start()
        self.__start_memory = tracemalloc.take_snapshot()

    def __memory_end(self):
        self.__stop_memory = tracemalloc.take_snapshot()
        tracemalloc.stop()


    def __deltaMem(self):
        """
        Calcula la diferencia en memoria alocada del programa entre dos
        instantes de tiempo y devuelve el resultado en Mb
        """
        memory_diff = self.__stop_memory.compare_to(self.__start_memory, "filename")
        delta_memory = 0.0

        # suma de las diferencias en uso de memoria
        for stat in memory_diff:
            delta_memory = delta_memory + stat.size_diff
        # de Byte -> kByte
        delta_memory = delta_memory / (1024**2)
        return delta_memory
    

    def printTrace(self, processDesc: str = "Proceso en", trace = None) -> None:
        """
        Imprime el tiempo y la memoria que toma un proceso. Si trace no se especifica
        por parámetro, imprime la información almacenada en self.last_trace 

        Args:
            trace: dict -- diccionario con llave time de tiempo transcurrido y
            llave memory de memoria utilizada
            processDesc: str -- (Optional) descripción corta del proceso realizado
        """
        if trace is None:
            if self.last_trace is None:
                raise Exception("Last trace está vacío y no se pasó un Trace por parámetro")
            else:
                trace = self.last_trace
        
        time = str(round(trace["time"], 4)) + " segundos"
        if trace["memory"] is not None:
            memory = str(round(trace["memory"], 4)) + " Mb"
            print(processDesc, time, "-", memory)
        else:
            print(processDesc, time)


