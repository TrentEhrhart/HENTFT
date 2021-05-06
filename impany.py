# This function analyzes newly imported data from the device
# The output is one row of indicators for each night of data into a pandas DataFrame (dfi)
# Newly imported data is appended to the user's permanent raw data temperature and heart rate dataframes(dftemp, dfhr)
# The final indicator dataframe is then exported to a .csv file to be read and displayed by the application
def import_analysis_func():

    impcount = impcount + 1                                                     # Keeps track of how many imports in a given night

    # ADD NEWLY IMPORTED DATA TO TEMPORARY HEART RATE AND TEMPERATURE DATAFRAMES
    dfhrimport = dfraw[[ 'Heart Rate']].copy()                                  # Temporary heart rate DataFrame
    dftempimport = dfraw[['Temperature']].copy()                                # Temporary temperature DataFrame

    # REMOVE POOR DATA FROM IMPORTED TEMPERATURE AND HEART RATE DATA SETS
    # Delete obscure data (anything +- 15% away from average) from the heart rate Dataframe
    hravg = dfhrimport['Heart Rate'].mean()                                     # Find average heart Rate
    hrplus15 = (hravg * .15) + hravg                                            # Avg Heart Rate + 15%
    hrminus15 = hravg - (hravg * .15)                                           # Avg Heart Rate - 15%
    dfhrimport = dfhrimport[dfhrimport['Heart Rate'] <= hrplus15]               # Remove data above threshold
    dfhrimport = dfhrimport[dfhrimport['Heart Rate'] >= hrminus15]              # Remove data below threshold
    dfhrimport = dfhrimport.reset_index()                                       # Resetting index after deletion of extraneous data

    # Delete obscure data (anything +- 5% away from average) from the temperature dataframe
    tempavg = dftempimport['Temperature'].mean()                                # Find average temperature
    tempplus5 = (tempavg * .05) + tempavg                                       # Avg temperature + 5%
    tempminus5 = tempavg - (tempavg * .05)                                      # Avg temperature - 5%
    dftempimport = dftempimport[dftempimport['Temperature'] <= tempplus5]       # Remove temperatures above threshold
    dftempimport = dftempimport[dftempimport['Temperature'] >= tempminus5]      # Remove temperatures below threshold
    dftempimport = dftempimport.reset_index()                                   # Reset index after deletion of extraneous data

    # FIND WHICH NIGHT THIS IMPORTED DATA CORRESPONDS TO
    timenow = datetime.datetime.now()                                           # Time right now
    todayonepm = timenow.replace(hour=13, minute=0, second=0, microsecond=0)    # One pm today
    if timenow > todayonepm:                                                    # It's still night-time and nightof = today's date
        nightof = datetime.datetime.now().date()
    else:                                                                       # It's the morning and nightof = yesterday's date
        nightof = datetime.datetime.now().date() - datetime.timedelta(days=+1)

    # Find indicators (BBT, average HR, recent HR)
    bbtimport = dftempimport['Temperature'].min()                               # Basal Body Temperature (lowest temp in dataframe)
    hravg = dfhrimport['Heart Rate'].mean()                                     # Average Heart Rate
    recenthr = dfhrimport['Heart Rate'].iloc[-1]                                # Most Recent Heart Rate

    # Determine if the indicator dataframe has been changed with this night's data
    recentnightof = dfi['Night of:'].iloc[-1]                                   # Finds which night was last edited
    if recentnightof == nightof:                                                # Data has already been imported tonight
        if bbtimport < dfi['Basal Body Temperature'].iloc[-1]                   # If the new bbt is lower than previous measurements, replace it
            dfi['Basal Body Temperature'].iloc[-1] = bbtimport
        hravg = ((hravg) + (impcount * dfi['Average Heart Rate'].iloc[-1])) / (impcount + 1)        # Calculate the new heart rate average by correctly weighting previous imported data
        dfi['Average Heart Rate'].iloc[-1] = hravg                              # Replace old avg heart rate with updated data
        dfi['Most Recent Heart Rate'].iloc[-1] = recenthr                       # Update Most Recent Heart Rate column with new data
    elif:                                                                       # Data for this night does not exist yet, this is the first dataset for tonight
        impcount = 1                                                            # Reset nightly import counter
        dfiadd = pd.DataFrame({"Night of:":[nightof], "Basal Body Temperature": [bbtimport], "Average Heart Rate": [hravg], "Most Recent Heart Rate": [recenthr]})
        dfi = dfi.Append(dfiadd, ignore_index = True)                           # Update indicator dataframe with a new row for tonight's data

    # Append raw imported data to temperature and heart rate dataframes
    dftemp = dftemp.append(dftempimport, reset_index = True)                    # Appends data to permanent dataframes and resets index
    dfhr = dfhr.append(dfhrimport, reset_index = True)

    # Copy indicator dataframe to .csv file to be used for application displays
    dfi.to_csv('indicatordataframe.csv', columns = ['Night of:', 'Basal Body Temperature', 'Average Heart Rate', 'Most Recent Heart Rate'])
