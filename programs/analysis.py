"""
this program does analysis on the input dataset to find symbols that can be pursued
"""

from operator import index
import pandas as pd
import datetime 


def analyze(dfPattern, MADXCobraParams, filterParams):
    qualifiedSymbols = []
    dfAnalysisSummary = pd.DataFrame()
    for symbol in dfPattern['symbol'].unique():
        dfSymbol = dfPattern.loc[dfPattern['symbol']==symbol]
        
        latestHighPrice = dfSymbol.loc[dfSymbol.index[-1], 'High'] # used for skipping the unrequired symbols based on the filter conditions
        if latestHighPrice > filterParams['maxPrice']:
            continue #skip the symbols with price range beyond the price in the filter condition         
        
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
        'latestLow': latestLow,
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
            dictSummary.update({'suggestion':'buy'})
            #dfAnalysisSummary = dfAnalysisSummary.append(dictSummary, ignore_index=True) # append the data into summary dataset
            dfAnalysisSummary = pd.concat([dfAnalysisSummary, pd.DataFrame(dictSummary, index=[0])], axis=0)
        else:
            suggestion = 'skip' # set the acction to buy
            dictSummary.update({'suggestion':'skip'})
            #dfAnalysisSummary = dfAnalysisSummary.append(dictSummary, ignore_index=True)
            dfAnalysisSummary = pd.concat([dfAnalysisSummary, pd.DataFrame(dictSummary, index=[0])], axis=0)
        
    #print(dfAnalysisSummary)
    return dfAnalysisSummary
