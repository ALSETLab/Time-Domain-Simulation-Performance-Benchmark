import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_cpu_usage(df_cpu, tool, experiment, solver, fig_name):

    fig, axes = plt.subplots(figsize = (10,10), nrows = 4, ncols = 3)
    fig.suptitle("CPU Utilization ({t}, {e} - {s})".format(t = tool, e = experiment, s = solver), fontname = "Times New Roman", fontsize = 22)

    num_core = 1

    for ax in axes.reshape(-1):

        # Computing moving average
        if solver == 'dassl':
            moving_average = df_cpu[tool][experiment][solver][num_core].rolling(window = 10).mean()
        else:
            moving_average = df_cpu[tool][experiment][solver][num_core].rolling(window = 100).mean()
    
        # Time vector
        t_sim = df_cpu[tool][experiment][solver]["Time"]
        # Plot
        ax.plot(t_sim, moving_average, color = '#4199CB')
        
        # Computing and printing the average

        average = df_cpu[tool][experiment][solver][num_core].mean()
        ax.axhline(y = average, color = '#FFB529', linestyle = '--')

        # Formatting title and axes labels
        ax.set_title("Core {}".format(num_core), fontname = "Times New Roman", fontsize = 18)
        ax.set_xlabel("Time (s)", fontname = "Times New Roman", fontsize = 18)
        ax.set_ylabel("Utilization (%)", fontname = "Times New Roman", fontsize = 18)

        num_core += 1

        for tick in ax.get_xticklabels():
            tick.set_fontname("Times New Roman")
            tick.set_fontsize(15)

        for tick in ax.get_yticklabels():
            tick.set_fontname("Times New Roman")
            tick.set_fontsize(15)

    fig.tight_layout()
    fig.subplots_adjust(top = 0.92)

    fig.savefig('Figs/02_CPU_Usage/{}.png'.format(fig_name), dpi = 300)
    
    fig, axes = None, None