import sys
sys.path.insert(0, '/Users/boopathi/Experiments/myTrade') #path of the app

from programs.get_trade_data import getTradedata
from programs.find_nodes import findNodes
from programs.support_and_resistance_lines import getSRLines
from programs.date_window import getDateWindow
from programs.viz_ADX_Cobra import vizADXCobra
from programs.pattern_MADX_Cobra import MADXCobra
from programs.analysis import analyze
from programs.gSheets import getSheetService, readSheet

import pandas as pd

# variables
dataPath = '/Users/boopathi/Experiments/myTrade/data/'
googleCredsPath = '/Users/boopathi/Experiments/myTrade/keys/credentials.json' #the path where the credentials downloaded from google sheets API
allSymbolsParams = {
    'sheetId':'1XoVUOt6cV5iVj8Ma5nHjkCZoWZTiJYjQI8miv4k3R-I', #get this from the share-link of the sheet
    'sheetRange': 'symbolsList!A:C' # range from the sheet, which contains information
    }
mySymbolsParams = {
    'sheetId':'16nJ1pC3cvFzF69zUnnaElFS0U7Rk4Pw1LAbsSzPUfyM', #get this from the share-link of the sheet
    'sheetRange': 'mySymbolsList!A:I' # range from the sheet, which contains information
    }

filterParams = {
    'lineTolerancePct':1,
    'minPrice':0,
    'maxPrice':500
}    

# execution mode
executionModes = {0:'Start Over',1:'Reuse Data'}
executionMode = executionModes[1]

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
MADXCobraParams = {
    'emaTimePeriod':10, 
    'smaTimePeriod':72, 
    'adxTimePeriod': 10, 
    'adxLowerLimit':20, 
    'adxUpperLimit':50,
    'resistnaceLimitPct':10, # consider only the resistance lines at this pct above the current high
    'supportLimitPct':10 # consider only the support lines at this pct below the current low
    }

# get the stocks list 
sheetService = getSheetService(credsPath=googleCredsPath)
dfAllSymbols = readSheet(sheetId=allSymbolsParams['sheetId'], sheetRange=allSymbolsParams['sheetRange'], service=sheetService)
#dfAllSymbols = dfAllSymbols.loc[dfAllSymbols['category']=='Nifty 150']
allSymbols = dfAllSymbols['symbol'].to_list()
#allSymbols = ['ASIANPAINT.NS', 'HDFC.NS', 'ICICIBANK.NS', 'ITC.NS', 'SBIN.NS', 'ULTRACEMCO.NS', 'ATGL.NS', 'BEL.NS', 'HAL.NS', 'INDHOTEL.NS', 'KAJARIACER.NS', 'NAVINFLUOR.NS', 'PAGEIND.NS', 'VINATIORGA.NS', 'WHIRLPOOL.NS']
#allSymbols = ['ASIANPAINT.NS', 'HDFC.NS', 'ICICIBANK.NS', 'RECLTD.NS','AMARAJABAT.NS','EIHOTEL.NS']
print(allSymbols)

dfMySymbols = readSheet(sheetId=mySymbolsParams['sheetId'], sheetRange=mySymbolsParams['sheetRange'], service=sheetService)
mySymbols = dfMySymbols['symbol'].to_list()

def analyzeAllSymbols(allSymbols, executionMode, dataPath, dateWindow, filterParams):
    dfRawTradeData = getTradedata(symbols=allSymbols, executionMode=executionMode, dataPath=dataPath, dateWindow=dateWindow, filterParams=filterParams)
    print("Raw data collected:")
    print(dfRawTradeData.head(10))

    dfPattern = MADXCobra(dfRawTradeData, params=MADXCobraParams)
    print('Pattern Data (tail sample):')
    print(dfPattern.tail(10))

    dfAnalysisSummary = analyze(dfPattern, MADXCobraParams=MADXCobraParams, filterParams=filterParams)
    print("Analysis Summary:")
    print(dfAnalysisSummary)
    suggestedSymbols = dfAnalysisSummary.loc[dfAnalysisSummary['suggestion']=='buy', 'symbol'].to_list()
    print('Suggested Symbols:', suggestedSymbols)

    dfNodes = findNodes(dfRawTradeData, suggestedSymbols, filterParams)
    print("Data with nodes - the turning points from low to high or high to low")
    print(dfNodes.sort_values(by=['symbol','scoreTops'], ascending=[True, False]).head(20))
    
    dfSupportLines, dfResistanceLines = getSRLines(df=dfNodes)
    print("Support Line data")
    print(dfSupportLines.head(10))
    print("Resistance Line data")
    print(dfResistanceLines.head(10))
    
    print("Visualizing data... ")
    vizADXCobra(symbols=suggestedSymbols, dfBase=dfPattern, dateWindow=dateWindow, dfSupportLines=dfSupportLines, dfResistanceLines=dfResistanceLines, params=MADXCobraParams)
    return dfSupportLines, dfResistanceLines

def trackMySymbols(mySymbols, executionMode, dataPath, dateWindow, MADXCobraParams, dfSupportLines, dfResistanceLines):
    dfRawTradeData = getTradedata(symbols=mySymbols, executionMode=executionMode, dataPath=dataPath, dateWindow=dateWindow)
    dfPattern = MADXCobra(dfRawTradeData, params=MADXCobraParams)
    dfAnalysisSummary = analyze(dfPattern, dfSupportLines, dfResistanceLines, MADXCobraParams=MADXCobraParams, filterParams=filterParams)
    vizADXCobra(symbols=mySymbols, dfBase=dfPattern, dateWindow=dateWindow, dfSupportLines=dfSupportLines, dfResistanceLines=dfResistanceLines, params=MADXCobraParams)
    print(dfAnalysisSummary)

dfSupportLines, dfResistanceLines = analyzeAllSymbols(allSymbols=allSymbols, executionMode=executionMode, dataPath=dataPath, dateWindow=dateWindow, filterParams=filterParams)

# Analysing/tracking the symbols that we own already.
executionMode = executionModes[1] # set the execution mode to reuse 
# trackMySymbols(mySymbols=mySymbols, executionMode=executionMode, dataPath=dataPath, dateWindow=dateWindow, MADXCobraParams=MADXCobraParams, dfSupportLines=dfSupportLines, dfResistanceLines=dfResistanceLines)
