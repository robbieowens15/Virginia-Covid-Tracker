import os
from pathlib import Path
from datetime import date
import process_data as pd
import graph_generator as gd

date = date.today().isoformat()

def create_html(locality):
    location = locality.name
    cases_increase = pd.calculate_daily_increase(locality,pd.TOTAL_CASES)
    hospitalizations_increase = pd.calculate_daily_increase(locality,pd.TOTAL_HOSPITALIZATIONS)
    death_increase = pd.calculate_daily_increase(locality,pd.TOTAL_DEATHS)
    yesterday_cases_increase = pd.calculate_yesterday_daily_increase(locality,pd.TOTAL_CASES)
    yesterday_hospitalizations_increase = pd.calculate_yesterday_daily_increase(locality,pd.TOTAL_HOSPITALIZATIONS)
    yesterday_death_increase = pd.calculate_yesterday_daily_increase(locality,pd.TOTAL_DEATHS)

    case_updownsame = ''
    if cases_increase - yesterday_cases_increase > 0:
        case_updownsame = 'up'
    elif cases_increase - yesterday_cases_increase < 0:
        case_updownsame = 'down'
    else:
        case_updownsame = 'same'

    hosptialization_updownsame = ''
    if hospitalizations_increase - yesterday_hospitalizations_increase > 0:
        hosptialization_updownsame = 'up'
    elif hospitalizations_increase - yesterday_hospitalizations_increase < 0:
        hosptialization_updownsame = 'down'
    else:
        hosptialization_updownsame = 'same'

    death_updownsame = ''
    if death_increase - yesterday_death_increase > 0:
        death_updownsame = 'up'
    elif death_increase - yesterday_death_increase < 0:
        death_updownsame = 'down'
    else:
        death_updownsame = 'same'

    n=7
    gd.n_day_moving_average_vs_time(locality, pd.TOTAL_CASES,n)
    gd.n_day_moving_average_vs_time(locality, pd.TOTAL_HOSPITALIZATIONS,n)
    gd.n_day_moving_average_vs_time(locality,pd.TOTAL_DEATHS,n)


    new_cases_graph_path = f'images/{location}-{n}daymoving{pd.TOTAL_CASES}-{date}.jpg'
    new_hospitalizations_graph_path = f'images/{location}-{n}daymoving{pd.TOTAL_HOSPITALIZATIONS}-{date}.jpg'
    new_deaths_graph_path = f'images/{location}-{n}daymoving{pd.TOTAL_DEATHS}-{date}.jpg'

    data_dir = Path(str(os.path.dirname(__file__))+'/HTML')
    file_path = data_dir / f'{location}-{date}.html'
    f = open(file_path,'w')

    message = f"""
    <!DOCTYPE html>
    <html>
        <h1 align="center">This is your Covid-19 update for {location}: {date}</h1>
        <table align="center" style="width:80%">
            <tr>
                <td>
                    <h2 align="center">New Cases: {cases_increase}</h2>
                    <p>There were {cases_increase} new cases recorded as of yesterday which is {case_updownsame}
                        from yesterday's count of {yesterday_cases_increase}
                        <br>
                    </p>
                    <h4>Look at the {n} day moving average for new cases in {location}:</h4>
                    <img src="{new_cases_graph_path}" alt= "New Cases vs Time for {date}">
                    <p>New Cases in {location} is appeare to be DECLINE/STAGNINT/INCREASING</p>
                </td>
                <td>
                    <h2 align="center">New Hospitalizations: {hospitalizations_increase}</h2>
                    <p>There were {hospitalizations_increase} new Hospitalizations recorded as of yesterday which is {hosptialization_updownsame}
                        from yesterday's count of {yesterday_hospitalizations_increase}
                        <br>
                    </p>
                    <h4>Look at the {n} day moving average for new Hospitalizations in {location}:</h4>
                    <img src="{new_hospitalizations_graph_path}"alt= "New Hosiptalizations vs Time for {date}">
                    <p>New Deaths in {location} is appeare to be DECLINE/STAGNINT/INCREASING</p>
                </td>
                <td>
                    <h2 align="center">New Deaths: {death_increase}</h2>
                    <p>There were {death_increase} new Deaths recorded as of yesterday which is {death_updownsame}
                        from yesterday's count of {yesterday_death_increase}
                        <br>
                    </p>
                    <h4>Look at the {n} day moving average for new Deaths in {location}:</h4>
                    <img src="{new_deaths_graph_path}"alt= "New Hosiptalizations vs Time for {date}">
                    <p>New Deaths in {location} is appeare to be DECLINE/STAGNINT/INCREASING</p>
                </td>
            </tr>
        </table>
    </html>
    """

    f.write(message)
    f.close()

create_html(pd.tracking_loalities[2])