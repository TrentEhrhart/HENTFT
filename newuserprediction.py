def new_user_prediction():
    # This function outputs predictions for next menses date, ovulation date, and fertile window if the user has been on the app for less than 90 days
    import pandas as pd
    import datetime

    #loading in test dataset from excel: Real data would come into the backend via a .csv file (the same concepts would apply)
    df_menses_start = pd.read_excel (r'C:\Users\trent\Documents\BME 261L - Development & Analysis in BME Design\261L Python\newusermensesdates.xlsx')
    df_menses_start['Menses Start Dates'] = pd.to_datetime(df_menses_start['Menses Start Dates'])           # Convert Dates to Datetime format


    #Next Menses Date Prediction
    if len(df_menses_start.index.values) == 0:                                      # If the user never input menses information upon downloading the app
        lmd = firstmd_false                                                         # firstmd_false comes from the initilization of the app (represents the day the user first used the app)
    else:
        lmd = df_menses_start.iloc[-1]                                              # Finds the most recent menses start date
    nmd = lmd + datetime.timedelta(days = 28)                                       # Next menses date = last menses date + 28 days

    # Store predicted Menses date in prediction dataframe
    df_pred_menses_date = pd.DataFrame()                                            # Creating dataframe to store predicted menses date
    df_pred_menses_date['Next Predicted Menses Date'] = nmd                         # Storing the next predicted menses date


    # Next Ovulation Date Prediction
    nod = lmd + datetime.timedelta(days = 14)                                       # Next ovulation date = last menses date + 14 days

    # Store Ovulation Date Prediction
    df_pred_ovulation = pd.DataFrame()                                              # Creating Dataframe to store predicted ovulation date
    df_pred_ovulation['Next Predicted Ovulation Date'] = nod                        # Storing the next predicted ovulation date


    # Fertile Window Prediction
        # Fertile window is the three days leading up to ovulation and the ovulation date
    ffd = nod - datetime.timedelta(days = 3)
    sfd = nod - datetime.timedelta(days = 2)
    tfd = nod - datetime.timedelta(days = 1)

    # Store Fertile Window Prediction
    df_pred_fertile_window = pd.DataFrame() and                                     # Creating Dataframe to store predicted fertile window
    df_pred_fertile_window['Predicted Fertile Window'] = [ffd, sfd, tfd, nod]       # Storing next predicted fertile window


    # Write prediction dataframes to a .csv file for use in the application interface
    df_pred_menses_date.to_csv('predictedmensesdate.csv', columns = ['Next Predicted Menses Date'])
    df_pred_ovulation.to_csv('predictedovulation.csv', columns = ['Next Predicted Ovulation'])
    df_pred_fertile_window.to_csv('predictedfertilewindow.csv', columns = ['Next Predicted Fertile Window'])
