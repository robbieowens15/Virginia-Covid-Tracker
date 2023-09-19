Virginia-Covid-Tracker
--
**Purpose:** To better inform citizens of the Commonwealth of Virginia with the most up to date covid statistics for their city or county

### Tech Stack
*Data Collection, Visualization, and Distribution*

- Obtain Data from Virginia Department of Health over HTTP Endpoint: `/csv_obtainer.py`
- Process Data to graphics for Daily new infections, hospitalizations, and deaths as well as 1 week rolling averages: `/process_data.py` & `graph_generator.py`
- Create an HTML email to communicate daily updates with graphics for each locality each user has enrolled to receive notifications on `covid_emailer_driver.py` & `email_sender.py` & `html_generator.py`

*Notification Enrollment*
- Lightweight flask webserver (`/flask_email_signup/*`) deployed to AWS Lightsail for user enrollment for daily notifications for a specific locality
- Storage of users' locality enrollment in SQL Lite Database `/flask_email_signup/site.db`
# Sample Email
### **HTML Message**

![](img/sample_email.jpeg?raw=true)

### **Graphics of Statistics**

![](img/New_Cases_vs_Time_Charlottesville_2021-07-01.jpeg?raw=true)
![](img/New_Hospitalizations_vs_Time_Charlottesville_2021-07-01.jpeg?raw=true)
![](img/New_Deaths_vs_Time_Charlottesville_2021-07-01.jpeg?raw=true)