# INITIALIZATION
# Importing necessary packages
import pandas as pd
import datetime

# Creating permanent dataframes for raw data analysis (temperature, heart rate, & indicators)
dftemp = pd.DataFrame(columns = ['Temperature'])                                # permanent temperature dataframe (stores every temperature reading)
dfhr = pd.DataFrame(columns = ['Heart Rate'])                                   # permanent heart rate dataframe (stores every heart rate reading)
dfi = pd.DataFrame(columns = ['Night of:', 'Basal Body Temperature',            # permanent indicator dataframe (stores 1 value of BBT, avg HR, and recent HR for each night)
    'Average Heart Rate', 'Most Recent Heart Rate'])

# Creating pandas dataframes to be used for fertility window prediction
df_menses_start = pd.DataFrame(columns = ['Menses Start Dates'])                # Keeps track of past menses start dates (user input)
df_past_pred_ovu = pd.DataFrame(columns = ['Predicted Ovulation Dates'])        # Keeps track of past predicted ovulation dates
df_pred_menses_date = pd.DateFrame(columns = ['Next Predicted Menses Date'])    # Keeps track of the next predicted menses date
df_pred_ovulation = pd.DataFrame(columns = ['Next Predicted Ovulation Date',    # Keeps track of next predicted ovulation date and fertile window
    'Next Predicted Fertile Window'])

# Setting import counter only the first time the script is run
impcount = 0

# Find Today's Date in case user does not input menses information when they log in for the first time
firstmd_false = datetime.datetime.now().date()
