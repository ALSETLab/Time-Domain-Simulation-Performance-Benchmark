import time
import psutil

# Function to measure execution performance
def measure_performance(perf_metrics, multiple_CPU = False, interval = 1):
    '''
    Description:
    
    This function writes on a dictionary information related to the CPU performance. Information is processed
    by default every second.
    
    Arguments:
    
    - perf_metrics: dictionary to which performance data will be written. It is recommended to create this dictionary 
    as a global variable
    - multiple_CPU: boolean that indicates whether the CPU usage is measured for a single core or for all cores. It defaults to False
    - interval: time between performance writings in the corresponding container. It defaults to 1 s.
    
    '''
    # CPU utilization, either single CPU or per CPU
    perf_metrics["cpu_use"].append(psutil.cpu_percent(percpu = multiple_CPU))
    # Virtual memory percentage
    perf_metrics["virtual_memory"].append(psutil.virtual_memory().percent)
    
    # CPU temperatures
    for item in psutil.sensors_temperatures()["coretemp"]:
        perf_metrics["temperature"][item.label].append(item.current)
    
    # Interruption to get measurements every specified time interval
    time.sleep(interval)
