import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_temperature(df_temperature, tool, experiment, solver, sensor, fig_name):

    if sensor == 'Physical id 0':
        sensor_name = 'Analog'
    else:
        sensor_name = sensor

    fig, axes = plt.subplots(figsize = (7, 5))
    fig.suptitle("Temperature ({t}, {e} - {s} - {a})".format(t = tool, e = experiment, s = solver, a = sensor_name), fontname = "Times New Roman", fontsize = 22)

    # Computing moving average
    if solver == 'dassl':
        moving_average = df_temperature[tool][experiment][solver][sensor].rolling(window = 10).mean()
    else:
        moving_average = df_temperature[tool][experiment][solver][sensor].rolling(window = 100).mean()
 
    # Time vector
    t_sim = df_temperature[tool][experiment][solver]["Time"]
    # Plot
    axes.plot(t_sim, moving_average, color = '#4199CB')
    
    # Computing and printing the average

    average = df_temperature[tool][experiment][solver][sensor].mean()
    axes.axhline(y = average, color = '#FFB529', linestyle = '--')

    # Formatting title and axes labels
    axes.set_title("{} Sensor".format(sensor_name), fontname = "Times New Roman", fontsize = 18)
    axes.set_xlabel("Time (s)", fontname = "Times New Roman", fontsize = 18)
    axes.set_ylabel("Temperature (°C)", fontname = "Times New Roman", fontsize = 18)

    for tick in axes.get_xticklabels():
        tick.set_fontname("Times New Roman")
        tick.set_fontsize(15)

    for tick in axes.get_yticklabels():
        tick.set_fontname("Times New Roman")
        tick.set_fontsize(15)

    fig.tight_layout()
    fig.subplots_adjust(top = 0.87)

    fig.savefig('Figs/03_Temperature/{}.png'.format(fig_name), dpi = 300)
    
    fig, axes = None, None