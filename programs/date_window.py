from calendar import month
import datetime
import pandas as pd

def getDateWindow(windowType, startDate, endDate, movingDays):
    today = datetime.date.today()
    if windowType == 'Custom Window':
        startDate = startDate
        endDate = endDate
    elif windowType == 'ITD':
        startDate = (today - pd.DateOffset(years=20)).date() # take data from 20 years ago!
        endDate = endDate
    elif windowType == 'WTD':
        offsetDays = today.weekday() 
        startDate = (today - pd.DateOffset(days=offsetDays)).date()
        endDate = today
    elif windowType == "MTD":
        startDate = today.replace(day=1)
        endDate = today
    elif windowType == 'YTD':
        startDate = today.replace(month=1).replace(day=1)
        endDate = today
    elif windowType == 'Rolling 3 Months':
        startDate = (today - pd.DateOffset(months=3)).date()
        endDate = today
    elif windowType == 'Rolling 6 Months':
        startDate = (today - pd.DateOffset(months=6)).date()
        endDate = today
    elif windowType == 'Rolling 12 Months':
        startDate = (today - pd.DateOffset(months=12)).date()
        endDate = today
    elif windowType == 'Rolling 24 Months':
        startDate = (today - pd.DateOffset(months=24)).date()
        endDate = today
    elif windowType == 'MVG':
        startDate = (today - pd.DateOffset(days=movingDays)).date()
        endDate = today
    dateWindow = {'windowType':windowType, 'startDate':startDate, 'endDate':endDate, 'movingDays':movingDays}
    print('update: start date: {}, end date: {}'.format(startDate, endDate))
    return dateWindow







