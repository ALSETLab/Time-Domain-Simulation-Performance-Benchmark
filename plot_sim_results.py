from modelicares import SimRes
import os
import matplotlib.pyplot as plt
import numpy as np

def plot_sim_results(solver, experiment, fig_name):

	if experiment == 'initialization':
		exp = 1
		b1 = "B2.V"
		b2 = "B4.V"
	elif experiment == 'line_opening':
		exp = 2
		b1 = "B2.V"
		b2 = "B4.V"
	elif experiment == 'bus_faults':
		exp = 3
		b1 = "B4.V"
		b2 = "B14.V"

	# Adjusting number of points
	if solver == 'dassl':
		n_points = 5000
	else:
		n_points = 240000

	current_wd = os.getcwd()

	# Directory of Dymola results
	if solver == 'trapezoid':
		solver_dym = 'Rkfix2'
	elif solver == 'rungekutta':
		solver_dym = 'Rkfix4'
	elif solver == 'euler':
		solver_dym = 'Euler'
	elif solver == 'dassl':
		solver_dym = 'dassl'

	# Directory of Dymola results
	simD_dir = os.path.join(current_wd, "WorkingDir/Dymola/{s}/{e}/OpenIPSL.IEEE14.IEEE_14_Buses_{e}_{s}.mat".format(s = solver_dym, e = exp))
	# Directory of OpenModelica results
	simOM_dir = os.path.join(current_wd, "WorkingDir/OpenModelica/{s}/OpenIPSL.IEEE14.IEEE_14_Buses_{e}_res.mat".format(s = solver, e = exp))

	# Creating object with Dymola results
	simD = SimRes(simD_dir)
	# Creating object with OpenModelica results
	simOM = SimRes(simOM_dir)

	fig, axes = plt.subplots(figsize = (12,10), nrows = 2, ncols = 2)
	fig.suptitle("Time-domain simulation results ({s} - {e})".format(s = solver, e = experiment), fontname = "Times New Roman", fontsize = 22)

	
	axes[0][0].plot(simD['Time'].values(), simD[b1].values(), label = 'Dymola', color = 'indigo')
	axes[0][0].legend()
	axes[0][0].plot(simOM['Time'].values(), simOM[b1].values(), label = 'OpenModelica', color = 'salmon')
	axes[0][0].legend(prop = {'size' : 14, 'family': "Times New Roman"}) 
	
	axes[0][1].plot(simD['Time'].values()[0:n_points], (1/n_points)*np.absolute((simD[b1].values()[0:n_points]- simOM[b1].values()[0:n_points])), label = 'NAE', color = 'peru')
	axes[0][1].legend(prop = {'size' : 14, 'family': "Times New Roman"})
	axes[0][1].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

	axes[1][0].plot(simD['Time'].values(), simD[b2].values(), label = 'Dymola', color = 'indigo')
	axes[1][0].plot(simOM['Time'].values(), simOM[b2].values(), label = 'OpenModelica', color = 'salmon')
	axes[1][0].legend(prop = {'size' : 14, 'family': "Times New Roman"})
	
	axes[1][1].plot(simD['Time'].values()[0:n_points], (1/n_points)*np.absolute((simD[b2].values()[0:n_points]- simOM[b1].values()[0:n_points])), label = 'NAE', color = 'peru')
	axes[1][1].legend(prop = {'size' : 14, 'family': "Times New Roman"})
	axes[1][1].ticklabel_format(style='sci', axis='y', scilimits=(0,0))

	for r in range(0,2):
	    for c in range(0,2):
	        axes[r][c].set_ylabel('Voltage [pu]', fontname = 'Times New Roman', fontsize = 16)
	        axes[r][c].set_xlabel('Time [s]', fontname = 'Times New Roman', fontsize = 16)      
	        for tick in axes[r][c].xaxis.get_major_ticks():
	            tick.label.set_fontsize(15)
	            tick.label.set_fontname("Times New Roman")
	        for tick in axes[r][c].yaxis.get_major_ticks():
	            tick.label.set_fontsize(15)
	            tick.label.set_fontname("Times New Roman")

	fig.tight_layout()
	fig.subplots_adjust(top = 0.92)

	# Saving figure
	fig.savefig('Figs/01_Tool_Result_Analysis/{}.png'.format(fig_name), dpi = 300)

	# Printing information about mean errors
	print("{r:=^32}".format(r=""))
	print("{r:^32}".format(r="{s} - {e}".format(s = solver, e = experiment)))
	print("{r:=^32}".format(r=""))

	MSED1B2 = (1/n_points)*np.sum((simD[b1].values()[0:n_points]- simOM[b1].values()[0:n_points])**2)
	MSED1B4 = (1/n_points)*np.sum((simD[b2].values()[0:n_points]- simOM[b2].values()[0:n_points])**2)
	MSED2 = (1/n_points)*np.absolute((simD[b1].values()[0:n_points]- simOM[b1].values()[0:n_points]))
	print('MSE {} ='.format(b1[0:2]), MSED1B2)
	print('MSE {} ='.format(b2[0:2]), MSED1B4)

	print("{r:=^32}".format(r=""))