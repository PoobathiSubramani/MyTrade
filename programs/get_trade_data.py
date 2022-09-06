
import yfinance as yf
import pandas as pd
import numpy as np


def getTradedata(symbols, executionMode, dataPath, dateWindow, filterParams, executionParams):
    # dataframe definition
    tradeDataColumns=['symbol','Date','Open','High','Low','Close','Adj Close','Volume']
    tradeData = pd.DataFrame(columns=tradeDataColumns)
    windowType = dateWindow['windowType'] # resolved window type
    startDate = dateWindow['startDate'] # resolved start date
    endDate = dateWindow['endDate'] # resolved end date
    fileSuffix = 'track' if executionParams['type']=='track' else 'analyze'
    fileName = 'tradeDataRaw_' + fileSuffix + '.csv'
    print("{} date window is: from {} to {}".format(windowType, startDate, endDate))
    # get the trade data for the symbols
    if executionMode == 'Start Over':
        for symbol in symbols:
            try:
                dfSymbol = yf.download(symbol,start=startDate, end=endDate)
                print('Got data for symbol - {}'.format(symbol))
            except:
                print('Attempt to get trade data for the symbol {} is failed. Please check.'.format(symbol))
                continue
            
            #print(dfSymbol.tail(10))            
            dfSymbol.reset_index(drop=False, inplace=True)

            latestHighPrice = dfSymbol.loc[dfSymbol.index[-1], 'High'] # used for skipping the unrequired symbols based on the filter conditions
            if latestHighPrice > filterParams['maxPrice']:            
                continue #skip the symbols with price range beyond the price in the filter condition  
            
            dfSymbol['symbol']=symbol
            dfSymbol = dfSymbol[tradeDataColumns]
            dfSymbol.loc[:,'symbolRowNum'] = np.arange(start=0, stop=len(dfSymbol), step=1)
            
            print('Trade Data <=  Price ({}) .'.format(filterParams['maxPrice']))
            #print(dfSymbol.tail(10))
            
            tradeData = pd.concat([tradeData, dfSymbol],axis=0, ignore_index=True)
            print('Update: Geting the data for symbol {} from {} to {} is successful.'.format(symbol, dateWindow['startDate'], dateWindow['endDate']))
            #tradeData.to_csv(dataPath+symbol+'.csv', sep='\t')
        tradeData['symbolRowNum'] = tradeData['symbolRowNum'].astype(np.int64)
        tradeData.to_csv(dataPath + fileName, sep='\t')
    else:
        print("Reusing the data that was collected already")
        #tradeData = pd.read_csv(dataPath+'tradeDataRaw.csv', dtype={'symbol':str,'Date':date,'Open':float,'High':float,'Low':float,'Close':float,'Adj Close':float,'Volume':int,'symbolRowNum':int},sep='\t', usecols=tradeDataColumns)
        tradeData = pd.read_csv(dataPath + fileName,sep='\t', parse_dates=['Date'],usecols=tradeDataColumns)
     
    tradeData.reset_index(inplace=True, drop=True)
    return tradeData

