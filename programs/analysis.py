"""
this program does analysis on the input dataset to find symbols that can be pursued
"""

from sqlite3 import Date
import pandas as pd
import datetime 


def analyze(dfPattern, dfSupportLines, dfResistanceLines, MADXCobraParams):
    qualifiedSymbols = []
    dfAnalysisSummary = pd.DataFrame()
    for symbol in dfPattern['symbol'].unique():
        dfSymbol = dfPattern.loc[dfPattern['symbol']==symbol]
        latestDate = dfSymbol.loc[dfSymbol.index.max(), 'Date']
        latestSMAHigh = dfSymbol.loc[dfSymbol.index.max(), 'SMAhigh']
        latestEMALow = dfSymbol.loc[dfSymbol.index.max(), 'EMAlow']
        latestEMAHigh = dfSymbol.loc[dfSymbol.index.max(), 'EMAhigh']
        latestADX = dfSymbol.loc[dfSymbol.index.max(), 'ADX']
        prevADX = dfSymbol.loc[dfSymbol.index.max()-1, 'ADX']
        ADXLowerLimit = MADXCobraParams['adxLowerLimit']
        ADXUpperLimit = MADXCobraParams['adxUpperLimit'] 
        latestLow = dfSymbol.loc[dfSymbol.index.max(), 'Low']
        obsDate = datetime.date.today()
        suggestion = 'skip'
        dictSummary = {'obsDate':obsDate,
        'symbol':symbol,
        'latestDate':latestDate,
        'latestSMAHigh':latestSMAHigh,
        'latestEMALow':latestEMALow,
        'latestEMAHigh':latestEMAHigh,
        'latestADX':latestADX,
        'prevADX':prevADX,
        'suggestion':suggestion}
        
        # condition
        if (latestEMALow > latestSMAHigh and 
            latestLow > latestEMAHigh and 
            latestADX > prevADX and 
            latestADX > ADXLowerLimit and latestADX < ADXUpperLimit):
            qualifiedSymbols.append(symbol)
            suggestion = 'buy' # set the acction to buy
            dfAnalysisSummary = dfAnalysisSummary.append(dictSummary, ignore_index=True) # append the data into summary dataset
        else:
            dfAnalysisSummary = dfAnalysisSummary.append(dictSummary, ignore_index=True)
        
    #print(dfAnalysisSummary)
    return dfAnalysisSummary