import sys
sys.path.insert(0, '/Users/boopathi/Experiments/myTrade') #path of the app

from programs.get_trade_data import getTradedata
from programs.find_nodes import findNodes
from programs.support_and_resistance_lines import getSRLines
#from programs.candle_pattern_detector import detectCandlePattern
#from programs.support_and_resistance_lines import findSimilarNodes
#from programs.support_and_resistance_lines import findNodes
from programs.date_window import getDateWindow
from programs.viz_ADX_Cobra import vizADXCobra
from programs.pattern_MADX_Cobra import MADXCobra

import pandas as pd

# variables
dataPath = '/Users/boopathi/Experiments/myTrade/data/'
#dataPath = '/Users/boopathi/Library/CloudStorage/GoogleDrive-boopathy.s@gmail.com/My Drive/data'
tolerancePct = 1 

# execution mode
executionModes = {0:'Start Over',1:'Reuse Data'}
executionMode = executionModes[0]

# select the date window for the data to be collected
windowTypes = {0:"Custom Window",1:"ITD", 2:"YTD", 3:"MTD", 4:"WTD", 5:"Rolling 3 Months", 6:"Rolling 6 Months", 7:"Rolling 12 Months", 8:"Rolling 24 Months", 9:"MVG"}
windowType = windowTypes[9] # select the index from the above list
startDate = '2022-07-01'
endDate = '2022-07-21'
movingDays = 150
dateWindow = getDateWindow(windowType=windowType, startDate=startDate, endDate=endDate, movingDays=movingDays) # get the resolved start and end dates
startDate = dateWindow['startDate'] # resolved start date
endDate = dateWindow['endDate'] # resolved end date

# parameters for MADX Cobra strategy
MADXCobraParams = {'emaTimePeriod':10, 'smaTimePeriod':72, 'adxTimePeriod': 10, 'adxLowerLimit':20, 'adxUpperLimit':50}

# select the stocks list 
symbols = ['DMART.NS']
# TATACOMM, ASIANPAINT, DMART

dfRawTradeData = getTradedata(symbols=symbols, executionMode=executionMode, dataPath=dataPath, dateWindow=dateWindow)
print("Raw data collected:")
print(dfRawTradeData.head(10))
dfNodes = findNodes(dfRawTradeData, tolerancePct=tolerancePct)
print("Data with nodes - the turning points from low to high or high to low")
print(dfNodes.head(10))
dfResistanceLines, dfSupportLines = getSRLines(df=dfNodes)
print("Resistance and Support Line data")
print(dfResistanceLines.head(10), dfSupportLines.head(10))
dfPattern = MADXCobra(dfRawTradeData, params=MADXCobraParams)
print("Visualizing data...")
vizADXCobra(dfPattern, dateWindow=dateWindow, dfSupportLines=dfSupportLines, dfResistanceLines=dfResistanceLines, params=MADXCobraParams)



#dfRawTradeData = detectCandlePattern(dfRawTradeData) #adding candle patterns to the raw data
#dfTest = dfRawTradeData.loc[dfRawTradeData['ADX']>=20]
#dfTest['action'] = 'buy' if dfTest.loc[dfTest['ADX']>dfTest['ADXR']] else 'sell'
#dfTest['action'] = dfTest.apply(lambda x: 'buy' if x['ADX']>x['ADXR'] else 'sell', axis=1)
#print(dfRawTradeData.tail(20))
#print(dfTest)

#vizADXCobra(dfBase=dfRawTradeData, dateWindow = dateWindow, params=MADXCobraParams)

#dfNodes = findNodes(dfRawTradeData=dfRawTradeData)
#dfNeighborNodes = findSimilarNodes(dfNodes=dfNodes, tolerance=tolerancePct, dataPath=dataPath)
#dfLines = getSupportAndResistanceLines(dfNeighborNodes=dfNeighborNodes, dataPath=dataPath)
#dfLines.to_csv(dataPath+'support_and_resistance_lines'+'.csv', sep='\t')
#drawVisualization(dfBase=dfRawTradeData, dfLines=dfLines, dateWindow = dateWindow)