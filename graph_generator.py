import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import process_data as processed_data
from scipy.interpolate import make_interp_spline, BSpline

def cumsum_vs_time(locality_obj, tag):
    y = []
    x = []
    for i in range(len(locality_obj.data_list)-1):
        y.insert(0, int(locality_obj.data_list[i][tag]))
        x.insert(0, locality_obj.data_list[i][processed_data.DATE])
    x.reverse()
    y.reverse()

    fig, ax = plt.subplots()

    plt.grid(color='black',linewidth=0.25,alpha=0.75)
    ax.plot(x,y, linewidth=4)
    ax.scatter(x,y,alpha=0.6,edgecolors='face')
    xlabels = []
    xticks = []
    for i in range(len(x)):
        if(i%10 == 0):
            xlabels.insert(0,x[i])
            xticks.insert(0,i)
       
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels)
    plt.xticks(rotation=30)

    plt.ylabel(tag)
    plt.title(f'Cummulative {tag} in '+locality_obj.name)

    plt.show()

cumsum_vs_time(processed_data.tracking_loalities[2],processed_data.TOTAL_DEATHS)