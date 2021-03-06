import os
from pathlib import Path
from datetime import date
import process_data as pd
import graph_generator as gd

date = date.today().isoformat()

#Increasing/Decrease/Stagnint Boundries
R_LOWER_BOUND = 0.88
R_UPPER_BOUND = 1.12

def create_html(locality,n):
    location = locality.name

    cases_increase = pd.calculate_daily_increase(locality,pd.TOTAL_CASES,True)
    hospitalizations_increase = pd.calculate_daily_increase(locality,pd.TOTAL_HOSPITALIZATIONS, True)
    death_increase = pd.calculate_daily_increase(locality,pd.TOTAL_DEATHS, True)
    yesterday_cases_increase = pd.calculate_daily_increase(locality,pd.TOTAL_CASES,False)
    yesterday_hospitalizations_increase = pd.calculate_daily_increase(locality,pd.TOTAL_HOSPITALIZATIONS,False)
    yesterday_death_increase = pd.calculate_daily_increase(locality,pd.TOTAL_DEATHS,False)

    cases_n_moving_average = pd.return_n_day_moving_average(locality,pd.TOTAL_CASES,n,True,None)
    hospitalizations_n_moving_average = pd.return_n_day_moving_average(locality,pd.TOTAL_HOSPITALIZATIONS,n,True,None)
    deaths_n_moving_average = pd.return_n_day_moving_average(locality,pd.TOTAL_DEATHS,n,True,None)
    previous_cases_n_moving_average = pd.return_n_day_moving_average(locality,pd.TOTAL_CASES,n,False,None)
    previous_hospitalizations_n_moving_average = pd.return_n_day_moving_average(locality,pd.TOTAL_HOSPITALIZATIONS,n,False,None)
    previous_deaths_n_moving_average = pd.return_n_day_moving_average(locality,pd.TOTAL_DEATHS,n,False,None)

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

    n_case_updownsame = ''
    if cases_n_moving_average - previous_cases_n_moving_average > 0:
        n_case_updownsame = 'up'
    elif cases_n_moving_average - previous_cases_n_moving_average < 0:
        n_case_updownsame = 'down'
    else:
        n_case_updownsame = 'same'

    n_hosptialization_updownsame = ''
    if hospitalizations_n_moving_average - previous_hospitalizations_n_moving_average > 0:
        n_hosptialization_updownsame = 'up'
    elif hospitalizations_n_moving_average - previous_hospitalizations_n_moving_average < 0:
        n_hosptialization_updownsame = 'down'
    else:
        n_hosptialization_updownsame = 'same'

    n_death_updownsame = ''
    if deaths_n_moving_average- previous_deaths_n_moving_average > 0:
        n_death_updownsame = 'up'
    elif deaths_n_moving_average- previous_deaths_n_moving_average < 0:
        n_death_updownsame = 'down'
    else:
        n_death_updownsame = 'same'

    new_cases_r_value = pd.return_reproduction_rate(locality,pd.TOTAL_CASES,n)
    
    new_cases_increasing_decreasing_stagnint = ''
    if new_cases_r_value <= R_LOWER_BOUND:
        new_cases_increasing_decreasing_stagnint = 'decreasing'
    elif new_cases_r_value >= R_UPPER_BOUND:
        new_cases_increasing_decreasing_stagnint = 'increasing'
    else:
        new_cases_increasing_decreasing_stagnint = 'stable'

    val = pd.return_reproduction_rate(locality,pd.TOTAL_HOSPITALIZATIONS,n)
    new_hospitalizations_increasing_decreasing_stagnint = ''
    if val <= R_LOWER_BOUND:
        new_hospitalizations_increasing_decreasing_stagnint = 'decreasing'
    elif val >= R_UPPER_BOUND:
        new_hospitalizations_increasing_decreasing_stagnint = 'increasing'
    else:
        new_hospitalizations_increasing_decreasing_stagnint = 'stable'
    
    val = pd.return_reproduction_rate(locality,pd.TOTAL_DEATHS,n)
    new_deaths_increasing_decreasing_stagnint = ''
    if val <= R_LOWER_BOUND:
        new_deaths_increasing_decreasing_stagnint = 'decreasing'
    elif val >= R_UPPER_BOUND:
        new_deaths_increasing_decreasing_stagnint = 'increasing'
    else:
        new_deaths_increasing_decreasing_stagnint = 'stable'
    
    total_cases = pd.return_cumlative(locality,pd.TOTAL_CASES)
    total_hosptializations = pd.return_cumlative(locality,pd.TOTAL_HOSPITALIZATIONS)
    total_deaths = pd.return_cumlative(locality,pd.TOTAL_DEATHS)

    #make graphs
    gd.n_day_moving_average_vs_time(locality, pd.TOTAL_CASES,n)
    gd.n_day_moving_average_vs_time(locality, pd.TOTAL_HOSPITALIZATIONS,n)
    gd.n_day_moving_average_vs_time(locality,pd.TOTAL_DEATHS,n)
    gd.cumsum_vs_time(locality,pd.TOTAL_CASES)
    gd.cumsum_vs_time(locality,pd.TOTAL_HOSPITALIZATIONS)
    gd.cumsum_vs_time(locality,pd.TOTAL_DEATHS)

    data_dir = Path(str(os.path.dirname(__file__))+'/HTML')
    file_path = data_dir / f'{location}-{date}.html'
    f = open(file_path,'w')

    message = f"""
<!DOCTYPE html>
<html>

<head>
    <title>Covid-19 update for {date} in {location}</title>
</head>
<h1 align="center">Covid-19 update in {location} for {date}</h1>
<br>
<h2 align="center">Today's Data</h2>
<br>
<h3>New Cases: {cases_increase}</h3>
<ul>
    <li>
        <p>There were {cases_increase} new cases recorded which is
            {case_updownsame} from yesterday's count of {yesterday_cases_increase}</p>
    </li>
    <li>
        <p>The current {n} day moving average is {cases_n_moving_average} which is 
             {n_case_updownsame} from the previous {n} day moving average of {previous_cases_n_moving_average}
        </p>
    </li>
    <li>
        <p>R={new_cases_r_value} (This is an approximation of how many healthy people the average infected person will spread the virus to)</p>
    </li>
    <li>
        <p>New cases in {location} appear to be {new_cases_increasing_decreasing_stagnint}</p>
    </li>
</ul>
<p><sub>For visual reference look at the attachment "New Cases vs Time {location} {date}"</sub></p>

<h3>New Hospitalizations: {hospitalizations_increase}</h3>
<ul>
    <li>
        <p>There were {hospitalizations_increase} new hospitalizations recorded which is {hosptialization_updownsame}
            from yesterday's count of {yesterday_hospitalizations_increase}</p>
    </li>
    <li>
        <p>The current {n} day moving average is {hospitalizations_n_moving_average} which is {n_hosptialization_updownsame}
            from the previous {n} day moving average of {previous_hospitalizations_n_moving_average}
        </p>
    </li>
    <li>
        <p>New hospitalizations in {location} appear to be {new_hospitalizations_increasing_decreasing_stagnint}</p>
    </li>
</ul>
<p><sub>For visual reference look at the attachment "New Hospitalizations vs Time {location}  {date}"</sub></p>

<h3>New Deaths: {death_increase}</h3>
<ul>
    <li>
        <p>There were {death_increase} new deaths recorded which is {death_updownsame}
            from yesterday's count of {yesterday_death_increase}</p>
    </li>
    <li>
        <p>The current {n} day moving average is {deaths_n_moving_average} which is {n_death_updownsame}
            from the previous {n} day moving average of {previous_deaths_n_moving_average}
        </p>
    </li>
    <li>
        <p>New deaths in {location} appear to be {new_deaths_increasing_decreasing_stagnint}</p>
    </li>
</ul>
<p><sub>For visual reference look at the attachment "New Deaths vs Time {location}  {date}"</sub></p>
<br>
<br>
<h2 align="center">Cumulative Data</h2>
<h3>Total Cases: {total_cases}</h3>
<p><sub>For visual reference look at the attachment "Total Cases vs Time {location}  {date}"</sub></p>
<h3>Total Hospitalizations: {total_hosptializations}</h3>
<p><sub>For visual reference look at the attachment "Total Hospitalizations vs Time {location}  {date}"</sub></p>
<h3>Total Deaths: {total_deaths}</h3>
<p><sub>For visual reference look at the attachment "Total Deaths vs Time {location}  {date}"</sub></p>
<br>
<br>
<h4>Enjoy These Emails? Consider supporting me:</h4>
<a href="http://paypal.me/RobertOwens956" target="_blank">PayPal</a>
<br>
<a href="http://www.venmo.com/Robbie-Owens-2">Venmo</a>
<br>
<br>
<a href="http://www.virginia-novelvirus.com/unsubscribe">Unsubscribe</a>
</html>
    """

    f.write(message)
    f.close()
