def existing_user_prediction:
    # This function analyzes basal body temperature and heart rate to predict the user's menses date, ovulation date, and fertility window
    # The output of this function is multiple .csv files containing the predicted dates

    import pandas as pd
    import datetime

    #loading in test dataset from excel: Real data would come into the backend via a .csv file (the same concepts would apply)
    df_menses_start = pd.read_excel (r'C:\Users\trent\Documents\BME 261L - Development & Analysis in BME Design\261L Python\existingusermensesdates.xlsx')
    df_menses_start['Menses Start Dates'] = pd.to_datetime(df_menses_start['Menses Start Dates'])           # Convert Dates to Datetime format

    # find length of menses date dataframe and index values of the four most recent dates
    len = len(df_menses_start.index.values)                                         # find the length of the past menses dates dataframe
    indexprev = len - 1                                                             # Index of previous menses date
    index2prev = len - 2                                                            # Index of 2nd to last menses date
    index3prev =len - 3                                                             # Index of 3rd to last menses date
    index4prev = len - 4                                                            # Index of 4th to last menses date

    # Get dates of previous menses dates from dataframe for Analysis
    lastmen = df_menses_start.iloc[indexprev]['Menses Start Dates']                 # Most recent menses start date
    lastmen2 = df_menses_start.iloc[index2prev]['Menses Start Dates']
    lastmen3 = df_menses_start.iloc[index3prev]['Menses Start Dates']
    lastmen4 = df_menses_start.iloc[index4prev]['Menses Start Dates']                # 4th most recent menses start date

    # Find the indexes of DFI dataframe of most recent cycles
    dfilen = len(dfi.index.values)                                                  # Find length of DFI dataframe
    for i in range(0,lendfi):                                                       # Iterate through indicator (DFI) dataframe
        if dfi.iloc[i]['Night of:'] == lastmen:                                     # Finding index of last menses start date in dfi dataframe
            lastmendfiindex = dfi.iloc[i]
        if dfi.iloc[i]['Night of:'] == lastmen2:                                    # Finding index of 2nd to last menses start date in dfi dataframe
            last2mendfiindex = dfi.iloc[i]
        if dfi.iloc[i]['Night of:'] == lastmen3:                                    # Finding index of 3rd to last menses start date in dfi dataframe
            last3mendfiindex = dfi.iloc[i]
        if dfi.iloc[i]['Night of:'] == lastmen4:                                    # Finding index of 4th to last menses start date in dfi dataframe
            last4mendfiindex = dfi.iloc[i]

    # Menses prediction
    # Find average length of past 3 menses cycles
    avgcyclelength = (((lastmen - lastmen2) + (lastmen2 - lastmen3) +               # Find average cycle length (from menses date to menses date)
            (lastmen3 - lastmen4)) / 3)

    #Add average cycle length to most recent menses date to predict next menses date
    nextmenses = lastmen + avgcyclelength                                           # Output is a datetime object

    #Store predicted menses date
    df_pred_menses_date = pd.DataFrame(columns = ['Predicted Menses Date'], data = [nextmenses])

    # Ovulation Date Prediction
    # Baseline Prediction (%20)
    basepred = lastmen + datetime.timedelta(days = 14)

    # Basal Body Temperature Prediction(60%)
    # Find when Basal Body temperature increased significantly in the previous three cycles
    for i in range(last4mendfiindex, last3mendfiindex):                             # Range of dates from 4th to last to 3rd to last menses dates
        if dfi.iloc[i+1]['Basal Body Temperature'] >                                # Finding if the next night's BBT is more than .4 degrees higher than this night
            ((dfi.iloc[i]['Basal Body Temperature']) + .4):
            nightofbbtincrease3 = dfi.iloc[i]['Night of:']                          # Store the date before BBT increased (ovulation date)
            break

    for i in range(last3mendfiindex, last2mendfiindex):                             # Range of dates from 3rd to last to 2nd to last menses dates
        if dfi.iloc[i+1]['Basal Body Temperature'] >                                # Finding if the next night's BBT is more than .4 degrees higher than this night
            ((dfi.iloc[i]['Basal Body Temperature']) + .4):
            nightofbbtincrease2 = dfi.iloc[i]['Night of:']                          # Store the date before BBT increased (ovulation date)
            break

    for i in range(last2mendfiindex, lastmendfiindex):                              # Range of dates from 2nd to last to most recent menses dates
        if dfi.iloc[i+1]['Basal Body Temperature'] >                                # Finding if the next night's BBT is more than .4 degrees higher than this night
            ((dfi.iloc[i]['Basal Body Temperature']) + .4):
            nightofbbtincrease = dfi.iloc[i]['Night of:']                           # Store the date before BBT increased (ovulation date)
            break

    #Find the length between BBT increase date and start of menses
    bbtinclength = nightofbbtincrease - lastmen2
    bbtinclength2 = nightofbbtincrease2 - lastmen3
    bbtinclength3 = nightofbbtincrease3 - lastmen4

    #Average the lengths between increase in BBT length and start of Menses
    bbtincavg = (bbtinclength + bbtinclength2 + bbtinclength3) / 3

    # Predict ovulation date by adding average bbt increase length to most recent menses start date
    bbtpred = bbtincavg + lastmen

    # Heart Rate Prediction (20%)
    # Find the night when heart rate increases by 4%
    for i in range(last4mendfiindex, last3mendfiindex):                             # Iterating through range of dates in indicator dataframe (4th to last to 3rd to last menses start dates)
        if dfi.iloc[i+1]['Average Heart Rate'] > (1.04 * (dfi.iloc[i]['Average Heart Rate'])):  #Find if the next night's avg heart rate increased by 4% compared to last night
            nightofhrincrease3 = dfi.iloc[i+1]['Night of:']                         # Store the date when the heart rate increase occured (ovulation date)
            break

    for i in range(last3mendfiindex, last2mendfiindex):                             # Iterating through range of dates in indicator dataframe (3rd to last to 2nd to last menses start dates)
        if dfi.iloc[i+1]['Average Heart Rate'] > (1.04 * (dfi.iloc[i]['Average Heart Rate'])):  #Find if the next night's avg heart rate increased by 4% compared to last night
            nightofhrincrease2 = dfi.iloc[i+1]['Night of:']                         # Store the date when the heart rate increase occured (ovulation date)
            break

    for i in range(last2mendfiindex, lastmendfiindex):                              # Iterating through range of dates in indicator dataframe(2nd to last to last menses start dates)
        if dfi.iloc[i+1]['Average Heart Rate'] > (1.04 * (dfi.iloc[i]['Average Heart Rate'])):  #Find if the next night's avg heart rate increased by 4% compared to last night
            nightofhrincrease = dfi.iloc[i+1]['Night of:']                          # Store the date when the heart rate increase occured (ovulation date)
            break

    #Find the length of time between increase in AVG Heart Rate and start of menses prior
    hrinclength = nightofhrincrease - lastmen2
    hrinclength2 = nightofhrincrease2 - lastmen3
    hrinclength3 = nightofhrincrease3 - lastmen4

    #Average the lengths between increase in nightly average heart rate and start of Menses
    hrincavg = (hrinclength + hrinclength2 + hrinclength3) / 3

    # Predict ovulation date by adding average hr increase length to most recent menses start date
    hrpred = hrincavg + lastmen

    #Find Final ovulation prediction
    nextovupred = ((0.2 * basepred) + (0.6 * bbtpred) + (0.2 * hrpred))             # Because the predicted dates are in a timestamp format, this formula gives a date as a function of time from the epoch
    nextovupred = nextovepred.date()                                                # Rounds the average to a day only rather than some time during the day, and converts to datetime format

    # Store predicted ovulation date
    df_pred_ovulation = pd.DataFrame(columns = ['Predicted Ovulation Date'], data = [nextovupred])


    # Fertile Window Prediction
    # Fertile window is the three days leading up to ovulation and the ovulation date
    ffd = nod - datetime.timedelta(days = 3)
    sfd = nod - datetime.timedelta(days = 2)
    tfd = nod - datetime.timedelta(days = 1)

    # Store Fertile Window Prediction
    df_pred_fertile_window = pd.DataFrame()                                         # Creating Dataframe to store predicted fertile window
    df_pred_fertile_window['Predicted Fertile Window'] = [ffd, sfd, tfd, nextovupred]       # Storing next predicted fertile window

    # Write prediction dataframes to a .csv file for use in the application interface
    df_pred_menses_date.to_csv('predictedmensesdate.csv', columns = ['Next Predicted Menses Date'])
    df_pred_ovulation.to_csv('predictedovulation.csv', columns = ['Next Predicted Ovulation'])
    df_pred_fertile_window.to_csv('predictedfertilewindow.csv', columns = ['Next Predicted Fertile Window'])
