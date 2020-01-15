from modelicares import SimRes
from OMPython import OMCSessionZMQ
import os
import time
import pickle
import copy
import multiprocessing as mp
from measurement_performance import*
from dymola_simulation import*
from om_simulation import*

if __name__ == "__main__":
    
    # Experiments
    experiments = ['initialization', 'line_opening', 'bus_faults']
    
    # Solver name in Dymola (first entry of the list) and OpenModelica (second entry)
    solvers = {'trapezoid' : ["Rkfix2", "trapezoid"],
        'rungekutta' : ["Rkfix4", "rungekutta"],
        'dassl' : ["dassl", "dassl"],
        'euler' : ["Euler", "euler"]}
    
    # Defining template for metrics storage
    metrics_template = {"execution_time" : 0,
           "cpu_use" : [],
           "virtual_memory" : [],
           "temperature": {"Package id 0": [],
                            "Core 0" : [],
                          "Core 1" : [],
                          "Core 2" : [],
                          "Core 3" : [],
                          "Core 4": [],
                          "Core 5": []}}
    # Path to Dymola              
    path_dymola = "/opt/dymola-2020x-x86_64/bin64/dymola.sh" # Path to Dymola in BabyGrid
    
    for n_exp, experiment in enumerate(experiments):       
        
        # Creating performance measurement dictionary (resetting the variable for each experiment)
        metrics = {'dassl': {'Dymola' : copy.deepcopy(metrics_template), 'OpenModelica': copy.deepcopy(metrics_template)},
            'euler' : {'Dymola' : copy.deepcopy(metrics_template), 'OpenModelica': copy.deepcopy(metrics_template)},
            'trapezoid' : {'Dymola' : copy.deepcopy(metrics_template), 'OpenModelica': copy.deepcopy(metrics_template)},
            'rungekutta' : {'Dymola' : copy.deepcopy(metrics_template), 'OpenModelica': copy.deepcopy(metrics_template)}}
        
        for solver in solvers:
            # Printing info about current solver
            print("=======================")
            print("CURRENT EXPERIMENT - SOLVER: {} - {}".format(experiment, solver))
            print("=======================\n")
            
            for n_tool, tool in enumerate(solvers[solver]):
                
                if n_tool == 0:
                    # Current tool: Dymola
                    tool_name = "Dymola"

                    model_info = {'root_path': os.getcwd(),
                    'library_path': "/OpenIPSL-1.5.0/OpenIPSL/package.mo",
                    'model_path': "/OpenIPSL-1.5.0/OpenIPSL/IEEE14/package.mo", #Path to the package.mo
                    'model_name': "OpenIPSL.IEEE14.IEEE_14_Buses_{}".format(n_exp + 1),
                    'output_path' : os.path.join(os.getcwd(), "WorkingDir/Dymola/{}/{}".format(solvers[solver][0], n_exp + 1))}

                    # Current solver
                    solver_name = solvers[solver][0]
                    
                    # Creating a pool of processes    
                    p = mp.Pool()
                    
                    # List of running processes
                    process = []

                    # Measurement of execution time per simulation
                    t = time.time()
                    apfun = p.apply_async(dymola_simulation,
                               args = (model_info, path_dymola, solvers[solver][0], True, ))
                    process.append(apfun)
                    p.close()
                    
                    # Registering data until all processes are completed
                    while not process[0].ready():
                        measure_performance(metrics[solver][tool_name], True, 0.2)
                        #print("Simulation is running (and performance is being measured...)")
        
                    # Closing pool of processes  
                    p.join()
                    print("All processes finished running")
                    process = None
                    p = None
                    
                    # Adding execution time to the measurements
                    metrics[solver][tool_name]["execution_time"] = time.time() - t
                    print("Execution time: {}".format(metrics[solver][tool_name]["execution_time"]))                    
                elif n_tool == 1:
                                       
                    tool_name = "OpenModelica"                    
                    

                    model_info = {'root_path': os.getcwd(),
                    'library_path': os.path.join(os.getcwd(), "OpenIPSL-1.5.0/OpenIPSL/package.mo"),
                    'model_path': os.path.join(os.getcwd(),"OpenIPSL-1.5.0/OpenIPSL/IEEE14/package.mo"),
                    'model_name': "OpenIPSL.IEEE14.IEEE_14_Buses_{}".format(n_exp + 1),
                    'output_path' : os.path.join(os.getcwd(), "WorkingDir/OpenModelica/{}/".format(solvers[solver][1], n_exp + 1))}

                    # Current solver
                    solver_name = solvers[solver][1]
                    
                    # Creating a pool of processes    
                    p = mp.Pool()
                    
                    # List of running processes
                    process = []

                    # Measurement of execution time per simulation
                    t = time.time()
                    apfun = p.apply_async(om_simulation,
                               args = (model_info, solver_name, ))
                    process.append(apfun)
                    p.close()
                    
                    # Registering data until all processes are completed
                    while not process[0].ready():
                        measure_performance(metrics[solver][tool_name], True, 0.2)
                        #print("Simulation is running (and performance is being measured...)")
        
                    # Closing pool of processes  
                    p.join()
                    print("All processes finished running\n")
                    
                    # Adding execution time to the measurements
                    metrics[solver][tool_name]["execution_time"] = time.time() - t
                    print("Execution time: {}".format(metrics[solver][tool_name]["execution_time"]))
                    
                print("Tool: {}\n".format(tool_name))
            #break     
        
        # Saving data from experiment
        with open("measurements_{}.pkl".format(experiment), 'wb') as f:
            pickle.dump(metrics, f, pickle.HIGHEST_PROTOCOL)
        del metrics