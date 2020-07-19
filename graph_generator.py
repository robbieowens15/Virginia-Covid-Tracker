import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import process_data as processed_data


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


    ax.plot(x,y, linewidth=3.5)
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

def n_day_moving_average_vs_time(locality_obj, tag, n):
    data = processed_data.calculate_moving_n_day_average_list(locality_obj, tag, n)
    y = []
    x = []
    for i in range(len(data)-n):
        y.insert(0, int(data[i]))
        x.insert(0, locality_obj.data_list[i+n][processed_data.DATE])
    x.reverse()
    y.reverse()

    fig, ax = plt.subplots()

    plt.grid(color='black',linewidth=0.25,alpha=0.75)


    ax.plot(x,y, linewidth=3.5)
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

    y_data_label = ''
    if tag == processed_data.TOTAL_CASES:
        y_data_label = 'New Cases'
    elif tag == processed_data.TOTAL_HOSPITALIZATIONS:
        y_data_label = 'New Hospitalizations'
    elif tag == processed_data.TOTAL_DEATHS:
        y_data_label = 'New Deaths'

    plt.ylabel(y_data_label)
    plt.title(f'{n} Day Moving Average for {y_data_label} in '+locality_obj.name)

    plt.show()

#cumsum_vs_time(processed_data.tracking_loalities[0],processed_data.TOTAL_CASES)
n_day_moving_average_vs_time(processed_data.tracking_loalities[2],processed_data.TOTAL_HOSPITALIZATIONS, 7)
