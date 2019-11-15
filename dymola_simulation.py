import os
import platform
import time
from dymola.dymola_interface import DymolaInterface
from dymola.dymola_exception import DymolaException

def dymola_simulation(model_info, path_dymola, solver, printInfo = True):
    '''
    
    '''
    # Retrieving model information
    root_path = model_info['root_path']
    library_path = model_info['library_path']
    model_path = model_info['model_path']
    model_name = model_info['model_name']
    output_path = model_info['output_path']
    
    dymola = None   
    
    try:
        if printInfo:
            print("Creating and starting Dymola instance")
          
        # Creating dymola instance
        dymola = DymolaInterface(dymolapath = path_dymola)
        
        if printInfo:
            print(f"Using Dymola port:" + str(dymola._portnumber))
            print(f"Changing working directory to: {output_path}")
        
        try:
            if not os.path.exists(output_path):
                os.makedirs(output_path)
                print("Working directory created")
        except OSError as ex:
            print("1: Failed to create folder for working directory")
        
        # CHANGING THE PATH TO OPENING THE LIBRARY AND THE MODEL        
        result = dymola.cd(root_path)
        if not result:
            print("1: Failed to change working directory")
        
        # Opening OpenIPSL library
        dymola.openModel(library_path)
        if result and printInfo:
            print("Library opened")
        
        # Opening model
        dymola.openModel(model_path)
        if result and printInfo:
            print("Model opened")
            
        # CHANGING THE PATH FOR THE WORKING DIRECTORY
        # Note that the model is already opened
        result = dymola.cd(output_path)
        if not result:
            print("1: Failed to change working directory")
        
        # Simulating the model
        if solver == 'dassl':
            dymola.Execute("Advanced.Define.DAEsolver = true")
            print("DAE setting changed for dassl")
        
        if solver in ["Rkfix2", "Rkfix4", "Euler"]:
            print("Running simulation...")
            result = dymola.simulateModel(model_name, method = solver, stopTime=120, numberOfIntervals=240000, tolerance=1e-06, resultFile = model_name + "_{}".format(solver))
        else:
            # Settings for dassl
            print("Running simulation...")
            result = dymola.simulateModel(model_name, method = solver, stopTime=120, numberOfIntervals=5000, tolerance=1e-06, resultFile = model_name + "_{}".format(solver))

        if not result:
            print("Simulation failed. Below is the error log:")
            log = dymola.getLastErrorLog()
            print(log)
        else:
            print("Simulation OK")
            # Close Dymola
            dymola.close()

    except DymolaException as ex:
        if printInfo:
            print(("Error: " + str(ex)))
        else:
            pass
    finally:
        if dymola is not None:
            dymola.close()
            dymola = None   
    