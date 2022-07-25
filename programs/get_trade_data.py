from calendar import month
import yfinance as yf
import pandas as pd
import numpy as np


def getTradedata(symbols, executionMode, dataPath, dateWindow):
    # dataframe definition
    tradeDataColumns=['symbol','Date','Open','High','Low','Close','Adj Close','Volume']
    tradeData = pd.DataFrame(columns=tradeDataColumns)
    windowType = dateWindow['windowType'] # resolved window type
    startDate = dateWindow['startDate'] # resolved start date
    endDate = dateWindow['endDate'] # resolved end date
    print("{} date window is: from {} to {}".format(windowType, startDate, endDate))
    # get the trade data for the symbols
    if executionMode == 'Start Over':
        for symbol in symbols:
            dfSymbol = yf.download(symbol,start=startDate, end=endDate)
            dfSymbol.reset_index(drop=False, inplace=True)
            dfSymbol['symbol']=symbol
            dfSymbol = dfSymbol[tradeDataColumns]
            dfSymbol['symbolRowNum'] = np.arange(start=0, stop=len(dfSymbol), step=1)
            tradeData = pd.concat([tradeData, dfSymbol],axis=0, ignore_index=True)
            print('Update: Geting the data for symbol {} from {} to {} is successful.'.format(symbol, dateWindow['startDate'], dateWindow['endDate']))
        tradeData.to_csv(dataPath+'tradeDataRaw.csv', sep='\t')
    else:
        print("Reusing the data that was collected already")
        tradeData = pd.read_csv(dataPath+'tradeDataRaw.csv', sep='\t', usecols=tradeDataColumns)

    # additional columns with some calculations to help further processing
    #tradeData['large'] = tradeData[['High','Low']].max(axis=1)
    #tradeData['small'] = tradeData[['High','Low']].min(axis=1)
    #tradeData['rowNum'] = np.arange(len(tradeData))
    tradeData['symbolRowNum'] = tradeData['symbolRowNum'].astype(np.int64) 
    tradeData.reset_index(inplace=True, drop=True)
    return tradeData

